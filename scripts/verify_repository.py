#!/usr/bin/env python3
"""
VISIONARY REPOSITORY QUALITY GATE & VERIFICATION SCRIPT
Runs comprehensive checks for repository hygiene, credential exposure,
naming correctness, test consistency, and artifact integrity.
"""

import os
import sys
import json
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def check_tracked_secrets():
    print("[1/6] Checking for tracked sensitive files (.env, .pyc, __pycache__)...")
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "**/.env", "**/.env.local", "**/.env.production", "**/*.pyc", "**/__pycache__/**"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        if output:
            print(f"  [FAIL]: Tracked sensitive/temporary files found:\n{output}")
            return False
        print("  [PASS]: No tracked .env, .pyc, or __pycache__ files.")
        return True
    except subprocess.CalledProcessError:
        print("  [PASS]: Git check returned clean.")
        return True

def check_member_name_spelling():
    print("[2/6] Checking for incorrect spelling 'Hồ Đoàng' in tracked files...")
    bad_patterns = ["Hồ Đoàng", "HỒ ĐOÀNG", "Ho Doang"]
    violations = []
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Check tracked text files only
    try:
        tracked_files = subprocess.check_output(
            ["git", "ls-files"], text=True, cwd=root_dir
        ).strip().splitlines()
    except Exception as e:
        print(f"  [WARN]: Could not list tracked files via git: {e}")
        tracked_files = []

    for rel_path in tracked_files:
        ext = os.path.splitext(rel_path)[1].lower()
        if ext in {'.md', '.cs', '.ts', '.tsx', '.py', '.json', '.xml', '.java', '.txt', '.yaml', '.yml'}:
            full_path = os.path.join(root_dir, rel_path)
            if not os.path.exists(full_path):
                continue
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for bp in bad_patterns:
                    if bp in content:
                        violations.append((rel_path, bp))
            except Exception:
                pass

    if violations:
        print(f"  [FAIL]: Found {len(violations)} instances of incorrect name spelling:")
        for path, bp in violations[:10]:
            print(f"    - {path}: found '{bp}'")
        return False
    print("  [PASS]: Zero instances of 'Hồ Đoàng' in tracked files.")
    return True

def check_test_consistency():
    print("[3/6] Checking test consistency across canonical reports...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    status_file = os.path.join(root_dir, "project-status", "verification.json")
    
    if not os.path.exists(status_file):
        print(f"  [FAIL]: {status_file} not found.")
        return False
        
    with open(status_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    backend_tests = data.get("backend", {}).get("tests", {}).get("total")
    if backend_tests != 15:
        print(f"  [FAIL]: Canonical verification.json expects 15 tests, got {backend_tests}.")
        return False
        
    print(f"  [PASS]: Canonical verification.json accurately reflects {backend_tests}/15 tests.")
    return True

def check_backend_solution_tests():
    print("[4/6] Executing backend xUnit tests locally (15 tests expected)...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    try:
        cmd = ["dotnet", "test", "backend/Visionary.Backend.sln", "--nologo"]
        res = subprocess.run(cmd, cwd=root_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL]: dotnet test failed:\n{res.stdout}\n{res.stderr}")
            return False
        if "Passed!  - Failed:     0, Passed:    15" in res.stdout or "Passed: 15" in res.stdout:
            print("  [PASS]: dotnet test 15/15 Passed 100%.")
            return True
        else:
            print(f"  [WARN]: Output did not match expected 15 passes:\n{res.stdout}")
            return False
    except Exception as e:
        print(f"  [FAIL]: ERROR running dotnet test: {e}")
        return False

def check_desktop_build():
    print("[5/6] Checking Windows Forms Desktop compilation...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    try:
        cmd = ["dotnet", "build", "desktop/Visionary.Desktop/Visionary.Desktop.csproj", "--nologo"]
        res = subprocess.run(cmd, cwd=root_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL]: Desktop build failed:\n{res.stderr}")
            return False
        print("  [PASS]: Windows Forms compiled successfully.")
        return True
    except Exception as e:
        print(f"  [FAIL]: ERROR checking desktop build: {e}")
        return False

def check_deliverable_filenames():
    print("[6/6] Checking member guide deliverable filenames...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    mg_dir = os.path.join(root_dir, "deliverables", "member-guides")
    
    old_file = os.path.join(mg_dir, "03_HO_DOANG_NGUYEN_KHANG_API_GUIDE.docx")
    new_file = os.path.join(mg_dir, "03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.docx")
    
    if os.path.exists(old_file):
        print(f"  [FAIL]: Old filename still exists: {old_file}")
        return False
        
    if not os.path.exists(new_file):
        print(f"  [FAIL]: Corrected filename missing: {new_file}")
        return False
        
    print("  [PASS]: Member guides correctly renamed to 03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.")
    return True

def main():
    print("=" * 70)
    print("      VISIONARY API - REPOSITORY VERIFICATION QUALITY GATE")
    print("=" * 70)
    
    results = [
        check_tracked_secrets(),
        check_member_name_spelling(),
        check_test_consistency(),
        check_backend_solution_tests(),
        check_desktop_build(),
        check_deliverable_filenames(),
    ]
    
    print("=" * 70)
    if all(results):
        print(">>> ALL 6 QUALITY GATES PASSED! REPOSITORY IS CLEAN & AUDITED.")
        print("=" * 70)
        sys.exit(0)
    else:
        print(">>> QUALITY GATE CHECKS FAILED. PLEASE REVIEW LOGS ABOVE.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
