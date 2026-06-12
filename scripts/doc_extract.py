# -*- coding: utf-8 -*-
"""Bóc text từ file .doc (Word 97-2003 binary) không cần MS Word.
Cách làm: decode stream WordDocument theo UTF-16LE rồi lọc các đoạn văn bản liên tục.
Dùng: python doc_extract.py <file.doc> [file_out.txt]
Lưu ý: đây là cách bóc heuristic — kiểm tra số Điều + đọc soát trước khi dùng làm nguồn luật.
"""
import re
import sys
import unicodedata

import olefile


def extract(path):
    ole = olefile.OleFileIO(path)
    data = ole.openstream("WordDocument").read()
    t = data.decode("utf-16-le", errors="ignore")
    t = unicodedata.normalize("NFC", t)
    # giữ các run dài gồm chữ (mọi chữ cái unicode), số, dấu câu thường gặp
    pattern = r"[\w\s.,;:()‘’“”\"'%/–—\-+]{40,}"
    runs = re.findall(pattern, t, re.UNICODE)
    out = "\n".join(r.strip() for r in runs if r.strip())
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    text = extract(sys.argv[1])
    print("ky tu:", len(text))
    print("Dieu N:", len(re.findall(r"Điều \d+", text)))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print("da ghi:", sys.argv[2])
    else:
        print("sample dau:", repr(text[:400]))
        print("sample cuoi:", repr(text[-300:]))
