#!/usr/bin/env python3

def generate_commands(url, filename):
    print("\n📥 Generated Download Commands:\n")

    # CMD commands
    print("🔹 CMD:")
    print(f'curl -O {url}')
    print(f'certutil -urlcache -split -f {url} {filename}')
    print(f'bitsadmin /transfer myDownloadJob {url} {filename}')

    # PowerShell commands
    print("\n🔹 PowerShell:")
    print(f'Invoke-WebRequest -Uri "{url}" -OutFile "{filename}"')
    print(f'Start-BitsTransfer -Source "{url}" -Destination "{filename}"')
    print(f'$client = New-Object System.Net.WebClient; $client.DownloadFile("{url}", "{filename}")')
    print(f'iwr -uri "{url}" -Outfile "{filename}"')  # Added iwr short form

if __name__ == "__main__":
    url = input("Enter the download URL or IP: ").strip()
    port = input("Enter the port number (leave blank for default): ").strip()
    # Add http:// if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    # Add port if provided and not already in URL
    if port:
        # Split protocol and the rest
        protocol, rest = url.split("//", 1)
        # If there's already a port, remove it
        if "/" in rest:
            host, path = rest.split("/", 1)
            host = host.split(":")[0]  # Remove existing port if any
            url = f"{protocol}//{host}:{port}/{path}"
        else:
            host = rest.split(":")[0]
            url = f"{protocol}//{host}:{port}"
    filename = input("Enter the save file name (with extension): ").strip()
    generate_commands(url, filename)
