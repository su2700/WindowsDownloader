#!/usr/bin/env python3

def generate_commands(url, filename, server_type):
    print("\n📥 Generated Download Commands:\n")

    if server_type == "http":
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
        print(f'iwr -uri "{url}" -Outfile "{filename}"')
    elif server_type == "smb":
        # CMD commands for SMB
        print("🔹 CMD:")
        print(f'copy {url} {filename}')
        print(f'net use Z: {url.split("\\\\")[0] if url.startswith("\\\\") else url} && copy Z:\\{filename} . && net use Z: /delete')

        # PowerShell commands for SMB
        print("\n🔹 PowerShell:")
        print(f'Copy-Item "{url}" -Destination "{filename}"')
        print(f'New-PSDrive -Name Z -PSProvider FileSystem -Root "{url}"')
        print(f'Copy-Item "Z:\\{filename}" -Destination "."')
        print(f'Remove-PSDrive Z')

if __name__ == "__main__":
    server_type = input("Select server type (http/smb): ").strip().lower()
    url = input("Enter the download URL or IP: ").strip()
    port = input("Enter the port number (leave blank for default): ").strip()

    if server_type == "http":
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        if port:
            protocol, rest = url.split("//", 1)
            if "/" in rest:
                host, path = rest.split("/", 1)
                host = host.split(":")[0]
                url = f"{protocol}//{host}:{port}/{path}"
            else:
                host = rest.split(":")[0]
                url = f"{protocol}//{host}:{port}"
    elif server_type == "smb":
        if not url.startswith("\\\\"):
            url = "\\\\" + url
        if port:
            url = f"{url}:{port}"

    filename = input("Enter the save file name (with extension): ").strip()
    generate_commands(url, filename, server_type)
