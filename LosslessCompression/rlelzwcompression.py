import os
import math
import collections
import matplotlib.pyplot as plt


# =====================================================
# ФУНКЦІЇ RLE
# =====================================================

def encode_rle(sequence):
    if not sequence:
        return "", []

    result = []
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1
    result.append((sequence[-1], count))

    encoded_str = ''.join([f"{item[1]}{item[0]}" for item in result])
    return encoded_str, result


def decode_rle(encoded_data):
    result = []
    i = 0
    while i < len(encoded_data):
        num_str = ""
        while i < len(encoded_data) and encoded_data[i].isdigit():
            num_str += encoded_data[i]
            i += 1
        if i < len(encoded_data) and num_str:
            count = int(num_str)
            char = encoded_data[i]
            result.append(char * count)
            i += 1
    return ''.join(result)


# =====================================================
# ФУНКЦІЇ LZW
# =====================================================

def encode_lzw(sequence):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    current = ""
    total_bits = 0

    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            code = dictionary[current]
            result.append(code)
            bits = 8 if code < 256 else math.ceil(math.log2(len(dictionary)))
            total_bits += bits
            dictionary[new_str] = len(dictionary)
            current = c

    if current:
        code = dictionary[current]
        result.append(code)
        bits = 8 if code < 256 else math.ceil(math.log2(len(dictionary)))
        total_bits += bits

    return result, total_bits


def decode_lzw(encoded_sequence):
    dictionary = {i: chr(i) for i in range(256)}
    result = []
    if not encoded_sequence:
        return ""

    previous = chr(encoded_sequence[0])
    result.append(previous)

    for code in encoded_sequence[1:]:
        if code in dictionary:
            current = dictionary[code]
        elif code == len(dictionary):
            current = previous + previous[0]
        else:
            raise ValueError("Invalid code")

        result.append(current)
        dictionary[len(dictionary)] = previous + current[0]
        previous = current

    return ''.join(result)


# =====================================================
# ЗЧИТУВАННЯ ПОСЛІДОВНОСТЕЙ
# =====================================================

def read_sequences():
    file_path = os.path.join(os.path.dirname(__file__), 'sequence.txt')
    if not os.path.exists(file_path):
        file_path = 'sequence.txt'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sequences = []
    lines = content.strip().split('\n')
    for line in lines:
        if 'Послідовність' in line and ':' in line:
            seq = line.split(':', 1)[1].strip()
            if seq:
                sequences.append(seq)

    return sequences[:8]


# =====================================================
# ОБЧИСЛЕННЯ ЕНТРОПІЇ
# =====================================================

def calculate_entropy(sequence):
    counts = collections.Counter(sequence)
    N = len(sequence)
    probability = {symbol: count / N for symbol, count in counts.items()}
    entropy = -sum(p * math.log2(p) for p in probability.values() if p > 0)
    return round(entropy, 4)


# =====================================================
# ОСНОВНА ПРОГРАМА
# =====================================================

def main():
    os.makedirs('LosslessCompression', exist_ok=True)

    sequences = read_sequences()
    if not sequences:
        print("Помилка: Не знайдено послідовностей у файлі sequence.txt")
        return

    results = []

    with open('LosslessCompression/results_rle_lzw.txt', 'w', encoding='utf-8') as f:
        for idx, seq in enumerate(sequences, 1):
            original_bits = len(seq) * 8
            entropy = calculate_entropy(seq)

            f.write(f"\n{'=' * 60}\n")
            f.write(f"Послідовність {idx}: {seq[:80]}...\n")
            f.write(f"Розмір оригінальної послідовності: {original_bits} bits\n")
            f.write(f"Ентропія: {entropy}\n")

            # RLE
            encoded_rle, rle_data = encode_rle(seq)
            decoded_rle = decode_rle(encoded_rle)
            rle_bits = len(encoded_rle) * 8
            cr_rle = round(original_bits / rle_bits, 2) if rle_bits > 0 and original_bits > 0 else 0
            cr_rle_display = cr_rle if cr_rle >= 1 else '-'

            f.write(f"\nКодування RLE:\n")
            f.write(f"  Закодована RLE послідовність: {encoded_rle[:100]}...\n")
            f.write(f"  Розмір: {rle_bits} bits\n")
            f.write(f"  Коефіцієнт стиснення RLE: {cr_rle_display}\n")
            f.write(f"  Декодування правильне: {decoded_rle == seq}\n")

            # LZW
            encoded_lzw, lzw_bits = encode_lzw(seq)
            decoded_lzw = decode_lzw(encoded_lzw)
            cr_lzw = round(original_bits / lzw_bits, 2) if lzw_bits > 0 else 0
            cr_lzw_display = cr_lzw if cr_lzw >= 1 else '-'

            f.write(f"\nКодування LZW:\n")
            f.write(f"  Закодована LZW послідовність: {encoded_lzw[:50]}...\n")
            f.write(f"  Розмір: {lzw_bits} bits\n")
            f.write(f"  Коефіцієнт стиснення LZW: {cr_lzw_display}\n")
            f.write(f"  Декодування правильне: {decoded_lzw == seq}\n")

            results.append([entropy, cr_rle_display, cr_lzw_display])

    # Таблиця результатів
    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    ax.axis('off')

    headers = ['Ентропія', 'КС RLE', 'КС LZW']
    row_labels = [f'Послідовність {i + 1}' for i in range(len(results))]

    table = ax.table(cellText=results, colLabels=headers, rowLabels=row_labels,
                     loc='center', cellLoc='center')
    table.set_fontsize(12)
    table.scale(0.8, 1.5)
    plt.title('Результати стиснення методами RLE та LZW', fontsize=14)
    plt.savefig('LosslessCompression/compression_results_table.png', dpi=600)
    plt.show()

    print("\n" + "=" * 50)
    print("ГОТОВО! Результати збережено в папку LosslessCompression/")
    print("Файли: results_rle_lzw.txt, compression_results_table.png")
    print("=" * 50)


if __name__ == "__main__":
    main()