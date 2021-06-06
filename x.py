from itertools import count
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    plt.cla()
    plt.plot(x_vals, y_vals)


ani = FuncAnimation(plt.gcf(), animate, interval=1000)


plt.tight_layout()
plt.show()
# ------------------------------------------------
# from datetime.datetime import datetime.datetime, timezone
import datetime
from dateutil.tz import tzlocal
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from numpy import double
import json
from binance.client import Client

load_dotenv()

# Global variables
sec = 1
BASE_PATH = os.getcwd()

# logging in to the acc using API key n secret
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))


# Extracting my assests, i.e., my crpyto I have
UTC = datetime.timezone.utc

file_path = f'{BASE_PATH}/value.txt'
TIME_NOW = datetime.datetime.now(tzlocal())
one_sec = datetime.timedelta(seconds=1)


if os.path.isfile(file_path):
    os.remove(file_path)
# else:
f = open(file_path, 'w+')
f.write(f'# {TIME_NOW}\n\n')
f.close()


def all_assests_info():
    global TIME_NOW
    my_assests = []
    total_assetsvalue = double()

    get_acc_obj = client.get_account()
    acc_balance = get_acc_obj['balances']

    for i in range(len(acc_balance)):
        q = double(acc_balance[i]['free'])
        if q != 0:
            if acc_balance[i]["asset"] == 'USDT':
                continue
            try:
                assest_avg_price = client.get_avg_price(
                    symbol=f'{acc_balance[i]["asset"]}USDT'
                )
                assest_avg_price = double(assest_avg_price['price'])
                assest_quantity = double(acc_balance[i]['free'])
                total_assetsvalue += assest_avg_price*assest_quantity
            except Exception as e:
                print(e)
                continue

            crypto_info = {
                'SYMBOL': f'{acc_balance[i]["asset"]}',
                'VALUE': assest_quantity,
                'CURR_RATE': assest_avg_price
            }
            my_assests.append(crypto_info)

    with open('value.txt', 'a') as f:
        tmp = TIME_NOW.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{tmp},{total_assetsvalue}\n')
        f.close()
    TIME_NOW += one_sec
    return my_assests


plt.style.use('seaborn')

xs = []
ys = []


def animate(i):
    val = all_assests_info()
    lines = open('value.txt', 'r').readlines()
    lines = lines[2:]

    for line in lines:
        if len(line) > 1:
            # try:
            x, y = line.split(',')
            x = datetime.datetime.now(tzlocal())
            # y = y[:-1]
            xs.append(x)
            ys.append(float(y))
    plt.cla()
    plt.title('REALTIME INVESTMENT GRAPH')
    plt.xlabel('DATE')
    plt.xlabel('INVESTED')

    plt.plot_date(xs, ys, linestyle='solid', ms=0)
    # plt.tight_layout()

    # plt.xticks(rotation=90)
    # ax1.set_ylim(min(ys)-.05, max(ys)+.05)  # added ax attribute here
    # plt.plot(xs, ys)
    # plt.set(
    # title="REALTIME INVESTMENT GRAPH",
    # xlabel=f"Time(in sec) from {TIME_NOW.strftime('%H:%M:%S')}",
    # ylabel="INVESTED AMOUNT IN USDT"
    # )
    # # added ax attribute here
    # # ax1.set_xlim(min(xs), max(xs)+one_sec)
    # ax1.plot(xs, ys)


# fig = plt.figure()
# fig.autofmt_xdate()
# ax1 = fig.add_subplot(1, 1, 1)

# plt.fig.set(
#     title="REALTIME INVESTMENT GRAPH",
#     xlabel=f"Time(in sec) from {TIME_NOW.strftime('%H:%M:%S')}",
#     ylabel="INVESTED AMOUNT IN USDT"
# )

ani = FuncAnimation(plt.gcf(), animate, interval=2000)
plt.show()
