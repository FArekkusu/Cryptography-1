from collections import Counter

ENGLISH_FREQUENCIES = {
    "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.01270,
    "f": 0.02228, "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153,
    "k": 0.00772, "l": 0.04025, "m": 0.02406, "n": 0.06749, "o": 0.07507,
    "p": 0.01929, "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056,
    "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150, "y": 0.01974,
    "z": 0.00074
}

def crack_single_byte_xor(encrypted_bytes):
    min_n, min_s = float("inf"), None

    for i in range(256):
        candidate_bytes = [x ^ i for x in encrypted_bytes]

        if all(x >= ord(" ") for x in candidate_bytes):
            candidate = "".join(map(chr, candidate_bytes))
            symbol_counts = Counter(filter(str.isalpha, candidate.lower()))

            total_letters = sum(symbol_counts.values())
            for x in symbol_counts:
                symbol_counts[x] /= total_letters
            
            n = fitting_quotient(symbol_counts, ENGLISH_FREQUENCIES)
            if n < min_n:
                min_n, min_s = n, candidate
    return min_s

def sum_squares(actual, expected):
    return sum((expected[x] - actual[x])**2 for x in expected)

def fitting_quotient(actual, expected):
    return sum(abs(actual[x] - expected[x]) for x in expected) / len(expected)

def chi_squared(actual, expected):
    return sum((actual[x] - expected[x])**2 / expected[x] for x in expected)