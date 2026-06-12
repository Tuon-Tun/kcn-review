---
name: legal-translate
description: Dịch hợp đồng/văn bản pháp lý VI↔EN có ràng buộc thuật ngữ. Dùng khi
  người dùng yêu cầu dịch một file trong contracts/.
---
# Dịch pháp lý có termbase
1. Đọc termbase/termbase.csv. Mọi term xuất hiện trong văn bản nguồn PHẢI dịch
   đúng cột en_chuan (hoặc vi khi dịch ngược). Không tự ý đổi.
2. Giữ nguyên: số Điều/Khoản, con số, ngày tháng, tên riêng. Văn phong pháp lý.
3. Term pháp lý CHƯA có trong termbase → liệt kê cuối bản dịch, mục
   "TERM CẦN BỔ SUNG" (kèm gợi ý bản dịch để người dùng duyệt vào CSV).
4. Dòng đầu mọi bản dịch: "BẢN DỊCH THAM KHẢO — CHƯA CÓ GIÁ TRỊ PHÁP LÝ".
5. Xuất .docx vào reports/, tên <tên-gốc>_translated.docx.
