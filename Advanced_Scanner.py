#!/usr/bin/env python3
"""
Advanced Network Scanner with Logging
"""

import argparse
import subprocess
import logging
import ipaddress
import sys
from datetime import datetime

def setup_logging(log_file: str, verbose: bool):
    """
    Sets up logging to both file and console.
    - File: stores everything (DEBUG and above)
    - Console: shows only INFO and above (or DEBUG if verbose)
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Logger catches everything

    # Clear any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- File Handler: saves everything to a file ---
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Save all levels
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # --- Console Handler: prints to screen ---
    console_handler = logging.StreamHandler()
    if verbose:
        console_handler.setLevel(logging.DEBUG)  # Show everything
    else:
        console_handler.setLevel(logging.INFO)   # Show only INFO and above
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger

def ping_host(ip: str, count: int, timeout: int, logger: logging.Logger) -> tuple:
    """
    Pings a single host and returns (is_alive, output)
    """
    try:
        # Build the ping command
        cmd = ["ping", "-c", str(count), "-W", str(timeout), ip]
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 1  # Slightly longer than ping's timeout
        )
        
        # Log the attempt (DEBUG level)
        logger.debug(f"Ping {ip} - return code: {result.returncode}")
        
        if result.returncode == 0:
            logger.info(f"Host {ip} is ALIVE")
            return (True, result.stdout)
        else:
            logger.debug(f"Host {ip} is dead (no response)")
            return (False, result.stderr)
            
    except subprocess.TimeoutExpired:
        logger.warning(f"Host {ip} - Timeout expired")
        return (False, "Timeout")
    except Exception as e:
        logger.error(f"Host {ip} - Unexpected error: {e}")
        return (False, str(e))
    

def parse_target(target: str, logger: logging.Logger) -> list:
    """
    Converts target into a list of IP addresses.
    Supports single IP (e.g., 192.168.1.1) or network (e.g., 192.168.1.0/24)
    Also supports a range limit (--range option will be applied later)
    """
    ips = []
    
    try:
        # Try to parse as a network
        network = ipaddress.ip_network(target, strict=False)
        # Convert all hosts to strings and store them
        ips = [str(ip) for ip in network.hosts()]
        logger.info(f"Parsed network {target} -> {len(ips)} hosts")
        
    except ValueError:
        # Not a network, try as single IP
        try:
            ipaddress.ip_address(target)  # Validate IP format
            ips = [target]
            logger.info(f"Parsed single IP: {target}")
        except ValueError:
            logger.error(f"Invalid target format: {target}")
            sys.exit(1)
    
    return ips
    
    
def main():
    # ----- Step 1: Parse command-line arguments -----
    parser = argparse.ArgumentParser(
        description="Advanced Network Scanner with Logging",
        epilog="Example: python scanner.py -t 192.168.1.0/24 -r 10 -v"
    )
    
    parser.add_argument(
        "-t", "--target", 
        required=True, 
        help="Target IP or network (e.g., 192.168.1.1 or 192.168.1.0/24)"
    )
    
    parser.add_argument(
        "-c", "--count", 
        type=int, 
        default=4, 
        help="Number of ping packets (default: 4)"
    )
    
    parser.add_argument(
        "-T", "--timeout", 
        type=int, 
        default=2, 
        help="Ping timeout in seconds (default: 2)"
    )
    
    parser.add_argument(
        "-r", "--range", 
        type=int, 
        default=None, 
        help="Limit scan to first N hosts (useful for large networks)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="scan.log", 
        help="Log file name (default: scan.log)"
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Show detailed output on screen (DEBUG level)"
    )
    
    args = parser.parse_args()
    
    # ----- Step 2: Setup logging -----
    logger = setup_logging(args.output, args.verbose)
    
    # Log the start of the scan
    logger.info("=" * 50)
    logger.info(f"Scan started at {datetime.now()}")
    logger.info(f"Target: {args.target}")
    logger.info(f"Packets per host: {args.count}")
    logger.info(f"Timeout: {args.timeout}s")
    
    # ----- Step 3: Parse target into list of IPs -----
    all_ips = parse_target(args.target, logger)
    
    # Apply range limit if specified
    if args.range and args.range < len(all_ips):
        scan_ips = all_ips[:args.range]
        logger.info(f"Range limit: scanning first {len(scan_ips)} of {len(all_ips)} hosts")
    else:
        scan_ips = all_ips
        logger.info(f"Scanning all {len(scan_ips)} hosts")
    
    # ----- Step 4: Scan each host -----
    alive_hosts = []
    total = len(scan_ips)
    
    for i, ip in enumerate(scan_ips, 1):
        logger.debug(f"Progress: {i}/{total} - Checking {ip}")
        is_alive, output = ping_host(ip, args.count, args.timeout, logger)
        
        if is_alive:
            alive_hosts.append(ip)
    
    # ----- Step 5: Summary -----
    logger.info("-" * 50)
    logger.info(f"SCAN COMPLETED")
    logger.info(f"Total hosts scanned: {total}")
    logger.info(f"Alive hosts found: {len(alive_hosts)}")
    
    if alive_hosts:
        logger.info("Alive hosts:")
        for ip in alive_hosts:
            logger.info(f"  - {ip}")
    else:
        logger.warning("No alive hosts found")
    
    logger.info(f"Log saved to: {args.output}")
    logger.info("=" * 50)
    
    # Also print summary to console (INFO already does this)
    print(f"\n✅ Scan complete. {len(alive_hosts)} hosts alive.")

# ----- Entry point -----
if __name__ == "__main__":
    main()
