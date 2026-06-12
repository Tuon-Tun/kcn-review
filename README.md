# KCN Review — Trợ lý review hợp đồng Khu Công Nghiệp

## Cái này là gì?

Một công cụ chạy trên máy tính của bạn. Bạn **thả file hợp đồng vào → bấm 1 nút →
nhận về báo cáo Word** chỉ ra các điều khoản rủi ro, kèm căn cứ pháp luật được
**máy kiểm chứng nguyên văn** (trích dẫn bịa tự động bị loại).
Nó cũng biết **dịch hợp đồng Việt–Anh** và **so sánh bản tiếng Việt với bản tiếng Anh**.

Đi kèm sẵn **kho 36 văn bản luật** (đã rà hiệu lực đến 06/2026) — xem
[bản đồ văn bản](laws/SO-DO-VAN-BAN.md) để biết kho có gì và các quan hệ
thay thế/sửa đổi. Hệ thống đã chạy thử end-to-end thành công.

Không cần biết lập trình. Chỉ cần biết mở trình duyệt.

---

## PHẦN 1 — Cài đặt (chỉ làm 1 lần, khoảng 30 phút)

### Bước 1: Cài 3 phần mềm
Tải về và cài như cài phần mềm bình thường (bấm Next liên tục là được):

1. **Git** — tải tại: https://git-scm.com/download/win
2. **Python** — tải tại: https://www.python.org/downloads/
   - ⚠️ QUAN TRỌNG: ở màn hình đầu tiên khi cài, **tick vào ô "Add Python to PATH"**
     (ô vuông nhỏ ở dưới cùng) rồi mới bấm Install.
3. **Claude Code** — tải tại: https://claude.com/claude-code

### Bước 2: Đăng nhập Claude
- Mở phần mềm Claude Code vừa cài → đăng nhập bằng tài khoản Claude của bạn
  (cần gói **Pro** trở lên). Chưa có? Đăng ký tại https://claude.ai

### Bước 3: Tải công cụ về máy
1. Nhờ người quản lý công cụ (chủ repo GitHub) **mời tài khoản GitHub của bạn**
   vào dự án trước. Chưa có tài khoản GitHub? Đăng ký miễn phí tại https://github.com
2. Mở menu Start → gõ `cmd` → Enter. Một cửa sổ đen hiện ra.
3. Gõ (hoặc dán) từng dòng sau, mỗi dòng xong bấm Enter:

```
cd Documents
git clone https://github.com/Tuon-Tun/kcn-review.git
cd kcn-review
pip install -r webapp/requirements.txt
```

(Lần đầu chạy `git clone` máy sẽ hỏi đăng nhập GitHub — làm theo hướng dẫn trên màn hình.)

### Bước 4: Kiểm tra
- Mở thư mục `Documents` → thấy thư mục **kcn-review** là xong. 🎉
- **Kho luật 36 văn bản đã có sẵn trong repo** — không phải nạp gì thêm.

---

## PHẦN 2 — Dùng hằng ngày (3 bước)

### Bước 1: Mở công cụ
- Vào thư mục `Documents\kcn-review` → **bấm đúp file `start-web.bat`**
- Một cửa sổ đen hiện ra (ĐỪNG TẮT nó — tắt là công cụ ngừng chạy)
- Trình duyệt tự mở trang công cụ. Nếu không tự mở, tự gõ vào trình duyệt:
  **http://127.0.0.1:8765**

### Bước 2: Thả hợp đồng vào và bấm nút
Trên trang web có 3 ô đánh số sẵn, làm từ trên xuống:
1. **Ô số 1**: bấm "Choose File" → chọn file hợp đồng (PDF hoặc Word) → bấm **Tải lên**
2. **Ô số 2**: chọn việc cần làm:
   - 🔍 **Review hợp đồng** — tìm điều khoản rủi ro, có kiểm chứng trích dẫn
   - 🌐 **Dịch VI↔EN** — dịch hợp đồng
   - 📑 **Đối chiếu song ngữ** — so bản Việt với bản Anh (cần tải lên cả 2 file)
3. Chờ vài phút. Chữ chạy trên màn hình = nó đang làm việc. Cứ để yên.

