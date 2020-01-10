import numpy as np
import talib as tl

from mpl_finance import candlestick2_ochl, volume_overlay
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation


def add_BBands(ax, closes):
    upperband, middleband, lowerband  = tl.BBANDS(
    # close narray
    closes,
    # time default 20
    timeperiod=20,
    # number of non-biased standard deviations from the mean
    nbdevup=2,
    nbdevdn=2,
    # Moving average type: simple moving average here
    matype=0)

    params = dict(c='#736bd2', ls='-', linewidth=1)
    idx = np.arange(closes.size)

    ax.plot(idx, upperband, **params)
    ax.plot(idx, middleband, **params)
    ax.plot(idx, lowerband, **params)

    ax.fill_between(idx, lowerband, upperband, facecolor='#ecfb07', alpha=0.3)


def add_volume(ax, open, close, vol):
    volume_params = dict(colorup='g', alpha=0.5, width=1)

    bc = volume_overlay(ax, open, close, vol, **volume_params)
    ax.add_collection(bc)

    idx = np.arange(vol.size)
    sma = tl.SMA(vol, 20)
    sma *= 2

    sma_params = dict(c='#0f07f9', ls='-', linewidth=1)
    ax.plot(idx, sma, **sma_params)

    ax.fill_between(idx, 0, sma, facecolor='#07f2f9', alpha=0.3)


def plot(klines, symbol, fig=None):

    style.use('fivethirtyeight')

    _, opens, highs, lows, closes, volumes = klines.columns

    # Create figure
    if fig is None:
        fig = plt.figure()
    else:
        fig.clear()

    ax1 = fig.add_subplot(111)

    candlestick2_ochl(ax1, opens, closes, highs, lows, width=1, colorup='g')
    ax1.set_ylim(lows.min() - lows.min() / 50)

    # Add a seconds axis for the volume overlay
    ax2 = ax1.twinx()
    ax2.set_ylim(0, 5 * volumes.max())
    ax2.grid(False)

    add_volume(ax2, opens, closes, volumes)
    #add_BBands(ax1, closes)

    plt.title(symbol)
    fig.savefig(r'C:\graphs\{}.png'.format(symbol), format='png',
                dpi=400)
    #plt.show()


def animate_plot(klines, symbol, window=50):
    fig = plt.figure()

    anim_running = True

    def onClick(event):
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    def animate(i):
        plot(klines, symbol, fig, i, i + window)

    fig.canvas.mpl_connect('button_press_event', onClick)

    anim = animation.FuncAnimation(fig, animate, interval=500, frames=range(klines.size - window), repeat=False)
    plt.show()

