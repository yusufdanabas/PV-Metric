import requests

URL = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"

parametreler = {
    "lat": 41.0,            # enlem (İstanbul)
    "lon": 29.0,            # boylam
    "peakpower": 1,         # 1 kWp'lik sistem -> sonuç doğrudan özgül verim olur
    "loss": 14,             # sistem kayıpları (%)
    "angle": 35,            # panel eğimi (derece)
    "aspect": 0,            # yön: 0 = tam güney
    "outputformat": "json", # cevabı JSON olarak iste
}

cevap = requests.get(URL, params=parametreler, timeout=30)
cevap.raise_for_status()
veri = cevap.json()

yillik_verim = veri["outputs"]["totals"]["fixed"]["E_y"]
print(f"Yıllık özgül verim: {yillik_verim:.0f} kWh/kWp")

print("\nAylık üretim (kWh/kWp):")
for ay in veri["outputs"]["monthly"]["fixed"]:
    print(f"  {ay['month']:2d}. ay: {ay['E_m']:.1f}")