### Bước 3: Lấy báo cáo
- **Ô số 3**: báo cáo hiện ra dạng file Word → bấm vào tên file để tải về → mở đọc.
- Báo cáo luôn có mục "CẦN NGƯỜI XEM" — đó là phần máy không dám tự kết luận,
  người làm pháp chế phải đọc.

### Tắt công cụ khi xong việc
- Đóng cửa sổ đen là xong.

---

## Khi gặp lỗi — tra bảng này

| Hiện tượng | Cách xử lý |
|---|---|
| Bấm `start-web.bat` xong cửa sổ đen tắt ngay | Python chưa cài đúng. Cài lại Python, NHỚ tick "Add Python to PATH" |
| Trình duyệt báo "không kết nối được" | Cửa sổ đen đã bị tắt. Bấm đúp `start-web.bat` lại |
| Báo cáo ghi "KHÔNG TÌM THẤY CƠ SỞ PHÁP LÝ" | Có thể đúng (kho không có quy định) hoặc thiếu văn bản — hỏi người quản lý, xem [bản đồ kho luật](laws/SO-DO-VAN-BAN.md) |
| Chạy mãi không xong (quá 30 phút) | Đóng cửa sổ đen, mở lại, thử lại với file nhỏ hơn |
| Lỗi khác không hiểu | Chụp màn hình, gửi người quản lý công cụ |

---

## ⚠️ 3 điều bắt buộc nhớ

1. **Máy phải có mạng internet** khi chạy (công cụ cần gọi Claude).
2. **AI chỉ hỗ trợ, không thay thế người làm pháp chế.** Phát hiện quan trọng
   phải tự kiểm tra lại trước khi dùng để đàm phán hay ký kết.
3. **Hợp đồng là tài liệu mật.** Không gửi thư mục `contracts/` và `reports/`
   cho người ngoài.

---

<details>
<summary>📎 Thông tin kỹ thuật (dành cho người quản lý công cụ — bấm để mở)</summary>

### Kiến trúc
- Engine: Claude Code chạy headless, nạp `CLAUDE.md` + 4 skill trong `.claude/skills/`:
  `legal-review` (4 bước có kiểm chứng), `legal-translate`, `bilingual-compare`,
  `law-fetch` (tải luật vào khu chờ duyệt `laws_staging/` — KHÔNG bao giờ tự ghi `laws/`).
- Web: `webapp/app.py` (Flask, cổng 8765). Mặc định chỉ máy này; đổi `HOST="0.0.0.0"`
  để mở LAN. Tự tìm Claude tại `%LOCALAPPDATA%\AnthropicClaude\claude.exe` hoặc PATH.

### Kho luật
- `laws/` — 36 văn bản / 8 nhóm, kèm `metadata.csv` (cấp hiệu lực, ngày hiệu lực,
  is_active) và [SO-DO-VAN-BAN.md](laws/SO-DO-VAN-BAN.md) (bản đồ quan hệ + thống kê
  + quy trình bổ sung). Văn bản hết hiệu lực giữ lại cho HĐ ký giai đoạn cũ.
- Cập nhật kho: gõ "rà soát hiệu lực" với agent, hoặc tải .docx từ thuvienphapluat
  đưa agent convert (quy trình ở mục 5 của bản đồ).

### Scripts
- `scripts/verify_citation.py` — kiểm chứng trích dẫn (B3); có `--selftest`.
- `scripts/fetch_laws.py` — tải luật từ nguồn chính thống (xdcs/vbpl.moj/congbao).
- `scripts/doc_extract.py` — bóc text file .doc cũ không cần MS Word.
- `scripts/push_via_api.ps1` — đẩy GitHub qua REST API khi proxy chặn git push.

### Lưu ý vận hành
- `.gitignore` đang TẠM MỞ phục vụ chuyển giao — `contracts/` và `reports/` hiện
  được commit. **Khôi phục chặn ngay sau khi chuyển giao xong** (hợp đồng là tài liệu mật).
- Theo dõi định kỳ: dự thảo NĐ thay NĐ 35/2022; NĐ hướng dẫn Luật Đầu tư 143/2025.

</details>
