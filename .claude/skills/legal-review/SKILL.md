---
name: legal-review
description: Quy trình review hợp đồng KCN 4 bước có kiểm chứng trích dẫn. Dùng khi
  người dùng yêu cầu review/đánh giá/phân tích hợp đồng trong contracts/inbox/.
---

# Quy trình review hợp đồng KCN

## Bước 1 — TRIAGE (khoanh vùng)
- Đọc lướt HĐ (chỉ trang đầu + mục lục/tiêu đề Điều): loại HĐ, ngôn ngữ, NGÀY KÝ
  (hỏi người dùng nếu không rõ).
- DETECT loại HĐ → ánh xạ sang nhóm luật (cột `nhom` trong laws/metadata.csv):
  | Loại HĐ                  | Nhóm luật bắt buộc      | Nhóm thêm khi HĐ có nội dung liên quan |
  |--------------------------|-------------------------|----------------------------------------|
  | Thuê đất / thuê lại đất  | kcn, dat-dai            | dau-tu, moi-truong, xay-dung, quy-hoach|
  | Thuê nhà xưởng           | kcn, dan-su             | dat-dai, moi-truong, xay-dung          |
  | Dịch vụ hạ tầng/tiện ích | kcn, dan-su             | moi-truong, dien-luc                   |
  | Gia công / dịch vụ SX    | dan-su                  | lao-dong, dau-tu, hai-quan             |
  | Đấu thầu chọn nhà đầu tư | kcn, dau-thau           | dat-dai, dau-tu                        |
  CHỈ grep/đọc file trong các thư mục laws/<nhóm> đã chọn — file ngoài nhóm coi
  như không tồn tại ở bước này (tiết kiệm token).
  + Quy tắc CẮT NGANG (thêm nhóm theo NỘI DUNG điều khoản, bất kể loại HĐ):
    - giá/phí ghi bằng ngoại tệ (USD, EUR...) → + ngoai-hoi
    - bên thuê là doanh nghiệp chế xuất (EPE) / có xuất nhập khẩu → + hai-quan
    - có điều khoản thuế (GTGT, TNDN) → + thue, dau-tu
    - có xây dựng/nghiệm thu công trình trên đất → + xay-dung
    - chuyển mục đích đất rừng → + lam-nghiep
    - tư cách pháp nhân/người ký → + doanh-nghiep
    - điều khoản trọng tài/luật áp dụng → + dan-su (BLDS Đ.683, Luật Trọng tài TM)
  + Nhóm ĐỊA PHƯƠNG: HĐ thuộc địa bàn có cơ chế đặc thù (da-nang, ho-chi-minh...)
  → thêm nhóm địa phương đó vào phạm vi (NQ đặc thù có thể cho ưu đãi khác luật chung). Gặp dẫn chiếu chéo sang văn bản
  ngoài nhóm ở B2 thì mới mở rộng, và ghi rõ lý do mở rộng.
- Lọc tiếp theo metadata.csv lấy văn bản có hiệu lực tại ngày ký; chọn CHỈ những văn bản
  thực sự liên quan loại HĐ này (HĐ dịch vụ hạ tầng đơn giản không cần Luật Đất
  đai/Lao động). Ghi rõ: dùng gì, loại gì, vì sao.
- Văn bản dùng cho ngày ký nhưng nay is_active=FALSE → ghi chú cờ "đã thay đổi".
- HĐ ký TRƯỚC 01/07/2025 (sắp xếp hành chính: sáp nhập tỉnh, bỏ cấp huyện) →
  BẮT BUỘC kiểm tra điều khoản địa danh + thẩm quyền cơ quan nhà nước được dẫn
  trong HĐ (vd "UBND huyện X" không còn tồn tại — thẩm quyền đất đai đã chuyển
  theo NĐ 151/2025); HĐ ký SAU mốc này mà vẫn ghi địa danh/cơ quan cũ → finding.
- Liệt kê điều khoản: ưu tiên (rủi ro tiềm ẩn theo CLAUDE.md) / bỏ qua (định nghĩa,
  thủ tục thuần).

## Bước 2 — PHÂN TÍCH (chỉ điều khoản ưu tiên, chỉ Điều luật liên quan)
Với từng điều khoản ưu tiên:
- Trích nguyên văn điều khoản HĐ.
- Grep từ khoá/số Điều trong các file luật đã khoanh vùng → CHỈ đọc các Điều khớp.
  KHÔNG đọc nguyên cả file luật dài.
- Gặp dẫn chiếu chéo → tra tiếp theo quy tắc trong CLAUDE.md, ghi chuỗi dẫn chiếu.
- Hai văn bản cho kết quả khác nhau → áp quy tắc xung đột (CLAUDE.md); không tự
  quyết được → chuyển "CẦN NGƯỜI XEM".
- Mỗi finding: mức ĐỎ/VÀNG/XANH + vấn đề + trích NGUYÊN VĂN đoạn luật (tên file,
  Điều/Khoản) + đề xuất sửa theo hướng bảo vệ KCN.
- Không có căn cứ → "KHÔNG TÌM THẤY CƠ SỞ PHÁP LÝ TRONG laws/".

## Bước 3 — KIỂM CHỨNG MÁY (bắt buộc, không bỏ qua)
- Xuất findings ra JSON tạm → chạy: python scripts/verify_citation.py
- Script đối chiếu TỪNG quoted_law_text với nội dung thật trong laws/**/*.txt
  (quét đệ quy mọi thư mục nhóm)
  (chuẩn hoá khoảng trắng rồi khớp chuỗi). FAIL → loại finding, ghi vào
  "Đã loại do không xác minh được".
- Script chưa tồn tại → viết nó trước (kèm self-test bắt được trích dẫn bịa),
  rồi mới tiếp tục.

## Bước 4 — BÁO CÁO
Tạo reports/YYYY-MM-DD_<tên-HĐ>.docx (python-docx, font Arial); nếu file đã tồn
tại (review lại trong ngày) thì thêm hậu tố _HHMM để không ghi đè. Gồm:
1. Tóm tắt: loại HĐ, ngày ký, điểm rủi ro tổng, số finding đỏ/vàng/xanh.
2. Phạm vi triage: luật đã dùng / đã loại / cờ hiệu lực — minh bạch phạm vi đọc.
3. Chi tiết finding: điều khoản → vấn đề → căn cứ nguyên văn (+ chuỗi dẫn chiếu
   nếu có) → đề xuất.
4. "CẦN NGƯỜI XEM": finding bị loại ở B3, xung đột chưa phân định, thiếu căn cứ.
5. Chân trang: "AI hỗ trợ review, không thay thế tư vấn pháp lý. Verify finding
   quan trọng bằng NotebookLM trước khi sử dụng."
Sau đó: cập nhật reports/index.csv (ngày, tên HĐ, loại, điểm, số đỏ/vàng, đường dẫn);
chuyển HĐ sang contracts/done/; nếu MCP Google Drive đã cấu hình → upload báo cáo
lên "KCN-Tool/Reports/<tháng>"; in tóm tắt 5 dòng.
