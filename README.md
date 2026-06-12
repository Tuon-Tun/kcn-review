# KCN Review — Tool review hợp đồng Khu Công Nghiệp

Tool hỗ trợ pháp chế Ban Quản lý KCN review / dịch / đối chiếu song ngữ hợp đồng,
chạy trên Claude Code với quy trình 4 bước có kiểm chứng trích dẫn (chống bịa căn cứ).

## Yêu cầu
- [Claude Code](https://claude.com/claude-code) đã đăng nhập (gói Pro trở lên)
- Python 3.10+ và Flask (`pip install flask`) — chỉ cần nếu dùng giao diện web

## Cài đặt sau khi clone
1. **Nạp văn bản luật** vào `laws/` (dạng `.txt` để kiểm chứng trích dẫn hoạt động)
   và cập nhật `laws/metadata.csv` (cấp hiệu lực + ngày hiệu lực). ⚠️ Dữ liệu mẫu
   trong metadata.csv cần kiểm tra lại ngày hiệu lực trước khi dùng.
2. Bổ sung thuật ngữ vào `termbase/termbase.csv` (cột: `vi,en_chuan,bien_the,ghi_chu,loai_hd`).

## Cách dùng
**Dòng lệnh:** mở Claude Code trong thư mục này, thả hợp đồng vào `contracts/inbox/`,
gõ: *"review hợp đồng <tên file>"* — skill `legal-review` tự kích hoạt.

**Giao diện web (cho người không rành kỹ thuật):** bấm đúp `start-web.bat`,
trình duyệt mở `http://127.0.0.1:8765` — kéo thả file, bấm nút, tải báo cáo.

## Lưu ý bảo mật
`contracts/`, `reports/` và file luật **không được commit** (xem `.gitignore`) —
hợp đồng là tài liệu mật, mỗi máy tự nạp dữ liệu riêng.

> ⚠️ AI hỗ trợ review, không thay thế tư vấn pháp lý. Verify finding quan trọng
> trước khi sử dụng.
