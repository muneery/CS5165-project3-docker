import os
import re
import socket
from collections import Counter
from pathlib import Path

DATA_DIR = Path("/home/data")
OUTPUT_DIR = DATA_DIR / "output"
RESULT_FILE = OUTPUT_DIR / "result.txt"

IF_FILE = DATA_DIR / "IF.txt"
ARUTW_FILE = DATA_DIR / "AlwaysRememberUsThisWay.txt"

def read_text(path: Path) -> str:
    # Handle UTF-8 and UTF-16 text files correctly
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-16")

def tokenize_basic(text: str):
    # Words only (letters + apostrophes inside words)
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())

def tokenize_split_contractions(text: str):
    # Split contractions like: I'm -> i, m ; can't -> can, t
    tokens = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())
    out = []
    for t in tokens:
        if "'" in t:
            out.extend([p for p in t.split("'") if p])
        else:
            out.append(t)
    return out

def top_n_words(tokens, n=3):
    return Counter(tokens).most_common(n)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "UNKNOWN"
    finally:
        s.close()

def main():
    # Read files
    if_text = read_text(IF_FILE)
    ar_text = read_text(ARUTW_FILE)

    # a) Word count each
    if_tokens = tokenize_basic(if_text)
    ar_tokens_basic = tokenize_basic(ar_text)

    if_count = len(if_tokens)
    ar_count = len(ar_tokens_basic)

    # b) Grand total
    grand_total = if_count + ar_count

    # c) Top 3 IF.txt
    if_top3 = top_n_words(if_tokens, 3)

    # d) Top 3 AlwaysRememberUsThisWay.txt (contractions split)
    ar_tokens_split = tokenize_split_contractions(ar_text)
    ar_top3 = top_n_words(ar_tokens_split, 3)

    # e) IP address
    ip = get_ip_address()

    # f) Write output + print
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "=== Project 3: Docker Results ===",
        f"IF.txt total words: {if_count}",
        f"AlwaysRememberUsThisWay.txt total words: {ar_count}",
        f"Grand total words (both files): {grand_total}",
        "",
        "Top 3 words in IF.txt:"
    ]

    for w, c in if_top3:
        lines.append(f"  {w}: {c}")

    lines.append("")
    lines.append("Top 3 words in AlwaysRememberUsThisWay.txt (contractions split):")

    for w, c in ar_top3:
        lines.append(f"  {w}: {c}")

    lines.append("")
    lines.append(f"Container host IP address: {ip}")
    lines.append("")

    RESULT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(RESULT_FILE.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
    