import random
from modexp import modexp
import string


def encode(msg, n, e):
    char_dict, char_inversed_dict, max_char_value = enumerate_chars()
    chars_in_block, char_len = find_blocks_len(n, max_char_value)

    blocks = letters_to_codes(split_raw_on_blocks(msg, chars_in_block), char_dict, n)
    encoded_blocks = encode_blocks(blocks, e, n)

    return "".join(encoded_blocks)


def decode(msg, n, d):
    char_dict, char_inversed_dict, max_char_value = enumerate_chars()
    chars_in_block, char_len = find_blocks_len(n, max_char_value)

    decoded_blocks = decode_blocks(split_encoded_on_blocks(msg, n), d, n, char_len, chars_in_block)

    return codes_to_letters(decoded_blocks, char_len, char_inversed_dict)


def decode_blocks(encoded_blocks_list, d_key, n_key, char_length, chars_in_block):
    decoded_blocks_list = []
    for block in encoded_blocks_list:
        decoded_blocks_list.append(str(modexp(int(block), d_key, n_key)).zfill(char_length * chars_in_block))
    return decoded_blocks_list


def encode_blocks(blocks_list, e_key, n_key):
    encoded_blocks_list = []
    for block in blocks_list:
        encoded_blocks_list.append(str(modexp(int(block), e_key, n_key)).zfill(len(str(n_key))))
    return encoded_blocks_list


def codes_to_letters(decoded_blocks_list, letter_len, chars_code_dict_inverse):
    msg = ''
    for i in decoded_blocks_list:
        msg_list = list(map("".join, zip(*[iter(i)] * letter_len)))
        for j in msg_list:
            msg += chars_code_dict_inverse[j]
    return msg.rstrip(chr(20))


def letters_to_codes(blocks_list, chars_code_dict, n_key):
    return ["".join([chars_code_dict[char] for char in letter_block]).zfill(len(str(n_key))) for letter_block in blocks_list]


def split_raw_on_blocks(msg, block_len):
    """
    splits message into blocks
    """
    fictive_key = -(len(msg) % block_len) % block_len
    msg_with_tail = msg + chr(20) * fictive_key
    return list(map("".join, zip(*[iter(msg_with_tail)] * block_len)))


def split_encoded_on_blocks(msg, n):
    return [msg[i:i+len(str(n))] for i in range(0, len(msg), len(str(n)))]


def find_blocks_len(n, supported_chars_num):
    """
    need to change to 182182182182 instead of 182182182 later
    """
    shift = len(str(supported_chars_num))
    block_max_value = 0
    while not block_max_value * 10 ** shift + supported_chars_num >= n:
        block_max_value = block_max_value * 10 ** shift + supported_chars_num
    return len(str(block_max_value)) // shift, shift


def enumerate_chars():
    """
    enumerates the symbols
    supports latin, german, cyrillic
    three symbols per each character
    182
    """
    cyrillic = "абвгґдееєжзиіїйклмнопрстуфхцчшщьюяэъыё"
    special_chars = "0123456789-=`~!@#$%^&*()_+,./;\'\\[]<>?:\"|{} \t№§\n"

    chars = (special_chars +
             string.ascii_letters +
             "üäößÜÄÖ" +
             cyrillic +
             cyrillic.upper())
    supported_chars_len = len(chars)

    chars_code = zip([i for i in chars],
                     [str(j).rjust(3, "0") for j in range(supported_chars_len)])

    chars_code_dict = dict(chars_code)
    chars_code_dict[chr(20)] = str(supported_chars_len)
    chars_code_dict_inverse = dict(zip(chars_code_dict.values(), chars_code_dict.keys()))

    return chars_code_dict, chars_code_dict_inverse, supported_chars_len


def euclid(a, b):
    """
    greatest common divider
    """
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def gen_relative_primes(product):
    """
    generates a list of small relative primes
    """
    relative_primes = []
    for i in range(3, 100, 2):
        gcd = euclid(product, i)
        if gcd == 1:
            relative_primes.append(i)
    return relative_primes


def eratosthenes(n):
    """
    generates prime numbers starting from 53
    because other values are too small
    thus the cut
    >>> eratosthenes(100)
    [53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    """
    prime_list = []
    numbers = {}
    for i in range(2, n + 1):
        numbers[i] = True
    curr = 2
    while curr != n + 1:
        if numbers[curr] is True:
            if curr + curr < n + 1:
                for i in range(curr + curr, n + 1, curr):
                    numbers[i] = False
            prime_list.append(curr)
        curr += 1
    return prime_list[82:]


def rand_prime(n_range=10000):
    # n_range not bigger than 13000
    primes = eratosthenes(n_range)
    return random.choices(primes, k=2)  # change if random cant be used


def gen_keys():
    """
    key generator
    """
    # step 1
    p, q = rand_prime()
    # step 2
    n = p * q
    # step 3
    product = (p - 1) * (q - 1)
    relative_primes = gen_relative_primes(product)
    e = random.choice(relative_primes)
    # step 4
    d = pow(e, -1, product)
    # print("secret key: {}".format(d))
    return n, e, d


if __name__ == "__main__":
    msg = "Deadline"
    for i in range(1, 10000):
        n, e, d = gen_keys()
        try:
            encoded = encode(msg, n, e)
            decoded = decode(encoded, n, d)
            if decoded != msg:
                print(decoded)
        except KeyError:
            print(n)

