from main import get_data, model, stats

name = input("Choose your crypto (ETC, DASH, XMR): ")

crypto = get_data(name)
model(crypto)
stats(crypto)
