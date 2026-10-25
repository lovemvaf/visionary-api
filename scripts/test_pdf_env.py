import shutil
import subprocess

print("soffice:", shutil.which("soffice"))
print("libreoffice:", shutil.which("libreoffice"))

ps_word = """
try {
    $word = New-Object -ComObject Word.Application
    Write-Host "WORD_OK"
    $word.Quit()
} catch {
    Write-Host "WORD_ERR: $($_.Exception.Message)"
}
"""
p1 = subprocess.run(["powershell", "-NoProfile", "-Command", ps_word], capture_output=True, text=True)
print("PowerShell Word:", p1.stdout.strip())

ps_ppt = """
try {
    $ppt = New-Object -ComObject PowerPoint.Application
    Write-Host "PPT_OK"
    $ppt.Quit()
} catch {
    Write-Host "PPT_ERR: $($_.Exception.Message)"
}
"""
p2 = subprocess.run(["powershell", "-NoProfile", "-Command", ps_ppt], capture_output=True, text=True)
print("PowerShell PPT:", p2.stdout.strip())
