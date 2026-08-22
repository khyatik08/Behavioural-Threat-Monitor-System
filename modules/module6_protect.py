import hashlib
import os

FILES = [
    "logs/usage_log.csv",
    "logs/violations.csv",
    "logs/privacy_report.txt",
    "logs/port_scan_report.txt"
]


def calculate_hash(filename):
    sha = hashlib.sha256()

    with open(filename, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


def protect_logs(callback):

    callback("")
    callback("========================================")
    callback("      LOG INTEGRITY CHECK")
    callback("========================================")
    callback("")

    for file in FILES:

        if not os.path.exists(file):
            callback(f"{file}  ->  File Not Found.")
            continue

        hash_file = file + ".hash"

        current_hash = calculate_hash(file)

        # First Time → Generate Hash
        if not os.path.exists(hash_file):

            with open(hash_file, "w") as f:
                f.write(current_hash)

            callback(f"{os.path.basename(file)}")
            callback("Status : Protected")
            callback("Integrity : Hash Generated")
            callback("")

        # Verify Existing Hash
        else:

            with open(hash_file, "r") as f:
                saved_hash = f.read().strip()

            if current_hash == saved_hash:

                callback(f"{os.path.basename(file)}")
                callback("Status : VERIFIED")
                callback("Integrity : SAFE")
                callback("")

            else:

                callback(f"{os.path.basename(file)}")
                callback("ALERT : FILE TAMPERED")
                callback("Integrity : FAILED")
                callback("")

    callback("Verification Completed.")
