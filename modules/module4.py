import os

def view_logs(callback):

    callback("")
    callback("======================================")
    callback("         VIEWING LOG FILES")
    callback("======================================")
    callback("")

    files = [
        "logs/usage_log.csv",
        "logs/privacy_report.txt",
        "logs/violations.csv",
        "logs/port_scan_report.txt"
    ]

    for file in files:

        callback(f"\n========== {os.path.basename(file)} ==========\n")

        if os.path.exists(file):

            with open(file, "r") as f:

                data = f.readlines()

                if len(data) == 0:

                    callback("File is Empty.")

                else:

                    for line in data:
                        callback(line.strip())

        else:

            callback("File Not Found.")

    callback("\nFinished Reading All Log Files.")
