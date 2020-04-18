import requests as rq
import time as t


def connect_API(url, params, pprint=None, *args):
    waluta, kategoria = params
    url += '{}{}/{}.json'.format(waluta[0], waluta[1], kategoria)
    if args:
        if len(args) == 1:
            url += '?since={}'.format(args[0])
        else:
            url += '?sort={}'.format(args[1])
    response = rq.get(url).json()

    if pprint:
        print("Bids: \n{}".format(response['bids']))
        print("Asks: \n{}".format(response['asks']))

    return response


def main():
    params = [['BTC', 'USD'], 'orderbook']
    url = "https://bitbay.net/API/Public/"
    connect_API(url, params, True)

    loops = int(input("\nHow many executes(for infinite loop '0'): "))
    params[-1] = 'ticker'
    inf = True if loops == 0 else False

    while True:
        if not inf and loops > 0:
            loops -= 1
        response = connect_API(url, params)
        ratio = 1 - (response['ask'] - response['bid']) / response['bid']
        print()
        print("Ratio between bid and ask: {:.5f} %".format(ratio * 100))
        if not inf and loops == 0:
            break
        t.sleep(5)


if __name__ == '__main__':
    main()
