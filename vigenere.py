
from collections import Counter
from itertools import zip_longest
from single_byte_xor import crack_single_byte_xor

ENGLISH_IC = 1.73

def crack_vigenere(encrypted_bytes):
    possible_key_lens = get_possible_lens(encrypted_bytes)
    options = set()
    for step in possible_key_lens:
        columns = [crack_single_byte_xor(encrypted_bytes[start::step]) for start in range(step)]
        candidate = "".join("".join(x) for x in zip_longest(*columns, fillvalue=""))

        if candidate in options:
            return candidate
        if is_possible_decryption(candidate):
            options.add(candidate)
        
    if len(options) == 1:
        return options.pop()

def get_possible_lens(encrypted_bytes):
    r = []
    for step in range(1, len(encrypted_bytes) // 2 + 1):
        ic = sum(index_of_coincidence(encrypted_bytes[start::step]) for start in range(step)) / step
        if ENGLISH_IC * (1 / 2) < ic < ENGLISH_IC * (3 / 2):
            r.append(step)
    return r

def index_of_coincidence(bytes_):
    N = len(bytes_)
    return sum(n * (n - 1) for n in Counter(bytes_).values()) * 26 / N / (N - 1)

def is_possible_decryption(s):
    return sum(32 <= x < 127 for x in map(ord, s)) >= len(s) * 0.95
