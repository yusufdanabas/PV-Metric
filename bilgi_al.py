import math
import requests

PVGIS_URL = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"


def sayi_al(mesaj, varsayilan):
    """Kullanıcıdan sayı ister. Boş bırakırsa varsayılanı kullanır."""
    while True:
        giris = input(f"{mesaj} [{varsayilan}]: ").strip()
        if giris == "":
            return varsayilan
        try:
            return float(giris.replace(",", "."))
        except ValueError:
            print("  Lütfen geçerli bir sayı gir (örnek: 4.5).")


def pvgis_verim_al(enlem, boylam, egim, yon, kayip):
    """PVGIS'ten 1 kWp'lik sistemin yıllık üretimini (kWh/kWp) çeker."""
    parametreler = {
        "lat": enlem,
        "lon": boylam,
        "peakpower": 1,
        "loss": kayip,
        "angle": egim,
        "aspect": yon,
        "outputformat": "json",
    }
    try:
        cevap = requests.get(PVGIS_URL, params=parametreler, timeout=30)
        cevap.raise_for_status()
        veri = cevap.json()
        return veri["outputs"]["totals"]["fixed"]["E_y"]
    except (requests.RequestException, KeyError, ValueError) as hata:
        print(f"  PVGIS'ten veri alınamadı: {hata}")
        return None


def sistem_boyutlandir(aylik_kwh, verim, panel_wp):
    yillik_kwh = aylik_kwh * 12
    gerekli_kwp = yillik_kwh / verim
    panel_sayisi = math.ceil(gerekli_kwp * 1000 / panel_wp)
    gercek_kwp = panel_sayisi * panel_wp / 1000
    return yillik_kwh, gerekli_kwp, panel_sayisi, gercek_kwp


def geri_odeme(gercek_kwp, maliyet_kwp, verim, birim_fiyat):
    toplam_maliyet = gercek_kwp * maliyet_kwp
    yillik_tasarruf = gercek_kwp * verim * birim_fiyat
    sure_yil = toplam_maliyet / yillik_tasarruf
    return toplam_maliyet, yillik_tasarruf, sure_yil


print("=== PVMetric: Güneş Paneli Hesaplayıcı ===")
print("(Enter'a basarsan köşeli parantezdeki değer kullanılır)\n")

print("--- Konum ve panel yerleşimi ---")
enlem = sayi_al("Enlem", 41.0)
boylam = sayi_al("Boylam", 29.0)
egim = sayi_al("Panel eğimi (derece)", 35)
yon = sayi_al("Yön (0=güney, -90=doğu, 90=batı)", 0)
kayip = sayi_al("Sistem kayıpları (%)", 14)

print("\n--- Tüketim ve maliyet ---")
aylik_tuketim_kwh = sayi_al("Aylık tüketim (kWh)", 300)
panel_gucu_wp = sayi_al("Panel gücü (Wp)", 550)
kurulum_maliyeti_kwp = sayi_al("Kurulum maliyeti (TL/kWp)", 30000)
elektrik_birim_fiyat = sayi_al("Elektrik birim fiyatı (TL/kWh)", 4.0)

print("\nPVGIS'ten veri çekiliyor...")
ozgul_verim = pvgis_verim_al(enlem, boylam, egim, yon, kayip)

if ozgul_verim is None:
    ozgul_verim = sayi_al("Özgül verimi elle gir (kWh/kWp/yıl)", 1300)
else:
    print(f"PVGIS özgül verim  : {ozgul_verim:.0f} kWh/kWp/yıl")

yillik, gerekli, panel_adet, gercek = sistem_boyutlandir(
    aylik_tuketim_kwh, ozgul_verim, panel_gucu_wp
)
maliyet, tasarruf, sure = geri_odeme(
    gercek, kurulum_maliyeti_kwp, ozgul_verim, elektrik_birim_fiyat
)

print("\n--- SONUÇ ---")
print(f"Yıllık tüketim     : {yillik:,.0f} kWh")
print(f"Gerekli güç        : {gerekli:.2f} kWp")
print(f"Panel sayısı       : {panel_adet} adet ({gercek:.2f} kWp kurulu)")
print(f"Toplam maliyet     : {maliyet:,.0f} TL")
print(f"Yıllık tasarruf    : {tasarruf:,.0f} TL")
print(f"Basit geri ödeme   : {sure:.1f} yıl")