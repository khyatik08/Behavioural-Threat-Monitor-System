import csv
import time

def start_monitor(callback):

    callback("Monitoring Started")
    callback("Checking Users...")

    with open("config/config.txt", "r") as config:
        lines = config.readlines()

    threshold = int(lines[0].strip())
    start_hour = int(lines[1].strip())
    end_hour = int(lines[2].strip())

    approved_users = []

    with open("config/approved_users.txt", "r") as users_file:
        for line in users_file:
            approved_users.append(line.strip())

    with open("logs/usage_log.csv", "w") as log:
        log.write("Time,Username,Total Calls,Alert Type\n")

    callback("")
    callback("=========================================")
    callback("         USAGE MONITOR STARTED")
    callback("=========================================")
    callback(f"Threshold     : {threshold} calls")
    callback(f"Office Hours  : {start_hour}:00 to {end_hour}:00")
    callback("")

    with open("input/api_calls.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        all_calls = list(reader)

    callback(f"Total Records : {len(all_calls)}")
    callback("")

    call_count = {}

    for row in all_calls:

        username = row["username"].strip()
        calls = int(row["calls"])
        log_time = row["time"].strip()

        hour = int(log_time.split(":")[0])

        if username in call_count:
            call_count[username] += calls
        else:
            call_count[username] = calls

        total = call_count[username]

        if username not in approved_users:

            callback("UNKNOWN USER DETECTED!")
            callback(f"User  : {username}")
            callback(f"Time  : {log_time}")
            callback(f"Calls : {calls}")
            callback("")

            with open("logs/usage_log.csv", "a") as log:
                log.write(f"{log_time},{username},{total},Unknown user\n")

        elif hour < start_hour or hour >= end_hour:

            callback("OFF-HOURS WARNING!")
            callback(f"User  : {username}")
            callback(f"Time  : {log_time}")
            callback(f"Calls : {calls}")
            callback("")

            with open("logs/usage_log.csv", "a") as log:
                log.write(f"{log_time},{username},{total},Off hours\n")

        elif total > threshold:

            callback("CRITICAL ALERT - THRESHOLD CROSSED!")
            callback(f"User  : {username}")
            callback(f"Total : {total}")
            callback(f"Time  : {log_time}")
            callback("")

            with open("logs/usage_log.csv", "a") as log:
                log.write(f"{log_time},{username},{total},Threshold crossed\n")

        else:

            callback(f"[OK] {log_time} | {username:<12} | {total} calls | Normal")

        time.sleep(0.2)

    callback("")
    callback("=========================================")
    callback("            SCAN COMPLETE")
    callback("=========================================")
    callback("")

    callback("Call Summary")
    callback("-----------------------------------------")

    for user, total in call_count.items():
        callback(f"{user:<15} : {total} calls")

    callback("")
    callback("Log saved successfully to logs/usage_log.csv")
