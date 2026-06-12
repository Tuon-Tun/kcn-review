# -*- coding: utf-8 -*-
"""
KIỂM CHỨNG MÁY (Bước 3 quy trình legal-review): đối chiếu từng trích dẫn luật
trong findings với nội dung thật trong laws/**/*.txt bằng khớp chuỗi.

Cách dùng:
  python scripts/verify_citation.py <findings.json>     # kiểm chứng findings
  python scripts/verify_citation.py --selftest           # tự kiểm tra chính nó

Định dạng findings.json: danh sách các finding, mỗi cái gồm:
  {
    "id": "F1",
    "muc_do": "DO|VANG|XANH",
    "dieu_khoan_hd": "Điều X hợp đồng — trích nguyên văn",
    "van_de": "mô tả vấn đề",
    "quoted_law_text": "TRÍCH NGUYÊN VĂN đoạn luật làm căn cứ",
    "source_file": "moi-truong/BVMT-2020.txt",   (đường dẫn tương đối trong laws/)
    "dieu_khoan_luat": "Điều 51 Luật BVMT 2020",
    "de_xuat": "đề xuất sửa"
  }

Quy tắc: chuẩn hóa NFC + gộp mọi khoảng trắng thành 1 dấu cách, rồi tìm chuỗi con.
FAIL = trích dẫn không tồn tại nguyên văn trong file nguồn → finding bị LOẠI.
Kết quả ghi ra <findings>_verified.json; exit code 0 nếu tất cả PASS, 2 nếu có FAIL.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAWS = ROOT / "laws"


def normalize(text):
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


def verify(findings):
    results = []
    cache = {}
    for f in findings:
        src = f.get("source_file", "")
        quoted = f.get("quoted_law_text", "")
        path = LAWS / src
        if not quoted or not src:
            status, reason = "FAIL", "thieu quoted_law_text hoac source_file"
        elif not path.exists():
            status, reason = "FAIL", f"file nguon khong ton tai: {src}"
        else:
            if src not in cache:
                cache[src] = normalize(path.read_text(encoding="utf-8"))
            if normalize(quoted) in cache[src]:
                status, reason = "PASS", ""
            else:
                status, reason = "FAIL", "khong tim thay nguyen van trich dan trong file nguon"
        results.append({**f, "verify_status": status, "verify_reason": reason})
    return results


def selftest():
    import tempfile
    real = "Điều 51. Hạ tầng bảo vệ môi trường của khu sản xuất, kinh doanh tập trung."
    with tempfile.TemporaryDirectory() as td:
        # giả lập laws/ tạm để test độc lập
        global LAWS
        old_laws = LAWS
        LAWS = Path(td)
        (LAWS / "test").mkdir()
        (LAWS / "test" / "luat-test.txt").write_text(
            "Mở đầu.\n" + real + "\nKết thúc.", encoding="utf-8")
        cases = [
            # 1. trích đúng nguyên văn -> PASS
            {"id": "T1", "quoted_law_text": real, "source_file": "test/luat-test.txt"},
            # 2. trích đúng nhưng xuống dòng/khoảng trắng khác -> vẫn PASS
            {"id": "T2", "quoted_law_text": "Điều 51.  Hạ tầng\nbảo vệ môi trường của khu sản xuất, kinh doanh tập trung.",
             "source_file": "test/luat-test.txt"},
            # 3. trích dẫn BỊA (đổi một chữ) -> phải FAIL
            {"id": "T3", "quoted_law_text": real.replace("Điều 51", "Điều 52"),
             "source_file": "test/luat-test.txt"},
            # 4. file nguồn không tồn tại -> FAIL
            {"id": "T4", "quoted_law_text": real, "source_file": "test/khong-co.txt"},
        ]
        r = verify(cases)
        expect = ["PASS", "PASS", "FAIL", "FAIL"]
        ok = [x["verify_status"] for x in r] == expect
        for x, e in zip(r, expect):
            mark = "✓" if x["verify_status"] == e else "✗ SAI"
            print(f"  {x['id']}: {x['verify_status']} (mong doi {e}) {mark}")
        LAWS = old_laws
        if not ok:
            print("SELF-TEST THAT BAI — KHONG DUOC dung script nay de kiem chung")
            sys.exit(1)
        print("SELF-TEST OK: script bat duoc trich dan bia va chap nhan trich dan that.")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--selftest":
        selftest()
        return
    src = Path(sys.argv[1])
    findings = json.loads(src.read_text(encoding="utf-8"))
    results = verify(findings)
    out = src.with_name(src.stem + "_verified.json")
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    n_pass = sum(1 for r in results if r["verify_status"] == "PASS")
    n_fail = len(results) - n_pass
    for r in results:
        print(f"{r.get('id','?')}: {r['verify_status']}"
              + (f" — {r['verify_reason']}" if r["verify_reason"] else ""))
    print(f"\nKet qua: {n_pass} PASS, {n_fail} FAIL (finding FAIL phai bi LOAI khoi bao cao)")
    print(f"Da ghi: {out}")
    sys.exit(2 if n_fail else 0)


if __name__ == "__main__":
    main()
