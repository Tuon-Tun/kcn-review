# Bản đồ kho văn bản luật — kcn-review

> Cập nhật: 2026-06-18 · **67 văn bản / 18 nhóm** · Nguồn sự thật về hiệu lực: `laws/metadata.csv`
> Dành cho team legal: xem quan hệ thay thế/sửa đổi/hướng dẫn trước khi review và khi bổ sung văn bản mới.
> Chú giải: 🟢 đang hiệu lực · 🟡 hiệu lực một phần / bị sửa đổi · 🔴 hết hiệu lực (giữ cho HĐ cũ) · ✏️ văn bản sửa đổi · ⏳ ban hành nhưng hiệu lực trong tương lai

## 1. Thống kê nhanh

| Nhóm | Số VB | Đang hiệu lực | Hết hiệu lực | Ghi chú |
|---|---|---|---|---|
| dat-dai | 9 | 9 | 0 | đầy đủ nhất; + NĐ 96/2024 (hướng dẫn KD BĐS, kèm mẫu HĐ) |
| dau-tu | 10 | 9 | 1 (LĐT 2020) | + NĐ 96/2026 hướng dẫn LĐT 143/2025 (⏳ hiệu lực 01/7/2026) |
| moi-truong | 12 | 10 | 2 (PCCC cũ) | BVMT, PCCC mới, tài nguyên nước; PCCC cũ 136/2020+50/2024 cho HĐ trước 01/7/2025 |
| hai-quan | 5 | 5 | 0 | 🆕 EPE: Luật Hải quan, Thuế XNK, TT 38/39 |
| ngoai-hoi | 5 | 5 | 0 | 🆕 điều khoản giá USD; TT 32/2013 hạn chế ngoại tệ |
| xay-dung | 4 | 4 | 0 | 🆕 Luật XD 2025 (⏳) + 3 NĐ |
| dan-su | 4 | 4 | 0 | nền chung + trọng tài |
| dau-thau | 2 | 2 | 0 | 🆕 Luật Đấu thầu + chọn nhà đầu tư |
| doanh-nghiep | 2 | 2 | 0 | 🆕 Luật DN 2020 + sửa 2025 |
| quy-hoach | 3 | 2 | 1 | 🆕 Luật QH 2017 + Luật QH đô thị-NT 47/2024; bản 2009 hết hiệu lực |
| da-nang | 3 | 3 | 0 | cơ chế đặc thù + Khu TMTD |
| thue | 1 | 1 | 0 | 🆕 Luật Thuế GTGT 2024 |
| kcn | 2 | 1 | 1 (NĐ 82) | NĐ 35 đang chờ NĐ thay thế (dự thảo) |
| lao-dong | 2 | 2 | 0 | BLLĐ + 🆕 Luật Công đoàn |
| dien-luc | 1 | 1 | 0 | 🆕 Luật Điện lực 2024 |
| lam-nghiep | 1 | 1 | 0 | 🆕 Hòa Ninh có chuyển mục đích đất rừng |
| thuong-mai | 1 | 1 | 0 | 🆕 Luật Thương mại 2005 |
| ho-chi-minh | 1 | 1 | 0 | dùng đối chiếu |

**Lưu ý ⏳ hiệu lực tương lai (tại 18/06/2026 chưa có hiệu lực):** Luật Xây dựng 2025,
NĐ 96/2026 (hướng dẫn LĐT), NĐ 206/2026 — đều 01/07/2026. HĐ ký TRƯỚC mốc này vẫn
áp dụng văn bản cũ (triage tự xử theo ngày ký).

**✅ GAP đã lấp (18/06):** Luật Quy hoạch đô thị & nông thôn 47/2024/QH15 (hiệu lực
01/07/2025, thay Luật QH đô thị 2009) đã có trong kho (quy-hoach/LQHDTNT-2024).

## 2. Sơ đồ quan hệ (GitHub tự render)

