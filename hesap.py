import math


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

aylik_tuketim_kwh = sayi_al("Aylık tüketim (kWh)", 300)
ozgul_verim = sayi_al("Özgül verim (kWh/kWp/yıl)", 1300)
panel_gucu_wp = sayi_al("Panel gücü (Wp)", 550)
kurulum_maliyeti_kwp = sayi_al("Kurulum maliyeti (TL/kWp)", 30000)
elektrik_birim_fiyat = sayi_al("Elektrik birim fiyatı (TL/kWh)", 4.0)

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