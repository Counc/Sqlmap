import sys
import requests
from colorama import init, Fore, Style
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Renkleri başlat
init(autoreset=True)

def banner():
    print(Fore.RED + Style.BRIGHT + """
  ███████╗ ██████╗ ██╗     ███╗   ███╗ █████╗ ██████╗ 
  ██╔════╝██╔═══██╗██║     ████╗ ████║██╔══██╗██╔══██╗
  ███████╗██║   ██║██║     ██╔████╔██║███████║██████╔╝
  ╚════██║██║   ██║██║     ██║ ╚═╝ ██║██╔══██║██╔══██╗
  ███████║╚██████╔╝███████╗██║     ██║██║  ██║██████╔╝
  ╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ 
    """)
    print(Fore.YELLOW + "    [ SQL Injection Vulnerability Scanner ]")
    print(Fore.CYAN + "    [          GitHub: Counc            ]\n")
          

def scan_sql_injection(target_url):
    # Tarayıcı gibi görünmek için Headers ekleyelim (Engellenmeyi önler)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Test edilecek yaygın SQL enjeksiyon payload'ları
    payloads = [
        "'",
        "\"",
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1 --",
        "' AND 1=1 --"
    ]

    # Veritabanı hata mesajları (Açık olduğunu gösteren ipuçları)
    sql_errors = [
        "sql syntax",
        "mysql_fetch",
        "syntax error",
        "unclosed quotation mark",
        "odbc_driver",
        "sqlite3.operationalerror",
        "pg_query"
    ]

    print(Fore.BLUE + f"[*] Hedef taranıyor: {target_url}\n")

    vulnerable = False

    for payload in payloads:
        print(Fore.YELLOW + f"[*] Test ediliyor -> {payload}")
        
        # URL'yi manipüle edip payload ekleme mantığı
        parsed_url = urlparse(target_url)
        query_params = parse_qs(parsed_url.query)

        if not query_params:
            print(Fore.RED + "[-] Hata: URL içinde test edilebilecek bir parametre (örn: ?id=1) bulunamadı!")
            return

        # Parametrelerin sonuna payload ekleyelim
        modified_params = query_params.copy()
        for key in modified_params:
            modified_params[key] = [val + payload for val in modified_params[key]]

        # Yeni URL'yi oluşturalım
        encoded_query = urlencode(modified_params, doseq=True)
        test_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query,
            parsed_url.fragment
        ))

        try:
            # İstek atma (Timeout ve Headers korumalı)
            response = requests.get(test_url, headers=headers, timeout=10)
            
            # Gelen sayfada SQL hata mesajı arayalım
            page_content = response.text.lower()
            found_error = False
            for error in sql_errors:
                if error in page_content:
                    found_error = True
                    break

            if found_error:
                print(Fore.GREEN + Style.BRIGHT + f"[+] SQL AÇIĞI TESPİT EDİLDİ! Payload: {payload}")
                print(Fore.GREEN + f"[+] Riskli URL: {test_url}\n")
                vulnerable = True
                break
        
        except requests.exceptions.Timeout:
            print(Fore.RED + "[!] Bağlantı zaman aşımına uğradı (Timeout). Sunucu çok yavaş veya engelliyor.")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] Bağlantı hatası: {e}")

    if not vulnerable:
        print(Fore.RED + "\n[-] Tarama tamamlandı. Belirtilen parametrede bariz bir SQL açığı bulunamadı veya site korumalı.")

if __name__ == "__main__":
    banner()
    url = input(Fore.CYAN + "Test edilecek URL'yi girin (Örn: http://site.com/index.php?id=1): " + Style.RESET_ALL)
    if url.strip():
        scan_sql_injection(url.strip())
    else:
        print(Fore.RED + "Geçerli bir URL girmelisiniz!")
  
