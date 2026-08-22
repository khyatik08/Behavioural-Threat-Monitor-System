# Behavioural Threat Monitor System (BTMS)

**Python-based cybersecurity monitoring system** designed to monitor user activity, identify policy violations, scan network exposure, maintain security logs, and protect log integrity.

## Features

* **Usage Monitor** – Monitors user/API activity and detects unknown users, off-hours activity, and activity exceeding the defined usage threshold.
* **Privacy Scanner** – Checks activity records against organizational access policies and identifies blocked activities as policy violations.
* **Port Scanner** – Uses **Nmap** to scan a target IP/domain and identify open ports and associated services.
* **View Logs** – Provides centralized access to generated security logs and reports.
* **Search Alerts** – Performs case-insensitive searches across selected security records.
* **Protect Logs** – Uses **SHA-256 hashing** to detect unauthorized modification of security files.
* **Power BI Dashboard** – Provides visual analysis of security records and detected violations.

## Technologies Used

* **Python**
* **Tkinter** – GUI development
* **Pandas** – CSV/data processing
* **CSV / File Handling** – Security logs and reports
* **Regex** – Data/pattern validation where required
* **Hashlib** – SHA-256 file integrity verification
* **Subprocess** – Executing Nmap from Python
* **Nmap** – Network and port scanning
* **Kali Linux / WSL** – Security testing environment
* **Power BI** – Security data visualization and reporting

## System Modules

### 1. Usage Monitor

Reads configuration and activity data from files such as:

* `config.txt`
* `approved_users.txt`
* `api_calls.csv`

It maintains cumulative activity counts for users and flags:

* Unknown users
* Off-hours activity
* Threshold-crossing activity

The threshold is treated as a **company-defined monitoring policy**, not as direct proof of malicious activity.

Output:

`logs/usage_log.csv`

### 2. Privacy Scanner

The Privacy Scanner promotes the organization's **Data Loss Prevention (DLP) and access-control policies** by identifying activities that violate permitted/blocked access rules.

It processes CSV records containing information such as:

* Employee
* Department
* Platform
* Activity
* Access Status

Records marked `Block` or `Blocked` are recorded as policy violations.

Outputs:

* `logs/violations.csv`
* `logs/privacy_report.txt`

### 3. Port Scanner

Uses Nmap through Python's `subprocess` module to perform network scanning.

Example command:

```bash
nmap -Pn -sV -T4 --open -F <target>
```

The scanner can identify:

* Open ports
* Services
* Service/version information
* Network exposure

Outputs:

* `logs/port_scan_report.txt`
* `logs/port_scan.csv`

> Scanning should only be performed on systems or networks for which you have authorization.

### 4. View Logs

Provides a centralized interface for reviewing generated security records and reports.

It can display files such as:

* `usage_log.csv`
* `privacy_report.txt`
* `violations.csv`
* `port_scan_report.txt`

### 5. Search Alerts

Allows administrators to search security records using a username or keyword.

The search is **case-insensitive** and checks selected security files for matching records.

### 6. Protect Logs

Protects the integrity of important security records using **SHA-256 hashing**.

The system:

1. Generates a hash for a security file.
2. Stores the hash as a baseline.
3. Recalculates the hash during verification.
4. Compares the current and stored hashes.
5. Reports the file as `VERIFIED / SAFE` or `FILE TAMPERED / FAILED`.

## Project Structure

```text
BTMS/
│
├── main.py
│
├── config.txt
├── approved_users.txt
│
├── input/
│   └── api_calls.csv
│
├── logs/
│   ├── usage_log.csv
│   ├── violations.csv
│   ├── privacy_report.txt
│   ├── port_scan_report.txt
│   └── port_scan.csv
│
└── README.md
```

## How to Run

### 1. Install Python

Make sure Python 3.x is installed.

### 2. Install required Python libraries

```bash
pip install pandas
```

`tkinter`, `csv`, `hashlib`, `subprocess`, and other standard-library modules generally come with Python.

### 3. Install Nmap

Install Nmap and make sure the `nmap` command is accessible from your system terminal.

### 4. Run BTMS

```bash
python main.py
```

The Tkinter-based GUI will open and provide access to the different cybersecurity monitoring modules.

## Purpose of the Project

BTMS was developed as a **lightweight cybersecurity monitoring and administrative review system**. It combines user activity monitoring, policy-based privacy checking, network exposure assessment, security logging, and log-integrity verification within a single interface.

The system is intended to demonstrate how multiple cybersecurity functions can be integrated into one practical monitoring application.

## Disclaimer

BTMS is an academic/project-based cybersecurity monitoring system. It should be used only in authorized environments. Network scanning must be performed only against systems and networks for which you have explicit permission.

## Author

**Khyati Kimothi**

BCA Student | Cybersecurity Enthusiast
