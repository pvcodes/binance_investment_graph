import datetime
from dateutil.tz import tzlocal

# from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from numpy import double

from binance.client import Client

load_dotenv()

# logging in to the acc using API key n secret
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))


# Extracting my assests, i.e., my crpyto I have

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

    return my_assests, total_assetsvalue


# For storing plotting points
x_ax1 = []
y_ax1 = []


def animate(i):

    val, assest_val = all_assests_info()
    x = datetime.datetime.now(tzlocal())
    x_ax1.append(x)
    y_ax1.append(double(assest_val))

    ax1.cla()
    ax1.ticklabel_format(useOffset=False)
    ax1.set_title('REALTIME INVESTMENT GRAPH')
    ax1.set_xlabel('Time----------------------------->')
    ax1.set_ylabel('Invested USDT----------------------------->')
    ax1.plot_date(x_ax1, y_ax1, linestyle='solid', ms=0)

    x_ax2 = []
    y_ax2 = []
    explode = []
    for x in val:
        # print('1')
        x_ax2.append(x['SYMBOL'])
        y_ax2.append(double(x['VALUE'])*double(x['CURR_RATE']))
        explode.append(.05)

    ax2.cla()
    ax2.pie(y_ax2, labels=x_ax2, autopct='%1.1f%%', explode=explode)
    # ax2.plot_date(x_ax1, y_ax1, linestyle='solid', ms=0)


plt.style.use('seaborn')
fig = plt.figure()

ax1 = fig.add_axes([.05, .05, .9, .9])  # line chart axes
ax2 = fig.add_axes([.8, .75, .2, .2])  # pie chart axes

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Pranjal Verma',
                # visit_me='https://pvcodes.in'), bitrate=1800)


ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)

plt.show()
# plt.tight_layout()
# ani.save('im.mp4', writer=writer)
