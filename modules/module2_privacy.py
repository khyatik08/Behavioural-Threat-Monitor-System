import csv
from datetime import datetime
from tkinter import filedialog

def run_scanner(callback):
    filepath=filedialog.askopenfilename(title="Select Dataset",filetypes=[("CSV Files","*.csv"),("All Files","*.*")])
    if not filepath:
        callback("No file selected."); return

    with open(filepath,"r",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))

    total=clean=affected=violations=0
    upload_count=download_count=other_count=0
    blocked_count=permitted_count=0
    platform_count={}
    risk_high=0

    with open("logs/violations.csv","w") as log:
        log.write("Date,Employee,Department,Platform,Activity,Violation,Policy Status,Risk\n")

    for row in rows:
        total+=1
        employee=row["name"]
        department=row["department"]
        platform=row["platform"]
        notes=row["notes"]
        status=row["access status"].strip().lower()

        nl=notes.lower()
        if "upload" in nl: upload_count+=1
        elif "download" in nl: download_count+=1
        else: other_count+=1
        platform_count[platform]=platform_count.get(platform,0)+1

        if status in ("block","blocked"):
            violations+=1; affected+=1; blocked_count+=1; risk_high+=1
            with open("logs/violations.csv","a") as log:
                log.write(f"{datetime.now()},{employee},{department},{platform},{notes},Policy Violation,Blocked,High\n")
        else:
            clean+=1; permitted_count+=1

    callback("")
    callback("=======================================")
    callback("         PRIVACY SCANNER")
    callback("=======================================")
    callback("✓ Dataset Loaded Successfully")
    callback("✓ Scan Completed")
    callback("")
    callback("=======================================")
    callback("SCAN SUMMARY")
    callback("=======================================")
    callback(f"Total Records      : {total}")
    callback(f"Affected Records   : {affected}")
    callback(f"Clean Records      : {clean}")
    callback("")
    callback("Policy Summary")
    callback("-----------------------------")
    callback(f"Blocked Activities   : {blocked_count}")
    callback(f"Permitted Activities : {permitted_count}")
    callback("")
    callback("Activities")
    callback("-----------------------------")
    callback(f"Uploaded Files     : {upload_count}")
    callback(f"Downloaded Files   : {download_count}")
    callback(f"Other Activities   : {other_count}")
    callback("")
    callback("Top Platforms")
    callback("-----------------------------")
    for p,c in sorted(platform_count.items(), key=lambda x:x[1], reverse=True)[:3]:
        callback(f"{p:<18} : {c}")
    callback("")
    callback("Overall Risk")
    callback("-----------------------------")
    callback("Overall Risk : HIGH ⚠" if risk_high else "Overall Risk : LOW")

    with open("logs/privacy_report.txt","w") as r:
        r.write("========== PRIVACY SCAN REPORT ==========\n")
        r.write(f"Date : {datetime.now()}\n")
        r.write(f"File scanned : {filepath}\n")
        r.write(f"Total Records : {total}\n")
        r.write(f"Affected Records : {affected}\n")
        r.write(f"Clean Records : {clean}\n")
        r.write(f"Blocked Activities : {blocked_count}\n")
        r.write(f"Permitted Activities : {permitted_count}\n")
        r.write(f"Uploaded Files : {upload_count}\n")
        r.write(f"Downloaded Files : {download_count}\n")
        r.write(f"Other Activities : {other_count}\n")
        r.write("\nTop Platforms\n")
        for p,c in sorted(platform_count.items(), key=lambda x:x[1], reverse=True)[:3]:
            r.write(f"{p} : {c}\n")
        r.write("=========================================\n")
    callback("")
    callback("✓ privacy_report.txt Generated")
    callback("✓ violations.csv Generated")

