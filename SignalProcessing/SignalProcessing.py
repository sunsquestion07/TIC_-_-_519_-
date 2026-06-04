import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

def plot_graph(y, x, title, xlabel, ylabel, filename):
    os.makedirs('figures', exist_ok=True)
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.grid(True)
    plt.savefig(f'figures/{filename}.png', dpi=600)
    plt.show()

n = 500
Fs = 1000
F_max = 50

t = np.arange(n) / Fs
random_signal = np.random.normal(0, 10, n)

w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')
filtered_signal = signal.sosfiltfilt(sos, random_signal)

plot_graph(filtered_signal, t, 'Фільтрований сигнал', 'Час (с)', 'Амплітуда', 'filtered_signal')

spectrum = np.abs(np.fft.fftshift(np.fft.fft(filtered_signal)))
freq = np.fft.fftshift(np.fft.fftfreq(n, 1/Fs))

plot_graph(spectrum, freq, 'Спектр сигналу', 'Частота (Гц)', 'Амплітуда', 'spectrum')