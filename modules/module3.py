import subprocess
import os
import csv
import re
import threading
from datetime import datetime


def run_port_scanner(target, callback):

    # Run the actual scan in background
    thread = threading.Thread(
        target=perform_port_scan,
        args=(target, callback),
        daemon=True
    )

    thread.start()


def perform_port_scan(target, callback):

    callback("")
    callback("==============================================")
    callback("              PORT SCANNER STARTED")
    callback("==============================================")

    # --------------------------------------------------
    # Separate multiple targets
    # --------------------------------------------------

    targets = re.split(r"[\s,]+", target.strip())
    targets = [t for t in targets if t]

    if not targets:
        callback("ERROR: No target IP/domain provided.")
        return

    callback("Targets:")

    for t in targets:
        callback(f"  - {t}")

    callback("")
    callback("Running Nmap...")
    callback("")

    os.makedirs("logs", exist_ok=True)

    report_file = "logs/port_scan_report.txt"
    csv_file = "logs/port_scan.csv"

    # --------------------------------------------------
    # Nmap command
    # --------------------------------------------------

    command = [
    "nmap",
    "-Pn",
    "-sV",
    "-T4",
    "-F",
    "--open",
    "--host-timeout", "30s",
    "--max-retries", "1",
    target
]
    
    callback("Command:")
    callback(" ".join(command))
    callback("")

    try:

        # --------------------------------------------------
        # Start Nmap
        # --------------------------------------------------

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        output_lines = []

        # --------------------------------------------------
        # Display output while Nmap is running
        # --------------------------------------------------

        for line in process.stdout:

            line = line.rstrip()

            if line:

                output_lines.append(line)

                callback(line)

        process.wait()

        # --------------------------------------------------
        # Check result
        # --------------------------------------------------

        if process.returncode != 0:

            callback("")
            callback("Nmap scan failed.")
            callback(
                f"Return code: {process.returncode}"
            )

            return

        # --------------------------------------------------
        # Save TXT report
        # --------------------------------------------------

        with open(
            report_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "BEHAVIOURAL THREAT MONITOR SYSTEM\n"
            )

            file.write(
                "PORT SCAN REPORT\n"
            )

            file.write(
                "====================================\n"
            )

            file.write(
                f"Scan Time : {datetime.now()}\n"
            )

            file.write(
                f"Targets   : {', '.join(targets)}\n\n"
            )

            for line in output_lines:

                file.write(line + "\n")

        # --------------------------------------------------
        # Create CSV
        # --------------------------------------------------

        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Scan Time",
                "Target",
                "Port",
                "Protocol",
                "State",
                "Service",
                "Version"
            ])

            current_target = ""

            for line in output_lines:

                # Example:
                # Nmap scan report for 192.168.1.10

                if line.startswith(
                    "Nmap scan report for"
                ):

                    current_target = (
                        line
                        .replace(
                            "Nmap scan report for",
                            ""
                        )
                        .strip()
                    )

                # Example:
                # 22/tcp open ssh OpenSSH...

                match = re.match(
                    r"(\d+)/(tcp|udp)\s+"
                    r"(\w+)\s+"
                    r"(\S+)"
                    r"(?:\s+(.*))?",
                    line
                )

                if match:

                    port = match.group(1)
                    protocol = match.group(2)
                    state = match.group(3)
                    service = match.group(4)
                    version = (
                        match.group(5)
                        if match.group(5)
                        else ""
                    )

                    writer.writerow([
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        current_target,
                        port,
                        protocol,
                        state,
                        service,
                        version
                    ])

        callback("")
        callback("==============================================")
        callback("          SCAN COMPLETED SUCCESSFULLY")
        callback("==============================================")

        callback(
            f"Report saved to {report_file}"
        )

        callback(
            f"CSV saved to {csv_file}"
        )

    except FileNotFoundError:

        callback(
            "ERROR: Nmap is not installed or "
            "not available in PATH."
        )

    except Exception as e:

        callback(
            f"ERROR: {str(e)}"
        )