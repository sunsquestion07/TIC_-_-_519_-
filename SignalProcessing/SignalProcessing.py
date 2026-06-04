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
# =====================================================
# ПРАКТИЧНА РОБОТА №4 - КВАНТУВАННЯ
# =====================================================

levels = [4, 16, 64, 256]

quantized_signals = []
variances_q = []
snr_values_q = []

for M in levels:
    # Крок квантування
    delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)

    # Квантування сигналу
    quantized_signal = delta * np.round(filtered_signal / delta)
    quantized_signals.append(quantized_signal)

    # Рівні квантування
    quantize_levels = np.arange(np.min(quantized_signal), np.max(quantized_signal) + delta, delta)

    # Бітове представлення
    n_bits = int(np.log2(M))
    quantize_bit = [format(bits, '0' + str(n_bits) + 'b') for bits in range(M)]

    # Таблиця квантування
    quantize_table = np.column_stack((quantize_levels[:M], quantize_bit[:M]))

    # Побудова таблиці
    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table,
                     colLabels=['Значення сигналу', 'Кодова послідовність'],
                     loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    plt.savefig(f'figures/quantization_table_M{M}.png', dpi=600)
    plt.close()

    # Перетворення сигналу в бітову послідовність
    bits = []
    for signal_value in quantized_signal:
        for idx, level_value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - level_value), 0) == 0:
                bits.append(quantize_bit[idx])
                break

    # Об'єднання бітів в один рядок
    bits_string = ''.join(bits)
    bits_list = [int(bit) for bit in bits_string]

    # Побудова графіку бітової послідовності
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    x_bits = np.arange(len(bits_list))
    ax.step(x_bits, bits_list, linewidth=0.5)
    ax.set_xlabel('Номер біта', fontsize=14)
    ax.set_ylabel('Значення біта', fontsize=14)
    ax.set_title(f'Кодова послідовність для M={M}', fontsize=14)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True)
    plt.savefig(f'figures/bit_sequence_M{M}.png', dpi=600)
    plt.close()

    # Розрахунок дисперсії та SNR
    error = quantized_signal - filtered_signal
    var_error = np.var(error)
    var_signal = np.var(filtered_signal)
    variances_q.append(var_error)
    snr = var_signal / var_error if var_error > 0 else float('inf')
    snr_values_q.append(snr)

# Графіки цифрових сигналів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(t, quantized_signals[s], linewidth=1)
        ax[i, j].set_title(f'M = {levels[s]}', fontsize=14)
        ax[i, j].grid(True)
        s += 1
fig.supxlabel('Час (с)', fontsize=14)
fig.supylabel('Амплітуда', fontsize=14)
fig.suptitle('Цифрові сигнали (квантовані)', fontsize=14)
plt.tight_layout()
plt.savefig('figures/quantized_signals.png', dpi=600)
plt.show()

# Графік дисперсії від кількості рівнів квантування
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(levels, variances_q, 'ro-', linewidth=1)
plt.xlabel('Кількість рівнів квантування M', fontsize=14)
plt.ylabel('Дисперсія помилки квантування', fontsize=14)
plt.title('Залежність дисперсії від M', fontsize=14)
plt.grid(True)
plt.savefig('figures/variance_vs_M.png', dpi=600)
plt.show()

# Графік SNR від кількості рівнів квантування
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(levels, snr_values_q, 'bs-', linewidth=1)
plt.xlabel('Кількість рівнів квантування M', fontsize=14)
plt.ylabel('Відношення сигнал/шум (SNR)', fontsize=14)
plt.title('Залежність SNR від M', fontsize=14)
plt.grid(True)
plt.savefig('figures/snr_vs_M.png', dpi=600)
plt.show()

print("=" * 50)
print("РЕЗУЛЬТАТИ КВАНТУВАННЯ")
print("=" * 50)
print(f"{'M':<8} {'Дисперсія':<15} {'SNR':<15}")
print("-" * 40)
for i, M in enumerate(levels):
    print(f"{M:<8} {variances_q[i]:<15.6f} {snr_values_q[i]:<15.2f}")