import requests
from bs4 import BeautifulSoup
import re
import time
import ccxt
with open("api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'leverage' : 1
    }
})
sybmol = ""
my_balance = binance.fetch_balance(params = {"type" : "future"})
balance = my_balance['USDT']['total']

my_coins = ["YFIUSDT" , "MKRUSDT" , "DEFIUSDT" , "FOOTBALLUSDT" , "BNBUSDT" , "XMRUSDT" , "QNTUSDT" , "LTCUSDT" , "TRBUSDT" , 
"COMPUSDT" , "GMXUSDT" , "DASHUSDT" , "ZECUSDT" ,
"KSMUSDT" , "SSVUSDT" , "NMRUSDT" , "ZENUSDT" , "INJUSDT" , "UNFIUSDT" , "BLUEBIRDUSDT" , "LPTUSDT" , "FXSUSDT" , "XVSUSDT" , "CYBERUSDT", "ANTUSDT", "UNIUSDT",
"ARUSDT", "FILUSDT", "BALUSDT" , "ICPUSDT", "CVXUSDT" , "RUNEUSDT", "SNXUSDT" , "DYDXUSDT", "RNDRUSDT",
"LDOUSDT" , "WLDUSDT", "TOMOUSDT", "UMAUSDT", "OPUSDT", "RADUSDT", "HIGHUSDT","GALUSDT","LQTYUSDT","APEUSDT",
"BANDUSDT","API3USDT" , "RLCUSDT", "GTCUSDT" ,"HOOKUSDT", "LITUSDT", "ALICEUSDT", 
"PENDLEUSDT" ,  "PHBUSDT" ,"BELUSDT", "COMBOUSDT", "SFPUSDT", "SUSHIUSDT",
"PERPUSDT", "MAGICUSDT", "CRVUSDT", "OMGUSDT", "STGUSDT", "EDUUSDT","CTKUSDT",
"CELOUSDT", "BNTUSDT", "ARKMUSDT",  "HFTUSDT", "FRONTUSDT", "OCEANUSDT",
"JOEUSDT" , "RDNTUSDT", "YGGUSDT" , "BICOUSDT", "ENJUSDT", "FETUSDT" , "BNXUSDT" ,  "FTMUSDT",
"IDUSDT" ,"WOOUSDT", "AGIXUSDT" , "LRCUSDT" , 
"C98USDT" , "AUDIOUSDT" , "BLZUSDT" , "CFXUSDT" , "BAKEUSDT", "CTSIUSDT", "OGNUSDT",  "KLAYUSDT" , "XLMUSDT", "DUSKUSDT",
"DODOXUSDT" , "CHRUSDT" , "DARUSDT" ,  "NKNUSDT" , "ATAUSDT" , "FLMUSDT" , "ALPHAUSDT", "OXTUSDT",
"IDEXUSDT" , "MDTUSDT" , "RENUSDT", "ARPAUSDT" ,
"TRUUSDT" , "COTIUSDT" , "XEMUSDT" , "SKLUSDT" , "1000FLOKIUSDT" , "IOTXUSDT" ,
"GALAUSDT" , "RVNUSDT" , "ACHUSDT" , "CELRUSDT", "LINAUSDT" , "AMBUSDT" , "TLMUSDT", "PEOPLEUSDT" , "ONEUSDT" ,
"DGBUSDT" , "KEYUSDT" , "XVGUSDT" , "JASMYUSDT" , "CKBUSDT" , "RSRUSDT" , "LEVERUSDT", "REEFUSDT" , "HOTUSDT" , "1000PEPEUSDT",
"DENTUSDT" , "SPELLUSDT"]
while True:
    url = "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general"
    response = requests.get(url)
    data = response.json()

    latest_notice_title = data['data']['list'][0]['title']
    #latest_notice_title ="[거래] KRW 마켓 디지털 자산 추가 (CKB)" #테스트할때 앞에 맨앞에(latest앞 #) #삭제하고 ()안에 코인 넣어서 테스트
    if "[거래] KRW 마켓 디지털 자산 추가" in latest_notice_title:
        match = re.search(r'\((.*?)\)', latest_notice_title)
        if match:
            added_digital_asset = match.group(1)
            print(f"추가된 디지털 자산: {added_digital_asset}")
            symbol = added_digital_asset + "USDT"
            print(symbol)
            
        if symbol in my_coins: #롱칠때 
            coin_price = binance.fetch_ticker(symbol)
            coin_last_price = coin_price['last']
            buy_amount = coin_last_price * (balance * 0.5) #코인 가격 x 내가가진 잔고 x 0.5
            binance.create_market_buy_order(symbol = symbol , amount = buy_amount)
            break
        #if symbol in my_coins: #숏칠거면 주석 삭제하고 쓰기 / 위에 if symbol in coins 부터 break까지 줄은 ctrl + / 으로 주석처리
            #coin_price = binance.fetch_ticker(symbol)
            #coin_last_price = coin_price['last']
            #buy_amount = coin_last_price * (balance * 0.5) #코인 가격 x 내가가진 잔고 x 0.5
            #binance.create_market_sell_order(symbol=symbol , amount = buy_amount)
            #break
        else:
            print("디지털 자산 추가 정보를 찾을 수 없습니다.")
    else:
        print(latest_notice_title)
    print(balance)
    time.sleep(0.5)