# -*- coding: utf-8 -*-
"""
Kiểm tra TOÀN VẸN kho luật — chạy bất cứ lúc nào để giữ pipeline nhất quán:
  python scripts/audit_kho.py

Đối chiếu 3 nguồn phải khớp nhau:
  (1) file .txt thật trong laws/<nhóm>/
  (2) dòng trong laws/metadata.csv   (hiệu lực — engine dùng khi triage)
  (3) dòng trong laws/NGUON-GOC-VAN-BAN.csv  (nguồn gốc — audit)

Báo lỗi nếu: file thiếu metadata, metadata trỏ file không tồn tại, sai thư mục
nhóm, thiếu nguồn gốc, hoặc trùng doc_code. Exit 0 = sạch, 1 = có vấn đề.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAWS = ROOT / "laws"


def load_csv(name, key="doc_code"):
    rows = {}
    p = LAWS / name
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            code = (r.get(key) or "").strip()
            if code:
                rows[code] = r
    return rows


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # (1) file thật: doc_code -> nhóm
    files = {}
    dup_file = []
    for f in LAWS.rglob("*.txt"):
        code = f.stem
        if code in files:
            dup_file.append(code)
        files[code] = f.parent.name

    meta = load_csv("metadata.csv")
    nguon = load_csv("NGUON-GOC-VAN-BAN.csv")

    problems = []

    # file <-> metadata
    for code, nhom in files.items():
        if code not in meta:
            problems.append(f"[THIẾU METADATA] {nhom}/{code}.txt không có dòng trong metadata.csv")
        elif meta[code].get("nhom", "").strip() != nhom:
            problems.append(f"[SAI NHÓM] {code}: file ở '{nhom}' nhưng metadata ghi '{meta[code].get('nhom')}'")
        if code not in nguon:
            problems.append(f"[THIẾU NGUỒN GỐC] {code} không có trong NGUON-GOC-VAN-BAN.csv")
    for code in meta:
        if code not in files:
            problems.append(f"[METADATA MỒ CÔI] metadata có {code} nhưng không có file .txt")
    for code in dup_file:
        problems.append(f"[TRÙNG doc_code] {code} xuất hiện ở nhiều thư mục")

    # kiểm tra ngày hiệu lực hợp lệ + cờ is_active
    for code, r in meta.items():
        eff = (r.get("effective_date") or "").strip()
        if eff and not (len(eff) == 10 and eff[4] == "-"):
            problems.append(f"[NGÀY LỖI] {code}: effective_date='{eff}' không đúng YYYY-MM-DD")
        act = (r.get("is_active") or "").strip().upper()
        if act not in ("TRUE", "FALSE"):
            problems.append(f"[is_active LỖI] {code}: '{act}'")

    # thống kê theo nhóm
    from collections import Counter
    by_nhom = Counter(files.values())
    active = sum(1 for r in meta.values() if r.get("is_active", "").upper() == "TRUE")

    print(f"Kho: {len(files)} file .txt | metadata {len(meta)} dòng | nguồn gốc {len(nguon)} dòng")
    print(f"Đang hiệu lực: {active} | hết hiệu lực: {len(meta) - active} | nhóm: {len(by_nhom)}")
    print("Theo nhóm:", dict(sorted(by_nhom.items())))
    if problems:
        print(f"\n❌ {len(problems)} VẤN ĐỀ:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\n✅ KHO NHẤT QUÁN: file ↔ metadata ↔ nguồn gốc khớp hoàn toàn.")


if __name__ == "__main__":
    main()
