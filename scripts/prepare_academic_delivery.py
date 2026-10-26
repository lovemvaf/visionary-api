import os
import shutil
import hashlib

BASE_DIR = r"c:\Users\asus\Documents\Visionary API"
DELIVERY_DIR = os.path.join(BASE_DIR, "VISIONARY-ACADEMIC-DELIVERY")

DIRS = [
    "presentation",
    "slide-previews",
    "scripts-and-notes",
    "questions-and-answers",
    "demo-instructions",
    "member-guides",
    "grading-requirements",
    "evidence",
    "assets/logos",
    "tools",
    "internal-engineering-archive/agent-state",
    "internal-engineering-archive/security-records"
]

for d in DIRS:
    os.makedirs(os.path.join(DELIVERY_DIR, d), exist_ok=True)

print("Directories created successfully.")

# Map source files to destinations
COPY_MAPPINGS = [
    # Presentation
    ("deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx", "presentation/VISIONARY_TH71108_FINAL_PRESENTATION.pptx"),
    ("deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pdf", "presentation/VISIONARY_TH71108_FINAL_PRESENTATION.pdf"),
    
    # Scripts and Notes
    ("deliverables/VISIONARY_PRESENTATION_SCRIPT.docx", "scripts-and-notes/VISIONARY_PRESENTATION_SCRIPT.docx"),
    ("deliverables/VISIONARY_PRESENTATION_SCRIPT.pdf", "scripts-and-notes/VISIONARY_PRESENTATION_SCRIPT.pdf"),
    
    # Q&A
    ("deliverables/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx", "questions-and-answers/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx"),
    ("deliverables/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.pdf", "questions-and-answers/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.pdf"),
    
    # Demo Instructions
    ("deliverables/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.docx", "demo-instructions/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.docx"),
    ("deliverables/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.pdf", "demo-instructions/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.pdf"),
    
    # Grading Requirements
    ("docs/TH71108_FINAL_READINESS_REPORT.md", "grading-requirements/TH71108_FINAL_READINESS_REPORT.md"),
    ("docs/TH71108_REQUIREMENTS_TRACEABILITY_MATRIX.md", "grading-requirements/TH71108_REQUIREMENTS_TRACEABILITY_MATRIX.md"),
    ("docs/TH71108_SOURCE_CODE_EVIDENCE.md", "grading-requirements/TH71108_SOURCE_CODE_EVIDENCE.md"),
    
    # Evidence incident report
    ("docs/TH71108_REAL_CI_INCIDENT_REPORT.md", "evidence/TH71108_REAL_CI_INCIDENT_REPORT.md"),
    
    # University Logos
    ("assets/logos/dntu_logo.png", "assets/logos/dntu_logo.png"),
    ("assets/logos/cntt_dntu_logo.png", "assets/logos/cntt_dntu_logo.png"),
]

# Add member guides
mg_src = os.path.join(BASE_DIR, "deliverables", "member-guides")
if os.path.exists(mg_src):
    for f in os.listdir(mg_src):
        COPY_MAPPINGS.append((f"deliverables/member-guides/{f}", f"member-guides/{f}"))

# Add slide previews
sp_src = os.path.join(BASE_DIR, "deliverables", "slide-previews")
if os.path.exists(sp_src):
    for f in os.listdir(sp_src):
        COPY_MAPPINGS.append((f"deliverables/slide-previews/{f}", f"slide-previews/{f}"))

# Add evidence screenshots
ev_src = os.path.join(BASE_DIR, "deliverables", "evidence")
if os.path.exists(ev_src):
    for f in os.listdir(ev_src):
        COPY_MAPPINGS.append((f"deliverables/evidence/{f}", f"evidence/{f}"))

# Add presentation tools from scripts
script_files_to_tools = [
    "apply_slide_updates.py",
    "build_dat_winforms_guide.py",
    "build_duc_guide.py",
    "build_full_master_presentation.py",
    "build_ho_khang_api_guide.py",
    "build_khang_android_guide.py",
    "build_perfect_presentation.py",
    "build_presentation_base.py",
    "build_presentation_slides_1_to_7.py",
    "export_all_to_pdf.py",
    "fix_qa_guide_syntax.py",
    "fix_quotes.py",
    "generate_app_ui_cards.py",
    "generate_cards.py",
    "generate_full_qa_guide.py",
    "generate_live_demo_and_swagger_guide.py",
    "generate_presentation_script_doc.py",
    "inject_ci_qa.py",
    "member_guides_helpers.py",
    "render_presentation_slides.py",
    "test_pdf_env.py",
    "update_ci_cards.py",
    "update_s10_s11.py",
    "update_script_and_dat_guide.py"
]

for s in script_files_to_tools:
    src_path = f"scripts/{s}"
    if os.path.exists(os.path.join(BASE_DIR, src_path)):
        COPY_MAPPINGS.append((src_path, f"tools/{s}"))

# Add agent state files
agent_src = os.path.join(BASE_DIR, ".agent")
if os.path.exists(agent_src):
    for f in os.listdir(agent_src):
        if os.path.isfile(os.path.join(agent_src, f)):
            COPY_MAPPINGS.append((f".agent/{f}", f"internal-engineering-archive/agent-state/{f}"))

# Add security audit records from docs/security/
sec_src = os.path.join(BASE_DIR, "docs", "security")
if os.path.exists(sec_src):
    for f in os.listdir(sec_src):
        if os.path.isfile(os.path.join(sec_src, f)):
            COPY_MAPPINGS.append((f"docs/security/{f}", f"internal-engineering-archive/security-records/{f}"))

# Perform copying and verification
copied_count = 0
failed = []

for src_rel, dst_rel in COPY_MAPPINGS:
    src_full = os.path.join(BASE_DIR, src_rel)
    dst_full = os.path.join(DELIVERY_DIR, dst_rel)
    
    if not os.path.exists(src_full):
        failed.append(f"Source missing: {src_rel}")
        continue
        
    os.makedirs(os.path.dirname(dst_full), exist_ok=True)
    shutil.copy2(src_full, dst_full)
    
    # Verify file sizes
    src_size = os.path.getsize(src_full)
    dst_size = os.path.getsize(dst_full)
    if src_size != dst_size:
        failed.append(f"Size mismatch: {src_rel} ({src_size} vs {dst_size})")
    else:
        copied_count += 1

print(f"Total files copied and verified: {copied_count}")
if failed:
    print(f"Failures: {len(failed)}")
    for f in failed:
        print("  -", f)
else:
    print("ALL FILES SUCCESSFULLY COPIED WITH 100% SIZE INTEGRITY!")
