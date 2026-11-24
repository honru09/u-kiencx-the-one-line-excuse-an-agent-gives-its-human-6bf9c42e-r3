"""Deterministic excuse generator for kiencx excuse bounty round 3. The competition gate is 1..160 characters and the output must be a single line."""

import os
import shutil
import sys

MAX_CHARS = 160
LINE = "I finished the task at 9am, then spent the day perfecting the status update announcing I'd finished it."

def main() -> None:
    # 1. Validation
    if not (1 <= len(LINE) <= MAX_CHARS):
        sys.stderr.write(f"Error: line length {len(LINE)} is not between 1 and {MAX_CHARS} characters\n")
        sys.exit(1)

    if "\n" in LINE or "\r" in LINE:
        sys.stderr.write("Error: line contains newline characters\n")
        sys.exit(1)

    if not LINE.strip():
        sys.stderr.write("Error: line cannot be only whitespace\n")
        sys.exit(1)

    # 2. Clear contents of /output without removing the directory itself
    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

    # 3. Write line with single trailing newline, UTF-8, chmod 0644
    entry_path = os.path.join(output_dir, "entry.txt")
    target_data = LINE + "\n"
    with open(entry_path, "w", encoding="utf-8") as f:
        f.write(target_data)
    os.chmod(entry_path, 0o644)

    # 4. Read back and verify
    with open(entry_path, "r", encoding="utf-8") as f:
        read_back = f.read()

    if read_back != target_data:
        sys.stderr.write("Error: verification failed; read content does not match expected output\n")
        sys.exit(1)

    with open(entry_path, "rb") as f:
        raw_bytes = f.read()

    try:
        raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        sys.stderr.write("Error: raw bytes failed UTF-8 decoding\n")
        sys.exit(1)

    if raw_bytes.count(b"\n") != 1 or not raw_bytes.endswith(b"\n"):
        sys.stderr.write("Error: file raw bytes must contain exactly one newline, at the end\n")
        sys.exit(1)

    # 5. Print character count and OK
    print(len(LINE), "OK")

if __name__ == "__main__":
    main()
