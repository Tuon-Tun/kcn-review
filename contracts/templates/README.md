# Mẫu hợp đồng chuẩn — Thanh Bình Phú Mỹ

Đây là nơi team Pháp chế **tải lên các hợp đồng MẪU CHUẨN** của công ty, dùng làm
dữ liệu đối chiếu khi review hợp đồng khách hàng gửi. Mục đích: **đảm bảo mọi hợp
đồng nhất quán với chuẩn công ty** — phát hiện nhanh điều khoản khách hàng sửa khác mẫu.

## Khác gì với các thư mục khác?
| Thư mục | Chứa gì | Có lên GitHub? |
|---|---|---|
| `contracts/templates/` (đây) | MẪU CHUẨN của công ty — dùng chung | ✅ CÓ (để cả team đối chiếu cùng 1 chuẩn) |
| `contracts/inbox/` | HĐ thật cần review | ❌ tài liệu mật |
| `contracts/done/` | HĐ thật đã review xong | ❌ tài liệu mật |

## Cách tải mẫu lên (cho team legal)
1. Đặt file mẫu (.docx/.pdf) vào đúng thư mục loại HĐ:
   - `thue-lai-dat/` — thuê / thuê lại đất gắn hạ tầng
   - `thue-nha-xuong/` — thuê nhà xưởng xây sẵn
   - `dich-vu-ha-tang/` — dịch vụ hạ tầng / tiện ích
   - (thêm thư mục loại HĐ mới nếu cần)
2. Khai báo vào `index.csv` một dòng: loại HĐ, tên mẫu, đường dẫn file, phiên bản,
   ngày cập nhật, người duyệt mẫu, ghi chú.
3. Khi có phiên bản mới của một mẫu → cập nhật file + tăng `phien_ban` + `ngay_cap_nhat`
   (giữ lịch sử qua git, không tạo bản trùng).

## Dùng để làm gì?
- Web app → nút **📋 Đối chiếu với mẫu chuẩn**: tải HĐ khách hàng lên `inbox/`,
  tool tự tìm mẫu khớp loại HĐ trong `index.csv` và chỉ ra:
  - 🔴 điều khoản khách hàng sửa BẤT LỢI cho công ty (giá, thời hạn, trách nhiệm...)
  - 🟡 điều khoản BẢO VỆ trong mẫu bị khách hàng LƯỢC BỎ / làm yếu
  - 🟢 thay đổi khác nhưng không bất lợi
- Quy trình chạy bằng skill `template-compare`.

## Lưu ý
- Đối chiếu MẪU **khác** đối chiếu LUẬT (skill legal-review). Lệch mẫu KHÔNG có
  nghĩa trái luật — chỉ là khác chuẩn công ty. Vấn đề pháp lý vẫn phải review luật.
- Mẫu phải là bản đã được Pháp chế DUYỆT là "chuẩn công ty" — không để bản nháp lẫn vào.
