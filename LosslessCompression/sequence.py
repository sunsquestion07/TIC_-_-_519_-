import random
import collections
import math
import string
import os

# Ваші дані
last_name = "RIABOVOL"  # Ваше прізвище
group_number = "519"  # Номер групи

N_sequence = 100
os.makedirs('LosslessCompression', exist_ok=True)

# =====================================================
# ГЕНЕРАЦІЯ ПОСЛІДОВНОСТЕЙ
# =====================================================

# Послідовність 1: випадкові 0 та 1
seq1 = ''.join(random.choice(['0', '1']) for _ in range(N_sequence))

# Послідовність 2: прізвище + нулі
seq2 = last_name + '0' * (N_sequence - len(last_name))

# Послідовність 3: прізвище + нулі, перемішані
seq3_list = list(last_name + '0' * (N_sequence - len(last_name)))
random.shuffle(seq3_list)
seq3 = ''.join(seq3_list)

# Послідовність 4: чергування прізвища та номера групи
letters = list(last_name) + list(group_number)
n_letters = len(letters)
n_repeats = N_sequence // n_letters
remainder = N_sequence % n_letters
seq4_list = letters * n_repeats + letters[:remainder]
seq4 = ''.join(seq4_list)

# Послідовність 5: перші 2 букви прізвища + цифри групи, ймовірність 0.2
alphabet5 = list(last_name[:2]) + list(group_number)
seq5_list = [random.choice(alphabet5) for _ in range(N_sequence)]
random.shuffle(seq5_list)
seq5 = ''.join(seq5_list)

# Послідовність 6: букви (70%) та цифри (30%)
letters6 = list(last_name[:2])
digits6 = list(group_number)
n_letters6 = int(0.7 * N_sequence)
n_digits6 = N_sequence - n_letters6
seq6_list = [random.choice(letters6) for _ in range(n_letters6)] + [random.choice(digits6) for _ in range(n_digits6)]
random.shuffle(seq6_list)
seq6 = ''.join(seq6_list)

# Послідовність 7: англійські літери та цифри
alphabet7 = string.ascii_lowercase + string.digits
seq7 = ''.join(random.choice(alphabet7) for _ in range(N_sequence))

# Послідовність 8: всі одиниці
seq8 = '1' * N_sequence

sequences = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
names = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4',
         'Послідовність 5', 'Послідовність 6', 'Послідовність 7', 'Послідовність 8']

# Збереження послідовностей у файл
with open('LosslessCompression/sequence.txt', 'w', encoding='utf-8') as f:
    for i, seq in enumerate(sequences, 1):
        f.write(f"Послідовність {i}: {seq}\n")
        f.write(f"Розмір: {len(seq)} байт\n\n")


# =====================================================
# РОЗРАХУНОК ХАРАКТЕРИСТИК
# =====================================================

def calculate_characteristics(sequence, name):
    N = len(sequence)
    counts = collections.Counter(sequence)
    alphabet_size = len(counts)

    probability = {symbol: count / N for symbol, count in counts.items()}
    mean_probability = sum(probability.values()) / alphabet_size if alphabet_size > 0 else 0

    # Перевірка рівномірності
    if alphabet_size > 1:
        equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
        uniformity = "рівна" if equal else "нерівна"
    else:
        uniformity = "рівна"

    # Ентропія
    entropy = -sum(p * math.log2(p) for p in probability.values()) if alphabet_size > 0 else 0

    # Надмірність
    if alphabet_size > 1:
        source_excess = 1 - entropy / math.log2(alphabet_size)
    else:
        source_excess = 1

    return {
        'name': name,
        'sequence': sequence,
        'size': N,
        'alphabet_size': alphabet_size,
        'probability': probability,
        'mean_probability': mean_probability,
        'uniformity': uniformity,
        'entropy': entropy,
        'source_excess': source_excess
    }


results = []
for seq, name in zip(sequences, names):
    results.append(calculate_characteristics(seq, name))

# =====================================================
# ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТІВ У ФАЙЛ
# =====================================================

with open('LosslessCompression/results_sequence.txt', 'w', encoding='utf-8') as f:
    for res in results:
        f.write(f"{res['name']}: {res['sequence']}\n")
        f.write(f"Розмір послідовності: {res['size']} байт\n")
        f.write(f"Розмір алфавіту: {res['alphabet_size']}\n")
        prob_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in res['probability'].items()])
        f.write(f"Ймовірності появи символів: {prob_str}\n")
        f.write(f"Середнє арифметичне ймовірностей: {res['mean_probability']:.4f}\n")
        f.write(f"Ймовірність розподілу символів: {res['uniformity']}\n")
        f.write(f"Ентропія: {res['entropy']:.4f}\n")
        f.write(f"Надмірність джерела: {res['source_excess']:.4f}\n")
        f.write("-" * 50 + "\n\n")

# =====================================================
# ПОБУДОВА ТАБЛИЦІ
# =====================================================

import matplotlib.pyplot as plt

headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
row_labels = [f'Послідовність {i + 1}' for i in range(len(results))]
table_data = [[res['alphabet_size'], round(res['entropy'], 2), round(res['source_excess'], 2), res['uniformity']] for
              res in results]

fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
ax.axis('off')
table = ax.table(cellText=table_data, colLabels=headers, rowLabels=row_labels, loc='center', cellLoc='center')
table.set_fontsize(12)
table.scale(0.8, 1.5)
plt.title('Характеристики сформованих послідовностей', fontsize=14)
plt.savefig('LosslessCompression/characteristics_table.png', dpi=600)
plt.show()

print("Генерацію завершено! Файли збережено в папку LosslessCompression/")