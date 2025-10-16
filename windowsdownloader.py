#!/usr/bin/env python3

def generate_commands(url, filename, server_type):
    print("\n📥 Generated Download Commands:\n")

    if server_type == "http":
        # CMD commands
        print("🔹 CMD:")
        print(f'wget {url}/{filename} -O {filename}')
        print(f'curl -O {url}/{filename}')
        print(f'certutil -urlcache -split -f {url}/{filename} {filename}')
        print(f'bitsadmin /transfer myDownloadJob {url}/{filename} {filename}')

        # PowerShell commands
        print("\n🔹 PowerShell:")
        print(f'Invoke-WebRequest -Uri "{url}/{filename}" -OutFile "{filename}"')
        print(f'Start-BitsTransfer -Source "{url}/{filename}" -Destination "{filename}"')
        print(f'$client = New-Object System.Net.WebClient; $client.DownloadFile("{url}/{filename}", "{filename}")')
        print(f'iwr -uri "{url}/{filename}" -Outfile "{filename}"')

    elif server_type == "smb":
        # CMD commands for SMB
        print("🔹 CMD:")

        # Precompute share name to avoid f-string backslash issues
        share = url.split("\\\\")[0] if url.startswith("\\\\") else url

        print(f'copy {url}\\{filename} {filename}')
        print(f'net use Z: {share} && copy Z:\\{filename} . && net use Z: /delete')

        # PowerShell commands for SMB
        print("\n🔹 PowerShell:")
        print(f'Copy-Item "{url}\\{filename}" -Destination "{filename}"')
        print(f'New-PSDrive -Name Z -PSProvider FileSystem -Root "{url}"')
        print(f'Copy-Item "Z:\\{filename}" -Destination "."')
        print('Remove-PSDrive Z')


if __name__ == "__main__":
    server_type_input = input("Select server type (1 for http, 2 for smb): ").strip()
    if server_type_input == "1":
        server_type = "http"
    elif server_type_input == "2":
        server_type = "smb"
    else:
        print("Invalid selection. Defaulting to http.")
        server_type = "http"

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
