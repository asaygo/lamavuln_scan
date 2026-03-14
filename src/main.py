import zipfile
import os
from pathlib import Path
from lama_vuln_check import check_file

TEST_DIR = Path("repos_zip")
IGNORE_LIST = ["test", "example", "mock"]

# only analyze files with this extension
EXTENSION = "*.go"

def extract_zip(zip_path):
    extract_dir = zip_path.with_name(zip_path.stem + "_extracted")

    if not extract_dir.exists():
        print(f"Extracting {zip_path} -> {extract_dir}")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

    return extract_dir

def can_ignore(fname):
    global IGNORE_LIST
    for word in IGNORE_LIST:
        if word in fname:
            return 1
    return 0

def scan_go_files(folder):
    folder_path = Path(folder)

    for go_file in folder_path.rglob(EXTENSION):
        fname = str(go_file)
        if can_ignore(fname) == 0:
            check_file(str(go_file.resolve()))

    return

def extract_go_files():
    zip_files = list(TEST_DIR.glob("*.zip"))

    for zip_file in zip_files:
        print(f"\nProcessing {zip_file}")
        extracted_dir = extract_zip(zip_file)

    return

def main():
    # go through all zip files with the GitHub repos
    extract_files()
    scan_go_files(TEST_DIR)

if __name__ == "__main__":
    main()
