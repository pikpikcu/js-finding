#!/usr/bin/env python3

import argparse
import subprocess
import sys
import time
import re
import requests
import pyfiglet
import os
from colorama import Fore, Style, init
import socks
import socket
from urllib.parse import urlparse

def download_file(url, output_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            file_path = os.path.join(output_dir, file_name)

            os.makedirs(output_dir, exist_ok=True)

            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path
        else:
            return None
    except Exception as e:
        print(f"Download error: {str(e)}")
        return None


def create_wordlists(file_path):
    wordlists = set()
    with open(file_path, 'r') as file:
        content = file.read()
        words = re.findall(r'\b\w+\b', content)
        wordlists.update(words)
    return wordlists

def extract_js(domain, debug, download_files, output_dir, create_lists):
    result = []

    try:
        start_time = time.time()
        print(f"Extracting JS from: {domain}")

        processes = {
            "Waybackurls": subprocess.Popen(['waybackurls', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
            "Gauplus": subprocess.Popen(['gauplus', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
            "Subjs": subprocess.Popen(['subjs'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        }

        outputs = {}

        for name, process in processes.items():
            if debug:
                print(f"Extracting JS With: {name}")
            if name == "Subjs":
                output, error = process.communicate(input=domain.encode('utf-8'))
            else:
                output, error = process.communicate()
            output = output.decode('utf-8').splitlines()

            if name in ["Waybackurls", "Gauplus"]:
                output = [url for url in output if re.search(r"\.js$", url)]

            if debug and error:
                print(f"{name} error: {error.decode('utf-8')}")

            outputs[name] = output

        end_time = time.time()

        if debug:
            print(f"Extraction completed in: {end_time - start_time} seconds")

        result.append(f"Extrak domain: {domain}")
        result.append("Results Url JS:")

        for output in set(outputs["Waybackurls"]).union(set(outputs["Gauplus"])).union(set(outputs["Subjs"])):
            result.append(f"- {output}")

            if download_files and output_dir:
                file_path = download_file(output, output_dir)
                if file_path:
                    result.append(f"   - File downloaded: {file_path}")
                    if create_lists:
                        wordlists = create_wordlists(file_path)
                        wordlists_file_path = f"{file_path}.wordlists"
                        with open(wordlists_file_path, 'w') as wordlists_file:
                            wordlists_file.write("\n".join(wordlists))
                        result.append(f"   - Wordlists created: {wordlists_file_path}")
                else:
                    result.append(f"   - Failed to download file")

    except Exception as e:
        result.append(f"Error occured: {str(e)}")
        sys.exit(1)

    return result

def main():
    init()

    codename = "JS Finding"
    version = "v1.002"
    banner = pyfiglet.Figlet(font="slant").renderText(codename)
    banner += f"{version.center(len(codename))}\n"
    print(Fore.GREEN + banner + Style.RESET_ALL)

    parser = argparse.ArgumentParser(description='Extract JS files from given domains.')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-u', '--url', metavar='url', type=str, help='Single domain URL')
    group.add_argument('-l', '--list', metavar='file', type=str, help='A file containing a list of domains')
    parser.add_argument('-o', '--output', metavar='output', type=str, help='The output file to store the results')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-download', action='store_true', help='Enable file download')
    parser.add_argument('-output-dir', metavar='dir', type=str, help='The directory to store downloaded files')
    parser.add_argument('-create-lists', action='store_true', help='Enable wordlists creation')
    parser.add_argument('-proxy', metavar='proxy', type=str, help='Use a proxy server for requests')

    args = parser.parse_args()

    results = []

    if args.proxy:
        parsed_proxy = urlparse(args.proxy)
        proxy_type = parsed_proxy.scheme.lower()
        proxy_host = parsed_proxy.hostname
        proxy_port = parsed_proxy.port
        proxy_username = parsed_proxy.username
        proxy_password = parsed_proxy.password

        if proxy_type == 'http' or proxy_type == 'https':
            proxies = {
                'http': args.proxy,
                'https': args.proxy
            }
        elif proxy_type == 'socks4':
            socks.setdefaultproxy(socks.SOCKS4, proxy_host, proxy_port)
            socket.socket = socks.socksocket
        elif proxy_type == 'socks5':
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            socket.socket = socks.socksocket
            if proxy_username and proxy_password:
                socks.wrapmodule(requests)
                requests.get = socks.socksocket.get
        else:
            raise ValueError('Unsupported proxy type')
    else:
        proxies = None

    if not sys.stdin.isatty():
        input_lines = sys.stdin.readlines()
        for line in input_lines:
            line = line.strip()
            extracted = extract_js(line, args.debug, args.download, args.output_dir, args.create_lists)
            results += extracted
            results.append("")  # Add an empty line for readability
            print("\n".join(extracted))
            print()

    if args.url:
        extracted = extract_js(args.url, args.debug, args.download, args.output_dir, args.create_lists)
        results += extracted
        results.append("")  # Add an empty line for readability
        print("\n".join(extracted))
        print()

    if args.list:
        with open(args.list, 'r') as f:
            domains = f.read().splitlines()
        for domain in domains:
            extracted = extract_js(domain, args.debug, args.download, args.output_dir, args.create_lists)
            results += extracted
            results.append("")  # Add an empty line for readability
            print("\n".join(extracted))
            print()

    if args.output:
        output_content = "\n".join(results)
        with open(args.output, 'w') as f:
            f.write(output_content)
        print(Fore.CYAN + f"Results written to {args.output}" + Style.RESET_ALL)

    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        print(Fore.CYAN + f"Output directory created: {output_dir}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
