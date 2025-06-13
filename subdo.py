#Author by yourdre4m7
#Mau recode? minimal izin dlu ya
#Asal recode tanpa izin , NOOB SAMPAH !


import requests
import argparse
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Subdomain yang ingin difilter
EXCLUDED_PREFIXES = (
    "mail.", "webmail.", "cpanel.", "webdisk.", "www.", "autodiscover."
)

def print_banner():
    banner = f"""{Fore.CYAN}
,d88~~\          888       888~~  ,e,                888                        
8888    888  888 888-~88e  888___  "  888-~88e  e88~\888  e88~~8e  888-~\       
`Y88b   888  888 888  888b 888    888 888  888 d888  888 d888  88b 888          
 `Y88b, 888  888 888  8888 888    888 888  888 8888  888 8888__888 888          
   8888 888  888 888  888P 888    888 888  888 Y888  888 Y888    , 888          
\__88P' "88_-888 888-_88"  888    888 888  888  "88_/888  "88___/  888          
                                                                                by t.me/yourdre4m7
        {Style.RESET_ALL}{Fore.GREEN}Mass Subdomain Finder V.1x
        {Fore.YELLOW}Filtered Subdomain : mail, webmail, cpanel, webdisk, www, autodiscover.
"""
    print(banner)

def fetch_crtsh_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                names = entry.get("name_value", "")
                for name in names.split('\n'):
                    name = name.strip().lower()
                    if name.endswith(domain) and not name.startswith(EXCLUDED_PREFIXES):
                        subdomains.add(name)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching subdomains for {domain}: {e}")
    return sorted(subdomains)

def main(domains_file, output_file=None):
    with open(domains_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]

    results = {}
    print_banner()

    for domain in domains:
        print(f"{Fore.CYAN}\n[+] Searching subdomains for: {Fore.WHITE}{domain}")
        subdomains = fetch_crtsh_subdomains(domain)
        results[domain] = subdomains
        for sub in subdomains:
            print(f"{Fore.GREEN}  - {sub}")

    if output_file:
        with open(output_file, 'w') as f:
            for domain, subs in results.items():
                f.write(f"# {domain} ({len(subs)} subdomains)\n")
                for sub in subs:
                    f.write(sub + '\n')
                f.write("\n")
        print(f"\n{Fore.GREEN}[✔] Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mass Subdomain Finder")
    parser.add_argument("-d", "--domains", required=True, help="File containing list of domains")
    parser.add_argument("-o", "--output", help="Output file to save results")
    args = parser.parse_args()

    main(args.domains, args.output)
