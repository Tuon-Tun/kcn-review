---
name: law-fetch
description: Tự tìm, tải văn bản luật từ nguồn chính thống, convert sang .txt và xếp
  vào khu chờ duyệt laws_staging/ theo nhóm. Dùng khi người dùng yêu cầu tải/bổ sung/
  cập nhật văn bản luật. KHÔNG BAO GIỜ ghi trực tiếp vào laws/.
---

# Tải văn bản luật vào khu chờ duyệt

## Nguyên tắc bất di bất dịch
- CHỈ ghi vào `laws_staging/<nhóm>/` — TUYỆT ĐỐI không ghi/sửa gì trong `laws/`.
  Người dùng duyệt xong mới tự chuyển sang `laws/<nhóm>/` (hoặc ra lệnh chuyển
  sau khi xác nhận từng file).
- Nguồn ưu tiên theo thứ tự: (1) vbpl.vn (CSDL quốc gia về VBQPPL — chính thống),
  (2) congbao.chinhphu.vn / datafiles.chinhphu.vn, (3) cổng thông tin bộ ngành.
  KHÔNG dùng bản tổng hợp của blog/trang tin không chính thống.
- Luôn lấy đúng số hiệu văn bản (vd 31/2024/QH15) — tên gần giống không tính.

## Quy trình
1. Xác định danh sách cần tải:
   - Người dùng nêu cụ thể → dùng danh sách đó.
   - Người dùng nói "tải các luật còn thiếu" → đọc laws/metadata.csv, tìm các
     doc_code chưa có file .txt tương ứng trong laws/.
2. Với từng văn bản: tìm trên nguồn chính thống (WebSearch), mở trang toàn văn
   (WebFetch), lấy TOÀN VĂN — không lấy bản tóm tắt/trích.
3. Convert sang .txt thuần (UTF-8): giữ nguyên cấu trúc "Điều N." đầu dòng,
   bỏ HTML/menu/quảng cáo, giữ nguyên chính tả gốc (KHÔNG sửa chữ — sửa là
   hỏng khớp chuỗi kiểm chứng).
4. Lưu: `laws_staging/<nhóm>/<doc_code>.txt` — nhóm lấy theo cột `nhom` trong
   metadata.csv (kcn / dat-dai / dau-tu / moi-truong / lao-dong / dan-su);
   văn bản mới chưa có trong metadata → tự xếp nhóm hợp lý nhất và ghi rõ.
5. Ghi/cập nhật `laws_staging/metadata_draft.csv` (cùng cột với laws/metadata.csv
   + cột `nguon_url`, `ngay_tai`): mỗi file đã tải một dòng, kèm URL nguồn.
6. Báo cáo cuối: bảng từng văn bản — tải được/không, nguồn, nhóm, số Điều đếm
   được trong file (sanity check: Luật lớn mà file chỉ có vài Điều = tải thiếu,
   đánh dấu ⚠️). Nhắc người dùng: "Duyệt xong, ra lệnh 'duyệt file X' để chuyển
   vào laws/ và cập nhật metadata.csv chính thức."

## Khi người dùng ra lệnh duyệt ("duyệt file X" / "duyệt tất cả")
- Chuyển file từ laws_staging/<nhóm>/ sang laws/<nhóm>/ (đây là lệnh trực tiếp
  của người dùng nên được phép ghi vào laws/).
- Gộp dòng tương ứng từ metadata_draft.csv vào laws/metadata.csv (bỏ 2 cột phụ).
- LƯU HỒ SƠ NGUỒN GỐC: gộp các dòng đã duyệt (kèm nguon_url) vào
  laws/NGUON-GOC-VAN-BAN.csv rồi xóa khỏi metadata_draft.csv.
- Xoá file đã duyệt khỏi staging; KIỂM TRA LẠI staging phải sạch (không còn .txt
  của văn bản đã duyệt) — nếu dùng push_via_api.ps1 thì xác nhận cả trên remote.
- Cập nhật laws/SO-DO-VAN-BAN.md (thống kê + bảng quan hệ mục 2) cho văn bản mới.
- CHẠY `python scripts/audit_kho.py` — phải báo "✅ KHO NHẤT QUÁN" trước khi
  coi là xong (bắt file lệch tên / thiếu metadata / mồ côi). Đặt doc_code = tên
  file (không dấu, dùng gạch nối) để audit khớp.
