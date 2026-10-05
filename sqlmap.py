import sys
import requests
from colorama import init, Fore, Style

# Renkleri başlat
init(autoreset=True)

def banner():
    print(Fore.RED + """
███████  ██████  ██      ███    ███  █████  ██████  
██      ██    ██ ██      ████  ████ ██   ██ ██   ██ 
███████ ██    ██ ██      ██ ████ ██ ███████ ██████  
     ██ ██    ██ ██      ██  ██  ██ ██   ██ ██   ██ 
███████  ██████  ███████ ██      ██ ██   ██ ██████  
    """)
    print(Fore.YELLOW + "    [ SQL Injection Vulnerability Scanner ]")
    print(Fore.CYAN + "    [           GitHub: Counc             ]\n")

def check_sql_injection(url):
    if "=" not in url or "?" not in url:
        print(Fore.RED + "[!] Hata: URL bir parametre içermelidir (Örn: ?id=1)")
        return

    print(Fore.YELLOW + f"[*] Hedef taranıyor: {url}")
    
    # Test edilecek farklı payload'lar (enjeksiyon türleri)
    payloads = ["'", "\"", "' OR '1'='1"]
    
    sql_errors = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "sqlite3.operationalerror",
        "pg_query()",
        "sql syntax"
    ]

    vulnerable = False

    for payload in payloads:
        test_url = url + payload
        print(Fore.BLUE + f"[*] Test ediliyor -> {payload}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(test_url, headers=headers, timeout=10)
            
            page_content = response.text.lower()
            
            for error in sql_errors:
                if error in page_content:
                    vulnerable = True
                    print(Fore.GREEN + f"\n[+] AÇIK TESPİT EDİLDİ! Payload: {payload}")
                    print(Fore.GREEN + f"[+] Eşleşen Hata: {error}")
                    print(Fore.GREEN + f"[+] Riskli URL: {test_url}\n")
                    break
            if vulnerable:
                break

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] Bağlantı hatası: {e}")

    if not vulnerable:
        print(Fore.RED + "\n[-] Belirgin bir SQL açığına rastlanmadı (Hedef güvenli görünüyor).")

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input(Fore.CYAN + "Test edilecek URL'yi girin (Örn: http://site.com/index.php?id=1): ")
    
    check_sql_injection(target_url)
              
