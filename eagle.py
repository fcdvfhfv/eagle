import os
import pandas as pd
import subprocess

# ألوان التيرمينال لضبط الهيبة
Y = '\033[93m'
G = '\033[92m'
C = '\033[96m'
R = '\033[91m'
RS = '\033[0m'

def p_e():
    e = f"""
{Y}
             ___
            /   \\\\
       /\\\\ | . . | /\\\\
      /  \\\\|     |/  \\\\
     /    \\\\_---_/    \\\\
    /  /\\\\  \\   /  /\\\\  \\\\
   /  /  \\\\  \\ /  /  \\\\  \\\\
  /  /    \\\\  V  /    \\\\  \\\\
 /__/      \\\\___//      \\\\__\\
           [ B350 ]
{RS}
{C}=============================================
   🦅 B350 EAGLE RECON - NO KEYS MODE 🦅
============================================={RS}
    """
    print(e)

def r_c(c):
    try:
        # التشغيل عبر البروكسي لسحب البيانات بأمان
        p = subprocess.Popen(f"proxychains4 {c}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = p.communicate()
        return o.decode('utf-8', errors='ignore')
    except:
        return ""

def main():
    os.system('clear')
    p_e()
    
    t = input(f"{Y}ENTER TARGET DOMAIN (e.g. gov.il): {RS}")
    print(f"\n{R}[!] السحب بدأ.. الصقر يجمع الكومة الآن...{RS}\n")

    # 1. سحب بيانات الملكية (بدون مفتاح)
    d1 = r_c(f"whois {t}")
    
    # 2. سحب سجلات الـ DNS بالكامل
    d2 = r_c(f"dig {t} ANY +short")
    d2_full = r_c(f"dig {t} ANY")

    # 3. سحب النطاقات الفرعية (باستخدام محركات البحث العامة مباشرة)
    print(f"{G}[*] جاري استخراج النطاقات الفرعية...{RS}")
    r_c(f"sublist3r -d {t} -o .tmp")
    try:
        with open(".tmp", "r") as f: d3 = f.read()
        os.remove(".tmp")
    except: d3 = "لم يتم العثور على نطاقات فرعية."

    # 4. سحب معلومات السيرفر والإيميلات (Dmitry)
    print(f"{G}[*] جاري سحب الإيميلات والـ IPs...{RS}")
    d4 = r_c(f"dmitry -iwnse {t}")

    # 5. سحب بيانات الاستجابة (Header Analysis)
    d5 = r_c(f"curl -I -s {t}")

    # تجميع الكومة في الإكسل
    res = [
        ["Whois Data", d1],
        ["DNS Summary", d2],
        ["DNS Full Records", d2_full],
        ["Subdomains List", d3],
        ["Deep Intel (Dmitry)", d4],
        ["HTTP Header (Server Info)", d5]
    ]
    
    df = pd.DataFrame(res, columns=["Category", "Raw_Data"])
    f_n = f"B350_Full_Dump_{t}.xlsx"
    df.to_excel(f_n, index=False)

    print(f"\n{Y}=============================================")
    print(f"✅ انتهى السحب! الكومة جاهزة في: {f_n}")
    print(f"============================================={RS}")

if __name__ == "__main__":
    main()
