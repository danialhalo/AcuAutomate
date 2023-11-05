#!/usr/bin/env python3
# Unoficial Acunetix CLI version for automation 
# Coded by https://twitter.com/DanialHalo

import requests
import json
import argparse
import validators
import textwrap
import sys
requests.packages.urllib3.disable_warnings()



with open('config.json') as config_file:
    config = json.load(config_file)



tarurl = config['url']+":"+str(config['port'])
headers = {
    "X-Auth": config['api_key'],
    "Content-Type": "application/json"
}

def create_scan(target_url, scan_type):
    scan_profile = {
        "full": "11111111-1111-1111-1111-111111111111",
        "high": "11111111-1111-1111-1111-111111111112",
        "weak": "11111111-1111-1111-1111-111111111115",
        "crawl": "11111111-1111-1111-1111-111111111117",
        "xss": "11111111-1111-1111-1111-111111111116",
        "sql": "11111111-1111-1111-1111-111111111113",
    }
    profile_id = scan_profile.get(scan_type, scan_profile['full'])

    def add_task(url=''):
        data = {"address": url, "description": url, "criticality": "10"}
        try:
            response = requests.post(tarurl + "/api/v1/targets", data=json.dumps(data), headers=headers, timeout=30, verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(str(e))
            return

    url = tarurl+"/api/v1/scans"

    print("[*] Running scan on : "+str(target_url))

    data = {
        "target_id": add_task(target_url),
        "profile_id": profile_id,
        "schedule": {"disable": False, "start_date": None, "time_sensitive": False},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)


def scan_targets_from_file(file_path, scan_type):
    try:
        with open(file_path) as f:
            targets = f.readlines()
        targets = [x.strip() for x in targets]
        for target in targets:
            if validators.url(target):
                create_scan(target, scan_type)
            else:
                print("[!] Invalid URL: "+target)
    except Exception as e:
                print("[!] Error reading file: "+str(e))




def stop_scan(scan_id):
    url = tarurl+"/api/v1/scans/"+str(scan_id)+"/abort"
    response = requests.post(url, headers=headers, verify=False)

    print("[-] Scan stop scan id: "+scan_id)


def stop_specific_scan(target):
    url = tarurl+"/api/v1/scans?q=status:processing;"
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    for scan in scans:
        if target == scan["target"]["description"]:
            stop_scan(scan["scan_id"])

def stop_all_scans():
    url = tarurl+"/api/v1/scans?q=status:processing;"
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    for scan in scans:
        stop_scan(scan["scan_id"])


if __name__ == "__main__":


    banner = """

    \t\t                               __  _                 ___
    \t\t  ____ ________  ______  ___  / /_(_)  __      _____/ (_)
    \t\t / __ `/ ___/ / / / __ \/ _ \/ __/ / |/_/_____/ ___/ / /
    \t\t/ /_/ / /__/ /_/ / / / /  __/ /_/ />  </_____/ /__/ / /
    \t\t\__,_/\___/\__,_/_/ /_/\___/\__/_/_/|_|      \___/_/_/
    \t\t
    \t\t                   -: By Danial Halo :-

    """

    print(banner)



    if len(sys.argv) < 2:  # Check if no command line arguments are provided
        print("usage: acunetix-cli.py [-h]")


    parser = argparse.ArgumentParser(description="Launch or stop a scan using Acunetix API")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Start sub-command
    start_parser = subparsers.add_parser("scan", help="Launch a scan use scan -h")
    start_parser.add_argument("-p", "--pipe", action='store_true', help='Read from pipe')
    start_parser.add_argument("-d", "--domain", help="Domain to scan")
    start_parser.add_argument("-f", "--file", help="File containing list of URLs to scan")
    start_parser.add_argument("-t", "--type", choices=["full", "high", "weak", "crawl", "xss", "sql"], default="full",
                        help= textwrap.dedent('''\
                        High Risk Vulnerabilities Scan,
                        Weak Password Scan,
                        Crawl Only,
                        XSS Scan,
                        SQL Injection Scan,
                        Full Scan (by default)'''))


    # Stop sub-command
    stop_parser = subparsers.add_parser("stop", help="Stop a scan")
    stop_parser.add_argument("-d", "--domain", help="Domain of the scan to stop")
    stop_parser.add_argument("-a", "--all", action='store_true', help="Stop all Running Scans")

    args = parser.parse_args()

    if args.action == "scan":
        if args.domain:
            if validators.url(args.domain):
                create_scan(args.domain, args.type)
            else:
                print("[!] Invalid URL: "+args.domain)

        elif args.file:
            scan_targets_from_file(args.file, args.type)

        elif args.pipe:
            input_data = sys.stdin.read().split('\n')
            for url in input_data:
                if validators.url(url):
                    create_scan(url, args.type)

        else:
            print("[!] Must provide either domain or file containing list of targets \nFor Help: acunetix.py scan -h")

    elif args.action == "stop":
        if args.domain:
            stop_specific_scan(args.domain)
        elif args.all == True:
            stop_all_scans()
        else:
            print("[!] Must provide either domain or stop all flag \nFor Help: acunetix.py stop -h")
