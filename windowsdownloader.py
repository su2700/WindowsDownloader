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

if __name__ == "__main__":
    url = input("Enter the download URL or IP: ").strip()
    # Add http:// if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    filename = input("Enter the save file name (with extension): ").strip()
    generate_commands(url, filename)
