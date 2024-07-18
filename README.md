When you conquer the world, remember this day my friend.

Here's a colorful `README.md` using Markdown with some emoji and formatting to make it visually appealing:


# 🌈 Nydra 🌈

**Nydra** is a powerful tool for scanning subnets and brute-forcing various network services using `nmap` and `hydra`. This script helps identify open ports and attempts to gain access using specified usernames and passwords.

---

## 🚀 Features

- **🔍 Scans multiple subnets for open ports.**
- **💻 Supports various services:**
  - SSH
  - FTP
  - RDP
  - SMB
  - HTTP
  - HTTPS
  - MySQL
  - PostgreSQL
  - Telnet
  - VNC
  - MSSQL
  - Redis
- **📁 Input usernames and passwords from files or as single entries.**
- **⚙️ Flexible command-line arguments for easy usage.**

---

## 📋 Requirements

- **Python 3.x**
- **`nmap` installed on your system**
- **`hydra` installed on your system**

### Installation of Dependencies

You can install required packages using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

Run the script from the command line with the following options:

```bash
python nydra.py -s <subnet_file_or_single_subnet> -u <username_file_or_single_username> -p <password_file_or_single_password> -S <service>
```

### Example Commands

1. **Using files:**
   ```bash
   python nydra.py -s subnet.txt -u usernames.txt -p passwords.txt -S ssh
   ```

2. **Using single entries:**
   ```bash
   python nydra.py -s 192.168.1.0/24 -u admin -p password123 -S ssh
   ```

---

## 📂 Input Files

- **`subnet.txt`**: A file containing a list of subnets to scan (e.g., `192.168.1.0/24`).
- **`usernames.txt`**: A file containing a list of usernames or a single username.
- **`passwords.txt`**: A file containing a list of passwords or a single password.

---

## 🛡️ Supported Services

| **Service**      | **Port** |
|------------------|----------|
| SSH              | 22       |
| FTP              | 21       |
| RDP              | 3389     |
| SMB              | 445      |
| HTTP             | 80       |
| HTTPS            | 443      |
| MySQL            | 3306     |
| PostgreSQL       | 5432     |
| Telnet           | 23       |
| VNC              | 5900     |
| MSSQL            | 1433     |
| Redis            | 6379     |

---

## ⚠️ Important Note

**This script is intended for educational purposes only. It should only be used in environments where you have explicit permission to perform such actions. Unauthorized access to systems is illegal and unethical. Always follow best practices and laws related to cybersecurity.**

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Feel free to adjust any of the emojis or sections to better fit your style!