```mermaid
flowchart TB
  classDef active fill:#e8f5e9,stroke:#2e7d32
  classDef partial fill:#fff8e1,stroke:#f9a825
  classDef expired fill:#ffebee,stroke:#c62828
  classDef amend fill:#e3f2fd,stroke:#1565c0

  subgraph KCN["🏭 KCN / KKT"]
    ND82["🔴 NĐ 82/2018<br/>(HĐ ký trước 15/07/2022)"]:::expired
    ND35["🟢 NĐ 35/2022<br/>quản lý KCN-KKT"]:::active
    ND82 -- "bị thay thế bởi" --> ND35
  end

  subgraph DAUTU["💰 Đầu tư & Thuế"]
    LDT2020["🔴 Luật Đầu tư 2020<br/>(HĐ ký trước 01/03/2026)"]:::expired
    LDT2025["🟢 Luật Đầu tư 143/2025"]:::active
    ND31["🟡 NĐ 31/2021<br/>hướng dẫn LĐT"]:::partial
    ND239["✏️ NĐ 239/2025"]:::amend
    QD29["🟢 QĐ 29/2021<br/>ưu đãi đặc biệt"]:::active
    ND182["🟢 NĐ 182/2024<br/>Quỹ Hỗ trợ đầu tư"]:::active
    NQ107["🟢 NQ 107/2023<br/>thuế tối thiểu 15%"]:::active
    ND236["🟢 NĐ 236/2025"]:::active
    TNDN["🟢 Luật Thuế TNDN 67/2025"]:::active
    LDT2020 -- "bị thay thế bởi" --> LDT2025
    LDT2020 -. "hướng dẫn" .- ND31
    ND239 -- "sửa đổi" --> ND31
    ND31 -. "căn cứ" .- QD29
    NQ107 -. "hướng dẫn" .- ND236
    NQ107 == "trung hòa ưu đãi thuế suất<br/>→ chuyển sang hỗ trợ chi phí" ==> ND182
    TNDN -. "nền ưu đãi thuế" .- QD29
  end

  subgraph DATDAI["🌍 Đất đai & KD BĐS"]
    LDD["🟢 Luật Đất đai 2024"]:::active
    ND102["🟢 NĐ 102/2024"]:::active
    ND103["🟡 NĐ 103/2024<br/>tiền thuê đất"]:::partial
    ND291["✏️ NĐ 291/2025"]:::amend
    ND151["🟢 NĐ 151/2025<br/>phân quyền 2 cấp<br/>(đến 28/02/2027)"]:::active
    ND226["✏️ NĐ 226/2025"]:::amend
    NQ254["🟢 NQ 254/2025<br/>gỡ vướng thi hành"]:::active
    KDBDS["🟢 Luật KD BĐS 2023<br/>cho thuê lại QSDĐ"]:::active
    LDD -. "hướng dẫn" .- ND102
    LDD -. "hướng dẫn" .- ND103
    ND291 -- "sửa đổi" --> ND103
    ND226 -- "sửa đổi" --> ND151
    LDD -. "gỡ vướng" .- NQ254
    LDD <-. "cho thuê lại trong dự án" .-> KDBDS
  end

  subgraph MOITRUONG["🌿 Môi trường & PCCC"]
    BVMT["🟡 Luật BVMT 2020"]:::partial
    L146["✏️ Luật 146/2025<br/>sửa 15 luật NN-MT"]:::amend
    ND08["🟡 NĐ 08/2022<br/>giấy phép MT, đấu nối<br/>(+ bộ phụ lục)"]:::partial
    ND05["✏️ NĐ 05/2025"]:::amend
    ND48["✏️ NĐ 48/2026"]:::amend
    PCCC["🟢 Luật PCCC&CNCH 55/2024<br/>(thay luật 2001)"]:::active
    ND105["🟢 NĐ 105/2025"]:::active
    L146 -- "sửa đổi" --> BVMT
    BVMT -. "hướng dẫn" .- ND08
    ND05 -- "sửa đổi lần 1" --> ND08
    ND48 -- "sửa đổi lần 2" --> ND08
    PCCC -. "hướng dẫn" .- ND105
  end

  subgraph DANSU["⚖️ Dân sự & Tranh chấp"]
    BLDS["🟢 BLDS 2015<br/>(Đ.683: luật áp dụng BĐS)"]:::active
    TTTM["🟡 Luật Trọng tài TM 2010<br/>(sửa nhẹ bởi L81/2025)"]:::partial
    LBH["🟡 Luật BH VBQPPL 64/2025"]:::partial
    L87["✏️ Luật 87/2025"]:::amend
    L87 -- "sửa đổi" --> LBH
  end

  subgraph DIAPHUONG["📍 Địa phương"]
    NQ136["🟡 NQ 136/2024<br/>đặc thù Đà Nẵng"]:::partial
    NQ259["✏️ NQ 259/2025"]:::amend
    QD1142["🟢 QĐ 1142/QĐ-TTg<br/>Khu TMTD Đà Nẵng 1.881ha"]:::active
    NQ98["🟢 NQ 98/2023<br/>đặc thù TP.HCM (đối chiếu)"]:::active
    NQ259 -- "sửa đổi" --> NQ136
    NQ136 -. "thực hiện" .- QD1142
  end

  subgraph LAODONG["👷 Lao động"]
    BLLD["🟢 BLLĐ 2019"]:::active
  end

  LDT2025 -. "NĐ 31 chờ thay bằng<br/>NĐ hướng dẫn mới ⏳" .- ND31
  ND35 -. "Đ.61 NĐ31 về hạ tầng KCN" .- ND31
```

