---
name: template-compare
description: Đối chiếu hợp đồng khách hàng gửi với MẪU CHUẨN của công ty trong
  contracts/templates/ — phát hiện điều khoản lệch chuẩn, thiếu điều khoản bảo vệ,
  thay đổi bất lợi cho bên cho thuê. Dùng khi cần kiểm tra HĐ có nhất quán với mẫu công ty.
---

# Đối chiếu hợp đồng với mẫu chuẩn công ty (góc nhìn bên cho thuê - Thanh Bình Phú Mỹ)

## Bước 1 — Xác định mẫu chuẩn
- Đọc HĐ đến (trong contracts/inbox/): xác định LOẠI HĐ.
- Tra contracts/templates/index.csv → tìm mẫu khớp `loai_hd`; lấy file + phiên bản.
- KHÔNG có mẫu khớp → dừng, báo "CHƯA CÓ MẪU CHUẨN cho loại HĐ <X> trong
  contracts/templates/" + đề xuất team tạo mẫu. KHÔNG tự bịa mẫu.

## Bước 2 — Align điều khoản
- Map từng Điều của HĐ đến ↔ Điều tương ứng trong mẫu THEO NỘI DUNG/tiêu đề,
  không chỉ theo số thứ tự (khách hàng có thể đánh số lại).
- Điều chỉ có ở MỘT bên → đánh dấu để xét ở Bước 3.

## Bước 3 — Phát hiện 3 loại lệch (so với mẫu, đứng về phía công ty cho thuê)
- 🔴 ĐỎ — thay đổi BẤT LỢI ở điều khoản then chốt: giá thuê/phí, thời hạn, lãi
  chậm trả, điều chỉnh giá, giới hạn/miễn trừ trách nhiệm của công ty, điều kiện
  chấm dứt & thu hồi, chuyển nhượng/cho thuê lại, phạt vi phạm, bảo đảm/đặt cọc.
- 🟡 VÀNG — điều khoản BẢO VỆ công ty có trong mẫu nhưng bị LƯỢC BỎ hoặc làm yếu
  trong HĐ đến (vd: bỏ quyền kiểm tra môi trường, bỏ điều khoản ngôn ngữ ưu tiên).
- 🟢 XANH — điều khoản mới/diễn đạt khác nhưng KHÔNG bất lợi.
- Với mỗi finding ĐỎ/VÀNG: nêu rõ VÌ SAO bất lợi cho bên cho thuê + trích đoạn
  mẫu và đoạn HĐ đến để so sánh.

## Bước 4 — Báo cáo
- Bảng: Điều | Mẫu chuẩn (trích) | HĐ đến (trích) | Loại lệch | Mức | Khuyến nghị
  (giữ nguyên mẫu / chấp nhận / đàm phán lại).
- Tóm tắt đầu báo cáo: mẫu đối chiếu (tên + phiên bản), số lệch đỏ/vàng/xanh,
  mức độ "xa rời chuẩn" tổng thể.
- Xuất reports/YYYY-MM-DD_<tên-HĐ>_doichieu-mau.docx (python-docx, Arial); nếu
  trùng tên trong ngày thêm hậu tố _HHMM.

## Ranh giới (quan trọng — không nhầm vai)
- Đối chiếu MẪU = nhất quán với CHUẨN CÔNG TY; KHÁC đối chiếu LUẬT (legal-review).
- Lệch mẫu KHÔNG đồng nghĩa trái luật; ngược lại, đúng mẫu KHÔNG đồng nghĩa hợp pháp
  (mẫu cũng có thể lỗi thời so với luật). → Với HĐ quan trọng, chạy CẢ legal-review.
- KHÔNG kiểm chứng trích dẫn luật ở skill này (không có finding luật); chỉ so văn bản.
