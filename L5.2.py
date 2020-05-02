import requests
import matplotlib.pyplot as plt


def resource():
    BTC = (requests.get("https://bitbay.net/API/Public/BTC/Trades.json?sort=asc")).json()
    ETH = (requests.get("https://bitbay.net/API/Public/ETH/Trades.json?sort=asc")).json()
    LTC = (requests.get("https://bitbay.net/API/Public/LTC/Trades.json?sort=asc")).json()
    LSK = (requests.get("https://bitbay.net/API/Public/LSK/Trades.json?sort=asc")).json()
    GAME = (requests.get("https://bitbay.net/API/Public/GAME/Trades.json?sort=asc")).json()

    list_of_names = [BTC, ETH, LTC, LSK, GAME]

    list_BTC, list_ETH, list_LTC, list_LSK, list_GAME = ([] for i in range(5))

    for element in list_of_names:
        for item in element:
            if element == BTC:
                list_BTC.append(item['price'])
            elif element == ETH:
                list_ETH.append(item['price'])
            elif element == LTC:
                list_LTC.append(item['price'])
            elif element == LSK:
                list_LSK.append(item['price'])
            elif element == GAME:
                list_GAME.append(item['price'])

    BTC_variation, ETH_variation, LTC_variation, LSK_variation, GAME_variation = ([] for i in range(5))

    for i in range(len(list_BTC) - 1):
        BTC_variation.append(list_BTC[i+1] - list_BTC[i])
        ETH_variation.append(list_ETH[i+1] - list_ETH[i])
        LTC_variation.append(list_LTC[i+1] - list_LTC[i])
        LSK_variation.append(list_LSK[i+1] - list_LSK[i])
        GAME_variation.append(list_GAME[i+1] - list_GAME[i])

    list_of_variations = [BTC_variation, ETH_variation, LTC_variation, LSK_variation, GAME_variation]
    list_of_highs = []
    list_of_lows = []

    for element in list_of_variations:
        highs = 0
        lows = 0
        for i in range(len(element)):
            if element[i] >= 0:
                highs += i
            else:
                lows += i
        list_of_highs.append(highs)
        list_of_lows.append(lows)

    index_max_high = list_of_highs.index(max(list_of_highs))
    index_min_low = list_of_lows.index(min(list_of_lows))

    max_high = list_of_highs[index_max_high]
    min_low = list_of_lows[index_min_low]

    list_of_names_str = ["BTC", "ETH", "LTC", "LSK", "GAME"]

    plt.plot(BTC_variation, label="BTC")
    plt.plot(ETH_variation, label="ETH")
    plt.plot(LTC_variation, label="LTC")
    plt.plot(LSK_variation, label="LSK")
    plt.plot(GAME_variation, label="GAME")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Resource comparison")
    plt.show()

    return list_of_names_str[index_max_high], list_of_names_str[index_min_low], max_high, min_low


resource_name_1, resource_name_2, higest_value, lowest_value = resource()
print("The highest value is {}, and it's {}, the lowest value is {}, and it's {}".format(higest_value, resource_name_1, lowest_value, resource_name_2))
