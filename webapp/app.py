# -*- coding: utf-8 -*-
"""
Giao diện web cho tool kcn-review — dành cho người dùng non-tech.
Chạy: python webapp/app.py  (hoặc bấm đúp start-web.bat ở thư mục gốc)

Web app này KHÔNG tự phân tích hợp đồng. Nó chỉ:
  1. Nhận file upload -> lưu vào contracts/inbox/
  2. Gọi Claude Code (chế độ headless) với prompt cố định -> Claude chạy đúng
     skill legal-review / legal-translate / bilingual-compare như khi gõ tay.
  3. Hiện tiến độ và cho tải báo cáo từ reports/
"""
import os
import re
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request, send_from_directory

ROOT = Path(__file__).resolve().parent.parent          # thư mục kcn-review/
INBOX = ROOT / "contracts" / "inbox"
DONE = ROOT / "contracts" / "done"
REPORTS = ROOT / "reports"

# Đường dẫn Claude Code CLI — sửa lại nếu cài ở chỗ khác
CLAUDE_CANDIDATES = [
    Path(os.environ["LOCALAPPDATA"]) / "AnthropicClaude" / "claude.exe",
    "claude",  # fallback: có sẵn trong PATH
]

# Chỉ cho phép agent chạy python/pip và di chuyển file — KHÔNG cấp quyền rộng hơn.
ALLOWED_TOOLS = "Bash(python:*),Bash(py:*),Bash(pip:*),Bash(mv:*),Bash(move:*)"

# host="127.0.0.1": chỉ máy này dùng. Đổi thành "0.0.0.0" nếu muốn
# đồng nghiệp cùng mạng LAN truy cập (mở web bằng http://<IP-máy-này>:8765)
HOST = "127.0.0.1"
PORT = 8765

ALLOWED_EXT = {".pdf", ".docx", ".doc", ".txt"}

app = Flask(__name__)

job_lock = threading.Lock()
job = {"running": False, "action": None, "file": None,
       "log": "", "started": None, "finished": None, "exit_code": None}


def find_claude():
    for c in CLAUDE_CANDIDATES:
        if isinstance(c, Path):
            if c.exists():
                return str(c)
        else:
            from shutil import which
            if which(c):
                return c
    return None


def safe_name(name):
    name = os.path.basename(name)
    return re.sub(r'[^\wÀ-ỹ .\-()]', "_", name)


def run_claude(prompt, action, filename):
    claude = find_claude()
    with job_lock:
        if claude is None:
            job.update(running=False, exit_code=-1,
                       log="LỖI: Không tìm thấy Claude Code CLI. Sửa CLAUDE_CANDIDATES trong webapp/app.py")
            return
        job["log"] = f"[{datetime.now():%H:%M:%S}] Bắt đầu {action} — {filename}\nĐang gọi Claude Code, việc này có thể mất vài phút...\n"
    cmd = [claude, "-p", prompt,
           "--verbose",  # in tiến trình từng bước — không có thì ô log đứng im đến khi xong
           "--permission-mode", "acceptEdits",
           "--allowedTools", ALLOWED_TOOLS]
    try:
        proc = subprocess.Popen(cmd, cwd=str(ROOT),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding="utf-8", errors="replace")
        for line in proc.stdout:
            with job_lock:
                job["log"] += line
        proc.wait(timeout=3600)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        code = -2
        with job_lock:
            job["log"] += "\nLỖI: quá 60 phút, đã dừng tiến trình.\n"
    except Exception as e:
        code = -1
        with job_lock:
            job["log"] += f"\nLỖI: {e}\n"
    with job_lock:
        job["log"] += f"\n[{datetime.now():%H:%M:%S}] {'✓ HOÀN THÀNH' if code == 0 else '✗ KẾT THÚC CÓ LỖI (mã ' + str(code) + ')'} — xem mục Báo cáo bên dưới.\n"
        job.update(running=False, finished=time.time(), exit_code=code)


