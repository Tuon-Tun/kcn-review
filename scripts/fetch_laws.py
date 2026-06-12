# -*- coding: utf-8 -*-
"""
Tải văn bản luật từ nguồn chính thống về laws_staging/<nhóm>/ (khu chờ duyệt).
KHÔNG ghi vào laws/ — người dùng duyệt xong mới chuyển (skill law-fetch).

Nguồn:
- xdcs    : trang toàn văn HTML trên xaydungchinhsach.chinhphu.vn
- vanban  : trang văn bản trên vanban.chinhphu.vn -> tải file đính kèm (.pdf) -> convert
Chạy: python scripts/fetch_laws.py
"""
import csv
import io
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / "laws_staging"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

# doc_code -> (nhóm, kiểu nguồn, url hoặc docid)
# Kiểu nguồn: xdcs = HTML xaydungchinhsach.chinhphu.vn; vbpl = HTML toàn văn
# vbpl.moj.gov.vn (vbpl.vn chặn bot, mirror Bộ Tư pháp thì không); pdf = PDF trực tiếp
# (Công báo — bản sắp chữ, KHÔNG dùng PDF scan của vanban.chinhphu.vn);
# vanban = trang vanban.chinhphu.vn -> file đính kèm (thường là scan, dễ rỗng).
SOURCES = {
    "LDD-2024":    ("dat-dai",    "xdcs", "https://xaydungchinhsach.chinhphu.vn/toan-van-luat-dat-dai-119240221224513596.htm"),
    "LBH-2025":    ("dan-su",     "xdcs", "https://xaydungchinhsach.chinhphu.vn/toan-van-luat-so-64-2025-qh15-ban-hanh-van-ban-quy-pham-phap-luat-119250311155839688.htm"),
    "ND-102-2024": ("dat-dai",    "xdcs", "https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-102-2024-nd-cp-quy-dinh-chi-tiet-thi-hanh-mot-so-dieu-cua-luat-dat-dai-119240815163801541.htm"),
    "ND-35-2022":  ("kcn",        "vbpl", "https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=158798"),
    "LDT-2020":    ("dau-tu",     "vbpl", "https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=142867"),
    "BLDS-2015":   ("dan-su",     "vbpl", "https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=95942"),
    "BVMT-2020":   ("moi-truong", "vbpl", "https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=146609"),
    "BLLD-2019":   ("lao-dong",   "pdf",  "https://g7.cdnchinhphu.vn/api/download/stream?Url=tm-8mq6BhNw0NbrKRhTDAQWsKg3tuqaY0aWypnY78U6M2BY68Ekp0Gvvr483flbR6FbDgxmjr7YP7l2i5iv9MsJqGQFD-xZbGNBK3JkpnvSGayQMVOIcKs55w61x8-tj_k9m4S7wnpbBrmQmSPUUoQ~~&file_name=2019_993+%2b+994_45-2019-QH14.pdf"),
    "ND-82-2018":  ("kcn",        "pdf",  "https://g7.cdnchinhphu.vn/api/download/stream?Url=tm-8mq6BhNw0NbrKRhTDAQWsKg3tuqaY0aWypnY78U6M2BY68Ekp0Gvvr483flbRHprCUdHZ1t6IxlBbbMyus0JQwTvP5HcPqbS9oC-fhD_aaT0X3Qm2QY9uD8CWL3FSoCmNV8xI0IqODd1kfORh3A~~&file_name=2018_683+%2b+684_82-2018-N%c4%90-CP.pdf"),
    # --- Đợt 2: ưu đãi đầu tư, công nghệ cao/bán dẫn, cơ chế đặc thù địa phương ---
    "ND-31-2021":  ("dau-tu",     "vbpl", "https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=147720"),
    "NQ-136-2024": ("da-nang",    "xdcs", "https://xaydungchinhsach.chinhphu.vn/nghi-quyet-136-2024-qh15-ve-to-chuc-chinh-quyen-do-thi-va-thi-diem-mot-so-co-che-chinh-sach-dac-thu-phat-trien-tp-da-nang-119240716154818818.htm"),
    "NQ-98-2023":  ("ho-chi-minh","xdcs", "https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-thi-diem-co-che-chinh-sach-dac-thu-phat-trien-tp-hcm-119230707074903999.htm"),
}

# CHỜ BỔ SUNG — chưa tìm được toàn văn dạng text trên nguồn chính thống
# (xdcs chỉ có trang tóm tắt; vanban.chinhphu.vn là PDF scan; vbpl chỉ có bản gốc scan).
# Hướng xử lý: tải .doc từ Công báo rồi convert thủ công, hoặc chờ vbpl cập nhật toàn văn.
#   ND-239-2025 : Sửa đổi NĐ 31/2021 (hướng dẫn Luật Đầu tư) — QUAN TRỌNG khi tư vấn ưu đãi
#   ND-182-2024 : Quỹ Hỗ trợ đầu tư (bán dẫn/AI/công nghệ cao)
#   ND-103-2024 : Tiền sử dụng đất, tiền thuê đất (miễn giảm) — vanban docid 210797 (scan)
#   QD-29-2021  : Ưu đãi đầu tư đặc biệt (miễn tiền thuê đất 18-22 năm)
#   NQ-259-2025 : Sửa đổi NQ 136/2024 (Đà Nẵng — thêm ưu đãi Khu TMTD, TOD)

