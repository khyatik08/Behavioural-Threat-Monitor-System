import os

def search_alert(keyword, callback):

    callback("")
    callback("========================================")
    callback("          SEARCH ALERTS")
    callback("========================================")
    callback(f"Keyword : {keyword}")
    callback("")

    files = [
        "logs/usage_log.csv",
        "logs/violations.csv",
        "logs/port_scan_report.txt"
    ]

    total_matches = 0

    for file in files:

        if os.path.exists(file):

            callback(f"\n----- {os.path.basename(file)} -----")

            found = False

            with open(file, "r") as f:

                for line in f:

                    if keyword.lower() in line.lower():

                        callback(line.strip())

                        total_matches += 1
                        found = True

            if not found:
                callback("No matches found.")

        else:

            callback(f"{os.path.basename(file)} not found.")

    callback("")
    callback(f"Total Matches : {total_matches}")
    callback("Search Completed.")