## 2b. Nhóm mới (batch 18/06/2026) — sơ đồ bổ sung

```mermaid
flowchart LR
  classDef active fill:#e8f5e9,stroke:#2e7d32
  classDef future fill:#ede7f6,stroke:#5e35b1
  classDef expired fill:#ffebee,stroke:#c62828

  subgraph NGOAIHOI["💱 ngoai-hoi (giá USD)"]
    PL["🟢 Pháp lệnh Ngoại hối<br/>(hợp nhất + gốc 2005)"]:::active
    TT32["🟢 TT 32/2013<br/>hạn chế dùng ngoại tệ"]:::active
    TT06["🟢 TT 06/2019 (FDI)"]:::active
    TT16["🟢 TT 16/2014 (TK ngoại tệ)"]:::active
  end
  subgraph HAIQUAN["🚢 hai-quan (EPE)"]
    LHQ["🟢 Luật Hải quan 2014"]:::active
    LTXNK["🟢 Luật Thuế XNK 2016"]:::active
    TT38["🟢 TT 38/2015"]:::active
    TT39["✏️ TT 39/2018 sửa 38"]:::active
    LTXNK -.->|hướng dẫn| TT38
    TT39 -->|sửa| TT38
  end
  subgraph XAYDUNG["🏗️ xay-dung"]
    LXD["⏳ Luật Xây dựng 2025<br/>(01/7/2026)"]:::future
    ND06["🟢 NĐ 06/2021 chất lượng"]:::active
    ND175["🟢 NĐ 175/2024 hoạt động XD"]:::active
    ND206["⏳ NĐ 206/2026 chi phí"]:::future
  end
  subgraph QUYHOACH["🗺️ quy-hoach"]
    LQH["🟢 Luật Quy hoạch 2017"]:::active
    LQHDT["🔴 Luật QH đô thị 2009<br/>(hết hiệu lực 01/7/2025)"]:::expired
    L47["🟢 Luật QH đô thị-NT 47/2024"]:::active
    LQHDT -->|đã thay bởi| L47
  end
  subgraph KHAC["Khác"]
    LDN["🟢 Luật Doanh nghiệp 2020 + sửa 76/2025"]:::active
    LDTHAU["🟢 Luật Đấu thầu 2023 + NĐ 23/2024"]:::active
    LDL["🟢 Luật Điện lực 2024"]:::active
    LLN["🟢 Luật Lâm nghiệp 2017"]:::active
    LTM["🟢 Luật Thương mại 2005"]:::active
    LGTGT["🟢 Luật Thuế GTGT 2024"]:::active
    LTNN["🟢 Luật Tài nguyên nước 2023"]:::active
    LCD["🟢 Luật Công đoàn 2024"]:::active
  end
```