DRAFT_COLS = ["doc_code", "nhom", "nguon_url", "ngay_tai", "so_dieu", "ghi_chu"]


def clean_text(text):
    # NFC bắt buộc: vbpl trả Unicode dạng tổ hợp (NFD) — không chuẩn hóa thì
    # verify_citation.py khớp chuỗi sẽ trượt dù trích dẫn đúng
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\xa0", " ").replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    # vbpl bọc số điều/chương trong thẻ riêng -> "Điều \n1." — nối lại
    text = re.sub(r"\b(Điều|Chương|Mục)\s*\n\s*([\dIVXLC])", r"\1 \2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_xdcs(url):
    """Trang toàn văn HTML: lấy khối nội dung dài nhất."""
    r = requests.get(url, timeout=60, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    candidates = soup.find_all(["article", "div"], class_=re.compile("content|detail|maincontent", re.I)) or [soup.body]
    best = max(candidates, key=lambda d: len(d.get_text()))
    return clean_text(best.get_text("\n")), url


def fetch_vbpl(url):
    """Trang toàn văn trên mirror vbpl.moj.gov.vn."""
    r = requests.get(url, timeout=120, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    div = soup.find("div", class_=re.compile("toanvancontent|fulltext", re.I))
    if div is None:
        candidates = soup.find_all("div", class_=re.compile("content", re.I)) or [soup.body]
        div = max(candidates, key=lambda d: len(d.get_text()))
    return clean_text(div.get_text("\n")), url


def fetch_pdf(url):
    """PDF sắp chữ (Công báo) -> text."""
    from pypdf import PdfReader
    try:
        r = requests.get(url, timeout=300, headers=HEADERS)
    except requests.exceptions.SSLError:
        # proxy công ty chen chứng chỉ tự ký -> thử lại không verify
        # (chấp nhận được: văn bản công khai, có sanity check số Điều phía sau)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url, timeout=300, headers=HEADERS, verify=False)
    r.raise_for_status()
    if r.content[:4] != b"%PDF":
        raise RuntimeError("noi dung tra ve khong phai PDF")
    reader = PdfReader(io.BytesIO(r.content))
    return clean_text("\n".join(p.extract_text() or "" for p in reader.pages)), url


def fetch_vanban(docid):
    """Trang vanban.chinhphu.vn: tìm link file đính kèm .pdf rồi convert."""
    page_url = f"https://vanban.chinhphu.vn/?pageid=27160&docid={docid}"
    r = requests.get(page_url, timeout=60, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)
             if re.search(r"\.(pdf|docx?)(\?|$)", a["href"], re.I)]
    if not links:
        raise RuntimeError(f"khong tim thay file dinh kem tren {page_url}")
    links.sort(key=lambda u: (0 if u.lower().endswith(".pdf") else 1))  # ưu tiên PDF
    file_url = links[0]
    if file_url.startswith("/"):
        file_url = "https://vanban.chinhphu.vn" + file_url
    fr = requests.get(file_url, timeout=300, headers=HEADERS)
    fr.raise_for_status()
    if file_url.lower().split("?")[0].endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(fr.content))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    else:
        import docx  # python-docx, chỉ đọc được .docx
        d = docx.Document(io.BytesIO(fr.content))
        text = "\n".join(p.text for p in d.paragraphs)
    return clean_text(text), file_url


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    rows = []
    for code, (nhom, kind, ref) in SOURCES.items():
        out = STAGING / nhom / f"{code}.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and out.stat().st_size > 5000:
            text = out.read_text(encoding="utf-8")
            so_dieu = len(re.findall(r"^\s*Điều \d+", text, re.M))
            rows.append([code, nhom, ref if isinstance(ref, str) else "", date.today().isoformat(), so_dieu, "da tai truoc do"])
            print(f"--- {code}: da co file hop le ({so_dieu} Dieu), bo qua", flush=True)
            continue
        print(f"--- {code} ({kind}) ...", flush=True)
        try:
            fetcher = {"xdcs": fetch_xdcs, "vbpl": fetch_vbpl, "pdf": fetch_pdf, "vanban": fetch_vanban}[kind]
            text, src = fetcher(ref)
            so_dieu = len(re.findall(r"^\s*Điều \d+", text, re.M))
            note = ""
            if so_dieu < 5:
                note = "⚠️ qua it Dieu — kiem tra file tai thieu/loi extract"
            if len(text) < 5000:
                note = "⚠️ file qua ngan — nhieu kha nang loi"
            out.write_text(text, encoding="utf-8")
            print(f"    OK: {len(text):,} ky tu, {so_dieu} Dieu -> {out.relative_to(ROOT)} {note}", flush=True)
            rows.append([code, nhom, src, date.today().isoformat(), so_dieu, note])
        except Exception as e:
            print(f"    LOI: {type(e).__name__}: {e}", flush=True)
            rows.append([code, nhom, str(ref), date.today().isoformat(), 0, f"LOI: {e}"])
    draft = STAGING / "metadata_draft.csv"
    with open(draft, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(DRAFT_COLS)
        w.writerows(rows)
    print(f"\nXong. Bang nhap: {draft.relative_to(ROOT)}")
    print("Nguoi dung duyet xong moi chuyen vao laws/ (lenh: 'duyet file X' / 'duyet tat ca').")


if __name__ == "__main__":
    main()
