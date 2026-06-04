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
# =====================================================
# ПРАКТИЧНА РОБОТА №3 - ДИСКРЕТИЗАЦІЯ
# =====================================================

# Кроки дискретизації
steps = [2, 4, 8, 16]

# Списки для збереження результатів
discrete_signals = []
discrete_spectrums = []
reconstructed_signals = []
variances = []
snr_values = []

for Dt in steps:
    # 1. Дискретизація (прорідження)
    discrete_signal = np.zeros(n)
    for i in range(0, n, Dt):
        discrete_signal[i] = filtered_signal[i]
    discrete_signals.append(discrete_signal)

    # 2. Спектр дискретизованого сигналу
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(discrete_signal)))
    discrete_spectrums.append(spectrum)

    # 3. Відновлення аналогового сигналу (ФНЧ)
    w_recon = F_max / (Fs / 2)
    sos_recon = signal.butter(3, w_recon, 'low', output='sos')
    reconstructed = signal.sosfiltfilt(sos_recon, discrete_signal)
    reconstructed_signals.append(reconstructed)

    # 4. Розрахунок дисперсії та SNR
    error = reconstructed - filtered_signal
    var_error = np.var(error)
    var_signal = np.var(filtered_signal)
    variances.append(var_error)
    snr = var_signal / var_error if var_error > 0 else float('inf')
    snr_values.append(snr)

# =====================================================
# ПОБУДОВА ГРАФІКІВ
# =====================================================

font_size = 14
line_width = 1
fig_size = (21 / 2.54, 14 / 2.54)

# 1. Графіки дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=fig_size)
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(t, discrete_signals[s], linewidth=line_width)
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=font_size)
        ax[i, j].grid(True)
        s += 1
fig.supxlabel('Час (с)', fontsize=font_size)
fig.supylabel('Амплітуда', fontsize=font_size)
fig.suptitle('Дискретизовані сигнали', fontsize=font_size)
plt.tight_layout()
plt.savefig('figures/discrete_signals.png', dpi=600)
plt.show()

# 2. Графіки спектрів дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=fig_size)
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(freq, discrete_spectrums[s], linewidth=line_width)
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=font_size)
        ax[i, j].grid(True)
        s += 1
fig.supxlabel('Частота (Гц)', fontsize=font_size)
fig.supylabel('Амплітуда', fontsize=font_size)
fig.suptitle('Спектри дискретизованих сигналів', fontsize=font_size)
plt.tight_layout()
plt.savefig('figures/discrete_spectrums.png', dpi=600)
plt.show()

# 3. Графіки відновлених сигналів
fig, ax = plt.subplots(2, 2, figsize=fig_size)
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(t, reconstructed_signals[s], linewidth=line_width, label='Відновлений')
        ax[i, j].plot(t, filtered_signal, 'r--', linewidth=line_width, label='Оригінал')
        ax[i, j].set_title(f'Dt = {steps[s]}', fontsize=font_size)
        ax[i, j].grid(True)
        ax[i, j].legend()
        s += 1
fig.supxlabel('Час (с)', fontsize=font_size)
fig.supylabel('Амплітуда', fontsize=font_size)
fig.suptitle('Відновлені сигнали', fontsize=font_size)
plt.tight_layout()
plt.savefig('figures/reconstructed_signals.png', dpi=600)
plt.show()

# 4. Графік дисперсії від кроку дискретизації
plt.figure(figsize=fig_size)
plt.plot(steps, variances, 'bo-', linewidth=line_width)
plt.xlabel('Крок дискретизації Dt', fontsize=font_size)
plt.ylabel('Дисперсія помилки', fontsize=font_size)
plt.title('Залежність дисперсії від кроку дискретизації', fontsize=font_size)
plt.grid(True)
plt.savefig('figures/variance_vs_dt.png', dpi=600)
plt.show()

# 5. Графік SNR від кроку дискретизації
plt.figure(figsize=fig_size)
plt.plot(steps, snr_values, 'gs-', linewidth=line_width)
plt.xlabel('Крок дискретизації Dt', fontsize=font_size)
plt.ylabel('Відношення сигнал/шум', fontsize=font_size)
plt.title('Залежність SNR від кроку дискретизації', fontsize=font_size)
plt.grid(True)
plt.savefig('figures/snr_vs_dt.png', dpi=600)
plt.show()