import os
import subprocess

workspace = r"c:\Users\asus\Documents\Visionary API"

def convert_pptx_to_pdf(pptx_rel, pdf_rel):
    pptx_path = os.path.join(workspace, pptx_rel)
    pdf_path = os.path.join(workspace, pdf_rel)
    if not os.path.exists(pptx_path):
        print(f"File not found: {pptx_path}")
        return False

    ps_script = f"""
$ppt = $null
try {{
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open('{pptx_path}', 2, 0, 0)
    $pres.SaveAs('{pdf_path}', 32)
    $pres.Close()
    Write-Host "SUCCESS: {pdf_rel}"
}} catch {{
    Write-Host "ERROR: $($_.Exception.Message)"
}} finally {{
    if ($ppt) {{ $ppt.Quit() }}
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}}
"""
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
    print(res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return os.path.exists(pdf_path)

def convert_docx_to_pdf(docx_rel, pdf_rel):
    docx_path = os.path.join(workspace, docx_rel)
    pdf_path = os.path.join(workspace, pdf_rel)
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        return False

    ps_script = f"""
$word = $null
try {{
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open('{docx_path}')
    $doc.SaveAs([ref]'{pdf_path}', [ref]17)
    $doc.Close()
    Write-Host "SUCCESS: {pdf_rel}"
}} catch {{
    Write-Host "ERROR: $($_.Exception.Message)"
}} finally {{
    if ($word) {{ $word.Quit() }}
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}}
"""
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
    print(res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return os.path.exists(pdf_path)

if __name__ == "__main__":
    print("=== EXPORTING PPTX TO PDF ===")
    convert_pptx_to_pdf("deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx", "deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pdf")

    print("\n=== EXPORTING CORE DELIVERABLES DOCX TO PDF ===")
    convert_docx_to_pdf("deliverables/VISIONARY_PRESENTATION_SCRIPT.docx", "deliverables/VISIONARY_PRESENTATION_SCRIPT.pdf")
    convert_docx_to_pdf("deliverables/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx", "deliverables/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.pdf")
    convert_docx_to_pdf("deliverables/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.docx", "deliverables/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.pdf")

    print("\n=== EXPORTING MEMBER GUIDES TO PDF ===")
    member_files = [
        ("deliverables/member-guides/01_QUACH_KHOA_DUC_EASY_PRESENTATION_GUIDE.docx", "deliverables/member-guides/01_QUACH_KHOA_DUC_EASY_PRESENTATION_GUIDE.pdf"),
        ("deliverables/member-guides/02_DAO_TRI_KHANG_ANDROID_GUIDE.docx", "deliverables/member-guides/02_DAO_TRI_KHANG_ANDROID_GUIDE.pdf"),
        ("deliverables/member-guides/03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.docx", "deliverables/member-guides/03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.pdf"),
        ("deliverables/member-guides/04_VO_NGOC_MINH_DAT_WINFORMS_GUIDE.docx", "deliverables/member-guides/04_VO_NGOC_MINH_DAT_WINFORMS_GUIDE.pdf")
    ]
    for docx_f, pdf_f in member_files:
        convert_docx_to_pdf(docx_f, pdf_f)

    print("\n=== PDF EXPORT COMPLETE ===")