PROMPTS = {
    "review": 'Dùng skill legal-review để review hợp đồng "contracts/inbox/{f}". {extra}',
    "translate": 'Dùng skill legal-translate để dịch file "contracts/inbox/{f}". {extra}',
    "compare": 'Dùng skill bilingual-compare để đối chiếu song ngữ hai file "contracts/inbox/{f}" và "contracts/inbox/{f2}". {extra}',
}


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.post("/api/upload")
def upload():
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify(error="Chưa chọn file"), 400
    name = safe_name(f.filename)
    if Path(name).suffix.lower() not in ALLOWED_EXT:
        return jsonify(error="Chỉ nhận PDF, DOCX, DOC, TXT"), 400
    f.save(str(INBOX / name))
    return jsonify(ok=True, name=name)


@app.get("/api/state")
def state():
    with job_lock:
        j = dict(job)
    j["inbox"] = sorted(p.name for p in INBOX.iterdir() if p.is_file())
    j["reports"] = sorted((p.name for p in REPORTS.iterdir()
                           if p.is_file() and p.suffix.lower() == ".docx"), reverse=True)
    return jsonify(j)


@app.post("/api/run")
def run():
    data = request.get_json(force=True)
    action = data.get("action")
    f1, f2 = data.get("file"), data.get("file2")
    extra = data.get("extra", "").strip()
    if action not in PROMPTS:
        return jsonify(error="Hành động không hợp lệ"), 400
    if not f1 or not (INBOX / safe_name(f1)).exists():
        return jsonify(error="File không tồn tại trong inbox"), 400
    if action == "compare" and (not f2 or not (INBOX / safe_name(f2)).exists()):
        return jsonify(error="Đối chiếu song ngữ cần chọn đủ 2 file"), 400
    with job_lock:
        if job["running"]:
            return jsonify(error="Đang có việc chạy — chờ xong đã"), 409
        job.update(running=True, action=action, file=f1, log="",
                   started=time.time(), finished=None, exit_code=None)
    prompt = PROMPTS[action].format(
        f=safe_name(f1), f2=safe_name(f2 or ""),
        extra=(f"Thông tin thêm từ người dùng: {extra}" if extra else ""))
    threading.Thread(target=run_claude, args=(prompt, action, f1), daemon=True).start()
    return jsonify(ok=True)


@app.get("/reports/<path:name>")
def download(name):
    return send_from_directory(str(REPORTS), name, as_attachment=True)


PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<title>KCN Review — Review hợp đồng Khu Công Nghiệp</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
 body{font-family:'Segoe UI',Arial,sans-serif;margin:0;background:#f4f6f8;color:#1a2733}
 header{background:#0f3a5d;color:#fff;padding:14px 28px}
 header h1{margin:0;font-size:20px} header p{margin:2px 0 0;font-size:13px;opacity:.8}
 main{max-width:880px;margin:24px auto;padding:0 16px}
 .card{background:#fff;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:18px 22px;margin-bottom:18px}
 .card h2{margin:0 0 12px;font-size:16px;color:#0f3a5d}
 button{background:#0f3a5d;color:#fff;border:0;border-radius:6px;padding:9px 16px;font-size:14px;cursor:pointer}
 button:hover{background:#15517f} button:disabled{background:#9db2c2;cursor:not-allowed}
 select,input[type=text]{padding:8px;border:1px solid #c6d2db;border-radius:6px;font-size:14px;min-width:240px}
 .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:8px 0}
 #log{background:#0d1117;color:#c9d1d9;font-family:Consolas,monospace;font-size:12px;
      padding:12px;border-radius:8px;white-space:pre-wrap;max-height:320px;overflow-y:auto;display:none}
 .files li{margin:4px 0} .files a{color:#0f3a5d;font-weight:600}
 .badge{display:inline-block;background:#e8f0e8;color:#2d6a2d;border-radius:12px;padding:2px 10px;font-size:12px;margin-left:8px}
 .running{background:#fff3df;color:#8a5a00}
 .note{font-size:12px;color:#5b6b78;margin-top:10px}
</style></head><body>
<header><h1>⚖️ KCN Review</h1><p>Review · Dịch · Đối chiếu hợp đồng — Phòng Pháp chế, Thanh Bình Phú Mỹ</p></header>
<main>
 <div class="card"><h2>1️⃣ Đưa hợp đồng vào</h2>
  <div class="row"><input type="file" id="file" accept=".pdf,.docx,.doc,.txt">
   <button onclick="upload()">Tải lên</button><span id="upmsg"></span></div>
  <div class="note">File nhận: PDF, DOCX, DOC, TXT. File sẽ nằm trong hộp chờ (inbox) bên dưới.</div>
 </div>

 <div class="card"><h2>2️⃣ Chọn việc cần làm</h2>
  <div class="row"><label>Hợp đồng:</label><select id="f1"></select></div>
  <div class="row" id="f2row" style="display:none"><label>Bản thứ hai (EN):</label><select id="f2"></select></div>
  <div class="row"><label>Ghi chú thêm (vd: ngày ký 2025-03-15):</label><input type="text" id="extra" placeholder="không bắt buộc"></div>
  <div class="row">
   <button onclick="run('review')">🔍 Review hợp đồng</button>
   <button onclick="run('translate')">🌐 Dịch VI↔EN</button>
   <button onclick="toggleCompare()">📑 Đối chiếu song ngữ…</button>
   <span id="status"></span>
  </div>
  <div class="row" id="comparerow" style="display:none"><button onclick="run('compare')">▶ Chạy đối chiếu 2 file đã chọn</button></div>
  <pre id="log"></pre>
  <div class="note">Mỗi lượt chạy mất vài phút. Review tuân thủ quy trình 4 bước có kiểm chứng trích dẫn — finding không xác minh được sẽ tự bị loại.</div>
 </div>

 <div class="card"><h2>3️⃣ Báo cáo (bấm để tải)</h2><ul class="files" id="reports"></ul>
  <div class="note">⚠️ AI hỗ trợ review, không thay thế tư vấn pháp lý. Verify finding quan trọng trước khi sử dụng.</div>
 </div>
</main>
<script>
let running=false;
async function upload(){
 const f=document.getElementById('file').files[0];
 if(!f){document.getElementById('upmsg').textContent='Chưa chọn file';return}
 const fd=new FormData();fd.append('file',f);
 const r=await fetch('/api/upload',{method:'POST',body:fd});const j=await r.json();
 document.getElementById('upmsg').textContent=j.ok?('✓ Đã nhận '+j.name):('✗ '+j.error);
 refresh();
}
function toggleCompare(){
 const r2=document.getElementById('f2row'),rc=document.getElementById('comparerow');
 const show=r2.style.display==='none';
 r2.style.display=rc.style.display=show?'flex':'none';
}
async function run(action){
 const body={action,file:val('f1'),file2:val('f2'),extra:val('extra')};
 const r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const j=await r.json();
 if(j.error){document.getElementById('status').textContent='✗ '+j.error;return}
 document.getElementById('log').style.display='block';
}
function val(id){return document.getElementById(id).value}
async function refresh(){
 const j=await (await fetch('/api/state')).json();
 fill('f1',j.inbox);fill('f2',j.inbox);
 const st=document.getElementById('status');
 st.innerHTML=j.running?'<span class="badge running">⏳ Đang chạy: '+j.action+' — '+j.file+'</span>'
   :(j.exit_code===0?'<span class="badge">✓ Xong</span>':(j.exit_code!=null?'<span class="badge running">✗ Có lỗi</span>':''));
 const log=document.getElementById('log');
 if(j.log){log.style.display='block';if(log.textContent!==j.log){log.textContent=j.log;log.scrollTop=log.scrollHeight}}
 document.getElementById('reports').innerHTML=j.reports.map(n=>'<li><a href="/reports/'+encodeURIComponent(n)+'">📄 '+n+'</a></li>').join('')||'<li>Chưa có báo cáo nào</li>';
 running=j.running;
}
function fill(id,items){
 const s=document.getElementById(id),cur=s.value;
 s.innerHTML=items.map(n=>'<option>'+n+'</option>').join('');
 if(items.includes(cur))s.value=cur;
}
setInterval(refresh,2500);refresh();
</script></body></html>"""


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, không in được tiếng Việt
    except Exception:
        pass
    for d in (INBOX, DONE, REPORTS):
        d.mkdir(parents=True, exist_ok=True)
    print(f"\n  KCN Review web đang chạy: http://{HOST}:{PORT}\n  Đóng cửa sổ này để tắt.\n")
    app.run(host=HOST, port=PORT, debug=False)
