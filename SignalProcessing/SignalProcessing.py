import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os


def plot_graph(y, x, title, xlabel, ylabel, filename):
    os.makedirs('figures', exist_ok=True)
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.grid(True)
    plt.savefig(f'figures/{filename}.png', dpi=600)
    plt.show()


# =====================================================
# ПРАКТИЧНА РОБОТА №2 - ГЕНЕРАЦІЯ СИГНАЛУ
# =====================================================

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
freq = np.fft.fftshift(np.fft.fftfreq(n, 1 / Fs))

plot_graph(spectrum, freq, 'Спектр сигналу', 'Частота (Гц)', 'Амплітуда', 'spectrum')

# =====================================================
# ПРАКТИЧНА РОБОТА №3 - ДИСКРЕТИЗАЦІЯ
# =====================================================

steps = [2, 4, 8, 16]

discrete_signals = []
discrete_spectrums = []
reconstructed_signals = []
variances = []
snr_values = []

for Dt in steps:
    discrete_signal = np.zeros(n)
    for i in range(0, n, Dt):
        discrete_signal[i] = filtered_signal[i]
    discrete_signals.append(discrete_signal)

    spectrum_discrete = np.abs(np.fft.fftshift(np.fft.fft(discrete_signal)))
    discrete_spectrums.append(spectrum_discrete)

    w_recon = F_max / (Fs / 2)
    sos_recon = signal.butter(3, w_recon, 'low', output='sos')
    reconstructed = signal.sosfiltfilt(sos_recon, discrete_signal)
    reconstructed_signals.append(reconstructed)

    error = reconstructed - filtered_signal
    var_error = np.var(error)
    var_signal = np.var(filtered_signal)
    variances.append(var_error)
    snr = var_signal / var_error if var_error > 0 else float('inf')
    snr_values.append(snr)

# Графіки дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(t, discrete_signals[s], linewidth=1)
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=14)
        ax[i, j].grid(True)
        s += 1
fig.supxlabel('Час (с)', fontsize=14)
fig.supylabel('Амплітуда', fontsize=14)
fig.suptitle('Дискретизовані сигнали', fontsize=14)
plt.tight_layout()
plt.savefig('figures/discrete_signals.png', dpi=600)
plt.show()

# Графіки спектрів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(freq, discrete_spectrums[s], linewidth=1)
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=14)
        ax[i, j].grid(True)
        s += 1
fig.supxlabel('Частота (Гц)', fontsize=14)
fig.supylabel('Амплітуда', fontsize=14)
fig.suptitle('Спектри дискретизованих сигналів', fontsize=14)
plt.tight_layout()
plt.savefig('figures/discrete_spectrums.png', dpi=600)
plt.show()

# Графіки відновлених сигналів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(t, reconstructed_signals[s], linewidth=1, label='Відновлений')
        ax[i, j].plot(t, filtered_signal, 'r--', linewidth=1, label='Оригінал')
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=14)
        ax[i, j].grid(True)
        ax[i, j].legend()
        s += 1
fig.supxlabel('Час (с)', fontsize=14)
fig.supylabel('Амплітуда', fontsize=14)
fig.suptitle('Відновлені сигнали', fontsize=14)
plt.tight_layout()
plt.savefig('figures/reconstructed_signals.png', dpi=600)
plt.show()

# Дисперсія від кроку дискретизації
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(steps, variances, 'bo-', linewidth=1)
plt.xlabel('Крок дискретизації Dt', fontsize=14)
plt.ylabel('Дисперсія помилки', fontsize=14)
plt.title('Залежність дисперсії від кроку дискретизації', fontsize=14)
plt.grid(True)
plt.savefig('figures/variance_vs_dt.png', dpi=600)
plt.show()

# SNR від кроку дискретизації
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(steps, snr_values, 'gs-', linewidth=1)
plt.xlabel('Крок дискретизації Dt', fontsize=14)
plt.ylabel('Відношення сигнал/шум (SNR)', fontsize=14)
plt.title('Залежність SNR від кроку дискретизації', fontsize=14)
plt.grid(True)
plt.savefig('figures/snr_vs_dt.png', dpi=600)
plt.show()