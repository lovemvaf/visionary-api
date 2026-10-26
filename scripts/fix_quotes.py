import re

file_path = "scripts/build_perfect_presentation.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace any pattern like: '(\d+)["''](\d+)["'']' inside strings
# E.g. 1'00" -> 1p00s, 0'45" -> 0p45s, 1'15" -> 1p15s
def repl(m):
    return f"{m.group(1)}p{m.group(2)}s"

new_content = re.sub(r"(\d+)['\u2019](\d+)[\"\u201d]", repl, content)
# Also fix any single unescaped double quotes inside LỜI THUYẾT TRÌNH lines
new_content = re.sub(r'LỜI THUYẾT TRÌNH \(([^)]+)\):\s*\\n"', r'LỜI THUYẾT TRÌNH (\1):\\n"', new_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("build_perfect_presentation.py cleaned of unescaped quotes.")
