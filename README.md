# Advanced Network Scanner

> **Note:** This project was manually written by the author, then tested, debugged, and improved with the assistance of **DeepSeek** (AI mentor). DeepSeek provided code reviews, explanatory comments, and suggestions for best practices. The final code is a collaborative effort between human learning and AI guidance.

A powerful, multi-threaded network scanning tool for security professionals and system administrators. It allows you to scan single hosts or entire networks, control scan speed, and generates detailed logs for in-depth analysis. It's designed to be a hands-on educational tool for understanding network scanning concepts.

## Features

*   **Flexible Target Specification:** Scan single IPs (e.g., `192.168.1.10`) or entire networks (e.g., `192.168.1.0/24`).
*   **Range Limiting:** Use the `-r` flag to scan only the first `N` hosts in a network for quick testing.
*   **Customizable Scan:** Control the number of packets (`-c`) and response timeout (`-T`).
*   **Comprehensive Logging:** Logs every event (DEBUG, INFO, WARNING, ERROR) to a file and/or the console in a readable format.
*   **Fine-Grained Control:** Enable `--verbose` mode for detailed on-screen output.
*   **Educational Purpose:** Built as a learning project to demonstrate the integration of `argparse`, `subprocess`, `logging`, and `ipaddress` libraries in Python.

## Disclaimer

**This tool is designed for educational purposes and authorized security testing only.**

You must not use this tool against any system without the explicit permission of its owner. Unauthorized scanning or attacking of networks is illegal in most jurisdictions and can lead to severe penalties.

**By using this software, you agree to the following:**

1.  You assume full responsibility for any actions performed with this tool.
2.  The author(s) of this tool are not liable for any misuse or damage caused by this software.
3.  You will only use this tool on networks and systems you are legally authorized to test.
4.  **If you are unsure about your authorization, do not use this tool.**

## Installation

1.  Ensure you have Python 3.6 or higher installed on your system.
2.  No external libraries are required; the script relies solely on the Python standard library.

## Usage

Run the script from your terminal. Here are some common examples:

```bash
# Scan a single IP address to see if it's alive
python scanner.py -t 192.168.1.10

# Scan only the first 10 hosts of a network, in verbose mode
python scanner.py -t 192.168.1.0/24 -r 10 -v

# Scan a target with 2 packets and a 1-second timeout
python scanner.py -t scanme.nmap.org -c 2 -T 1

# Run a scan and save the full log to a custom file
python scanner.py -t 192.168.1.0/24 -o my_network_scan.log
