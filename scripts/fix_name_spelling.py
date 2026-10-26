import os
import re

EXTENSIONS = {'.md', '.cs', '.ts', '.tsx', '.py', '.json', '.bat', '.xml', '.java', '.txt', '.html', '.yaml', '.yml'}
EXCLUDE_DIRS = {'.git', 'bin', 'obj', 'node_modules', '.next', '.gradle'}

REPLACEMENTS = [
    # Full name exact matches
    ('Hồ Đoàn Nguyên Khang', 'Hồ Đoàn Nguyên Khang'),
    ('HỒ ĐOÀN NGUYÊN KHANG', 'HỒ ĐOÀN NGUYÊN KHANG'),
    ('Hồ Đoàn', 'Hồ Đoàn'),
    ('HỒ ĐOÀN', 'HỒ ĐOÀN'),
    ('Ho Doan Nguyen Khang', 'Ho Doan Nguyen Khang'),
    ('HO DOAN NGUYEN KHANG', 'HO DOAN NGUYEN KHANG'),
    ('HO_DOAN_NGUYEN_KHANG', 'HO_DOAN_NGUYEN_KHANG'),
    ('HoDoanNguyenKhang', 'HoDoanNguyenKhang'),
    ('HoDoan', 'HoDoan'),
    ('03_HO_DOAN_NGUYEN_KHANG_API_GUIDE', '03_HO_DOAN_NGUYEN_KHANG_API_GUIDE'),
]

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
total_replacements = 0
files_modified = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    # filter directories
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext in EXTENSIONS:
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue

            new_content = content
            file_changed = False
            for old, new in REPLACEMENTS:
                if old in new_content:
                    count = new_content.count(old)
                    new_content = new_content.replace(old, new)
                    total_replacements += count
                    file_changed = True

            if file_changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_modified.append(os.path.relpath(filepath, root_dir))

print(f"Total replacements: {total_replacements}")
print(f"Files modified ({len(files_modified)}):")
for f in files_modified:
    print(f" - {f}")
