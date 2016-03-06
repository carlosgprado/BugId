import os

sBaseFolderPath = os.path.dirname(__file__)

dxConfig = {
  "bSaveReport": True,          # Have BugId.py output a HTML formatted crash report.
  "bSaveTestReports": False,    # Have Tests.py output a HTML formatted crash report.
  "sKillBinaryPath_x86": os.path.join(sBaseFolderPath, "modules", "Kill", "bin", "Kill_x86.exe"),
  "sKillBinaryPath_x64": os.path.join(sBaseFolderPath, "modules", "Kill", "bin", "Kill_x64.exe"),
  "asSymbolServerURLs": ["http://msdl.microsoft.com/download/symbols"],
  "sCdbBinaryPath_x86": r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\cdb.exe",
  "sCdbBinaryPath_x64": r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\cdb.exe"
}
