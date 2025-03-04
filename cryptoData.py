#pip install requests
# pip install pycoingecko
import requests
from pycoingecko import CoinGeckoAPI


# ------------------------------------------------api version-----------------------------------------------------
# v url budu menit co chci hledat
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
# v headers je typ jakym chci dostat data a muj klic
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-wu1KPNzg4fZh245PPTCML8Fn\t"
}
# response zavola api get metodou
response = requests.get(url, headers=headers)

print(response.text)
# ------------------------------------------------api version-----------------------------------------------------

# ------------------------------------------------lib version-----------------------------------------------------
# startne coingecka
cg = CoinGeckoAPI()

# vezme prices podle ids a pozovna s vs
prices = cg.get_price(ids='bitcoin,ethereum', vs_currencies='usd')
print(prices)