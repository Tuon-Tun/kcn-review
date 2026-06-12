# Rà soát hiệu lực kho luật — 2026-06-12

Kết quả dò chéo header vbpl trong file đã tải + tra cứu văn bản sửa đổi/thay thế
đến tháng 6/2026. ⚠️ = ảnh hưởng trực tiếp đến review hợp đồng / tư vấn ưu đãi.

## ⚠️ PHÁT HIỆN LỚN — văn bản trong kho đã bị thay thế/sửa đổi

| Văn bản trong kho | Tình trạng | Văn bản mới | Kho đã có? |
|---|---|---|---|
| Luật Đầu tư 2020 (LDT-2020) | **HẾT HIỆU LỰC TOÀN BỘ từ 01/03/2026** | **Luật Đầu tư số 143/2025/QH15** (11/12/2025; 7 chương 52 Điều; riêng danh mục ngành nghề KD có điều kiện hiệu lực 01/07/2026) | **CHƯA — cần tải gấp** |
| Luật BVMT 2020 (BVMT-2020) | Hết hiệu lực MỘT PHẦN | Sửa bởi các Luật 11/2022, 16/2023, 18/2023, 47/2024, 54/2024 và **Luật 146/2025/QH15** (sửa 15 luật nông nghiệp–môi trường, hiệu lực 01/01/2026) | Chưa có Luật 146/2025 |
| NĐ 31/2021 (ND-31-2021) | Hết hiệu lực MỘT PHẦN | NĐ 239/2025 (✓ đã có). Lưu ý: Luật Đầu tư mới có hiệu lực → chờ nghị định hướng dẫn MỚI thay NĐ 31 | Theo dõi |
| Luật BH VBQPPL 2025 (LBH-2025) | Đã bị sửa đổi | **Luật 87/2025/QH15** (sửa đổi giữa 2025 — phục vụ chính quyền 2 cấp) | Chưa có |
| Luật Thuế TNDN 2008 (KHÔNG có trong kho nhưng là nền của ưu đãi thuế) | Hết hiệu lực | **Luật Thuế TNDN số 67/2025/QH15** (14/6/2025, hiệu lực 01/10/2025, áp dụng từ kỳ tính thuế 2025) — phân tầng 20%/17%/15%, điều chỉnh danh mục ngành ưu đãi Điều 12 | **CHƯA — quan trọng cho marketing ưu đãi** |

## Văn bản còn hiệu lực nguyên vẹn (xác nhận đến 6/2026)
- NĐ 35/2022 (KCN/KKT): còn hiệu lực, **nhưng Bộ Tài chính đang lấy ý kiến DỰ THẢO
  nghị định thay thế** — theo dõi mof.gov.vn, khi ban hành phải cập nhật ngay.
- Luật Đất đai 2024 + NĐ 102/2024 + NĐ 103/2024 (đã có bản sửa NĐ 291/2025 ✓)
  + NQ 254/2025 gỡ vướng ✓ — bộ đất đai đang đầy đủ.
- BLDS 2015, BLLĐ 2019: còn hiệu lực.
- NQ 136/2024 + NQ 259/2025 (Đà Nẵng) ✓, NQ 98/2023 (TP.HCM) ✓, QĐ 29/2021 ✓,
  NĐ 182/2024 ✓.

## ⚠️ Tác động hệ thống: sắp xếp hành chính 2025 (hiệu lực 01/07/2025)
- NQ 202/2025/QH15: sáp nhập đơn vị hành chính cấp tỉnh — **Đà Nẵng hợp nhất với
  Quảng Nam**; TP.HCM hợp nhất với Bình Dương, Bà Rịa-Vũng Tàu. Chính quyền 2 cấp,
  **bỏ cấp huyện**.
- Hệ quả cho dự án: địa danh "huyện Hòa Vang" trong hồ sơ KCN Hòa Ninh không còn
  cấp hành chính tương ứng (nay là xã trực thuộc TP); địa bàn ưu đãi đầu tư xác
  định theo CẤP XÃ (NĐ 239/2025 đã sửa Điều 21 NĐ 31 cho việc này); hồ sơ so sánh
  TP.HCM giờ bao trùm cả các KCN Bình Dương + BR-VT (lợi thế cạnh tranh thay đổi).
- HĐ ký trước/sau 01/07/2025 ghi tên đơn vị hành chính khác nhau → khi review chú ý
  điều khoản địa danh, thẩm quyền cơ quan.

## Nguyên tắc temporal (nhắc lại — đã có trong CLAUDE.md)
Văn bản hết hiệu lực KHÔNG xóa khỏi kho: HĐ ký trong thời gian văn bản còn hiệu lực
vẫn đối chiếu theo văn bản đó, kèm cờ "đã thay đổi — kiểm tra quy định hiện hành
trước khi đàm phán". Vd: HĐ ký 02/2026 → vẫn dùng Luật Đầu tư 2020.

## Việc cần làm
1. Người dùng tải 4 file .docx (kiểu thuvienphapluat như các lần trước):
   Luật Đầu tư 143/2025/QH15 · Luật Thuế TNDN 67/2025/QH15 ·
   Luật 146/2025/QH15 (sửa 15 luật NN-MT) · Luật 87/2025/QH15 (sửa Luật BH VBQPPL)
2. Khi duyệt kho: cập nhật metadata.csv — LDT-2020 expiry_date=2026-03-01,
   is_active=FALSE; thêm các văn bản mới với nhom tương ứng.
3. Soát lại research/da-nang/* theo địa giới hành chính mới.
4. Theo dõi: nghị định thay NĐ 35/2022 (dự thảo), nghị định hướng dẫn Luật Đầu tư 143/2025.
