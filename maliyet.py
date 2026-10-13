import csv

KDV_ORANI = 0.20  # VARSAYIM: gerçek oranı teklif/faturadan teyit et

# Her kalemin sürücüsü: "kwp", "panel" veya "sabit". Fiyatlar KDV HARİÇ.
KALEMLER = [
    {"ad": "İnverter",                     "surucu": "kwp",   "birim_fiyat": 2178},
    {"ad": "DC/AC kablo ve koruma",        "surucu": "kwp",   "birim_fiyat": 995},
    {"ad": "Konstrüksiyon + işçilik",      "surucu": "panel", "birim_fiyat": 5555},
    # VARSAYIM: proje 45.000 + nakliye/devreye alma 15.000 (tablodan, KDV durumu belirsiz)
    {"ad": "Proje, nakliye, devreye alma", "surucu": "sabit", "birim_fiyat": 60000},
]


def panelleri_yukle(dosya="paneller.csv"):
    """CSV'yi okuyup her panel için bir sözlük içeren liste döndürür."""
    paneller = []
    with open(dosya, newline="", encoding="utf-8-sig") as f:
        for satir in csv.DictReader(f):
            paneller.append({
                "model": satir["model"],
                "wp": float(satir["wp"]),
                "boy_mm": float(satir["boy_mm"]),
                "en_mm": float(satir["en_mm"]),
                "verim": float(satir["verim"]),
                "sicaklik_kats": float(satir["sicaklik_kats"]),
                "fiyat_tl": float(satir["fiyat_tl"]),
            })
    return paneller


def panel_disi_maliyet(kwp, panel_adedi):
    """Her kalemi sürücüsüne göre hesaplar. (toplam, detay listesi) döndürür."""
    toplam = 0
    detay = []
    for kalem in KALEMLER:
        if kalem["surucu"] == "kwp":
            miktar = kwp
        elif kalem["surucu"] == "panel":
            miktar = panel_adedi
        else:  # "sabit"
            miktar = 1
        tutar = kalem["birim_fiyat"] * miktar
        detay.append((kalem["ad"], tutar))
        toplam += tutar
    return toplam, detay


def sistem_maliyeti(panel, panel_adedi):
    """Seçilen panel ve adet için toplam maliyeti hesaplar."""
    kwp = panel_adedi * panel["wp"] / 1000
    panel_toplam = panel_adedi * panel["fiyat_tl"]
    disi_toplam, detay = panel_disi_maliyet(kwp, panel_adedi)
    haric = panel_toplam + disi_toplam
    kdv = haric * KDV_ORANI
    return {
        "kwp": kwp,
        "panel_toplam": panel_toplam,
        "panel_disi": disi_toplam,
        "detay": detay,
        "haric": haric,
        "kdv": kdv,
        "dahil": haric + kdv,
    }


if __name__ == "__main__":
    # Bu blok sadece "python maliyet.py" ile doğrudan çalıştırınca devreye girer.
    for p in panelleri_yukle():
        s = sistem_maliyeti(p, 36)
        print(f"{p['model']}")
        print(f"  {s['kwp']:.2f} kWp | KDV hariç {s['haric']:,.0f} TL | "
              f"KDV dahil {s['dahil']:,.0f} TL | {s['dahil'] / s['kwp']:,.0f} TL/kWp")