## 3. Ánh xạ loại hợp đồng → nhóm luật (dùng khi triage)

| Loại HĐ | Nhóm bắt buộc | Nhóm mở rộng khi liên quan |
|---|---|---|
| Thuê đất / thuê lại đất | kcn, dat-dai | dau-tu, moi-truong, xay-dung, quy-hoach, (+ địa phương) |
| Thuê nhà xưởng | kcn, dan-su | dat-dai, moi-truong, xay-dung |
| Dịch vụ hạ tầng/tiện ích | kcn, dan-su | moi-truong, dien-luc |
| Gia công / dịch vụ SX | dan-su | lao-dong, dau-tu, hai-quan |
| Đấu thầu chọn nhà đầu tư | kcn, dau-thau | dat-dai, dau-tu |

**Quy tắc cắt ngang (theo nội dung điều khoản, mọi loại HĐ):**
| Điều khoản có... | Thêm nhóm |
|---|---|
| giá/phí ghi bằng ngoại tệ (USD...) | ngoai-hoi |
| bên thuê là EPE / có XNK | hai-quan |
| thuế GTGT, TNDN | thue, dau-tu |
| xây dựng/nghiệm thu công trình | xay-dung |
| chuyển mục đích đất rừng | lam-nghiep |
| tư cách pháp nhân/người ký | doanh-nghiep |
| trọng tài / luật áp dụng | dan-su (BLDS Đ.683, Luật TTTM) |
| nước thải/PCCC | moi-truong |

## 4. Điểm cần theo dõi (cập nhật khi có)

| # | Việc | Trạng thái 06/2026 |
|---|---|---|
| 1 | Nghị định **thay thế NĐ 35/2022** | Dự thảo đang lấy ý kiến (Bộ Tài chính) — khi ban hành: tải về, đặt NĐ 35 expiry + is_active=FALSE |
| 2 | ✅ Nghị định **hướng dẫn Luật Đầu tư 143/2025** | ĐÃ CÓ: NĐ 96/2026 (hiệu lực 01/7/2026) |
| 3 | ✅ **Luật Quy hoạch đô thị & nông thôn 47/2024** | ĐÃ CÓ (18/06): quy-hoach/LQHDTNT-2024, hiệu lực 01/7/2025 |
| 4 | Ngày hiệu lực một số NĐ lấy theo ngày ban hành | ND-23-2024, ND-175-2024 (ghi chú trong NGUON-GOC) — xác nhận khi cần dùng chính xác |
| 5 | Lớp **thông tư** cấp bộ | Đã có TT hải quan (38/39), ngoại hối (06/16/32); bổ sung tiếp theo vụ việc |

## 5. Quy trình bổ sung văn bản mới (cho team legal)

1. Tải .docx từ thuvienphapluat (kiểm tra ĐÚNG số hiệu + ngày ban hành trước khi tải — đã từng dính 2 file trùng số khác văn bản).
2. Đưa file cho agent convert (`scripts/doc_extract.py` cho .doc cũ) → vào `laws_staging/<nhóm>/` chờ duyệt.
3. Duyệt xong → agent chuyển vào `laws/<nhóm>/` + cập nhật `metadata.csv` (đủ cấp hiệu lực, ngày hiệu lực, thay_the_cho, is_active) + cập nhật sơ đồ này.
4. Văn bản hết hiệu lực KHÔNG xóa — đặt `is_active=FALSE` + `expiry_date` (phục vụ HĐ ký trong giai đoạn cũ).
