# KCN Review — Trợ lý review hợp đồng Khu Công Nghiệp

## Cái này là gì?

Một công cụ chạy trên máy tính của bạn. Bạn **thả file hợp đồng vào → bấm 1 nút →
nhận về báo cáo Word** chỉ ra các điều khoản rủi ro, kèm căn cứ pháp luật.
Nó cũng biết **dịch hợp đồng Việt–Anh** và **so sánh bản tiếng Việt với bản tiếng Anh**.

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
- Mở phần mềm Claude Code vừa cài → nó sẽ hỏi đăng nhập → đăng nhập bằng
  tài khoản Claude của bạn (cần gói **Pro** trở lên, khoảng $20/tháng).
- Chưa có tài khoản? Đăng ký tại https://claude.ai

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
- Mở thư mục `Documents` → thấy thư mục **kcn-review** là xong phần cài đặt. 🎉

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
   - 🔍 **Review hợp đồng** — tìm điều khoản rủi ro
   - 🌐 **Dịch VI↔EN** — dịch hợp đồng
   - 📑 **Đối chiếu song ngữ** — so bản Việt với bản Anh (cần tải lên cả 2 file)
3. Chờ vài phút. Chữ chạy trên màn hình = nó đang làm việc. Cứ để yên.

### Bước 3: Lấy báo cáo
- **Ô số 3**: báo cáo hiện ra dạng file Word → bấm vào tên file để tải về → mở đọc.

### Tắt công cụ khi xong việc
- Đóng cửa sổ đen là xong.

---

## Khi gặp lỗi — tra bảng này

| Hiện tượng | Cách xử lý |
|---|---|
| Bấm `start-web.bat` xong cửa sổ đen tắt ngay | Python chưa cài đúng. Cài lại Python, NHỚ tick "Add Python to PATH" |
| Trình duyệt báo "không kết nối được" | Cửa sổ đen đã bị tắt. Bấm đúp `start-web.bat` lại |
| Báo cáo ghi "KHÔNG TÌM THẤY CƠ SỞ PHÁP LÝ" | Bình thường — nghĩa là chưa nạp đủ file luật vào thư mục `laws/`. Hỏi người quản lý công cụ |
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

- Engine: Claude Code chạy headless, nạp `CLAUDE.md` + 3 skill trong `.claude/skills/`
  (legal-review 4 bước có kiểm chứng trích dẫn, legal-translate, bilingual-compare).
- Văn bản luật: nạp thủ công file `.txt` vào `laws/` + cập nhật `laws/metadata.csv`
  (cấp hiệu lực, ngày hiệu lực — dữ liệu mẫu hiện tại cần kiểm tra lại).
  Agent không bao giờ tự sửa `laws/`.
- Thuật ngữ dịch: `termbase/termbase.csv` (cột `vi,en_chuan,bien_the,ghi_chu,loai_hd`).
- Web: `webapp/app.py` (Flask, cổng 8765). Mặc định chỉ máy này dùng được;
  đổi `HOST` thành `"0.0.0.0"` để mở cho mạng LAN.
- Web tự tìm Claude Code tại `%LOCALAPPDATA%\AnthropicClaude\claude.exe` hoặc lệnh
  `claude` trong PATH; cài chỗ khác thì sửa `CLAUDE_CANDIDATES` đầu `webapp/app.py`.
- `.gitignore` đang TẠM MỞ để chuyển giao dữ liệu — khôi phục chặn `contracts/`,
  `reports/` sau khi chuyển giao xong.

</details>
