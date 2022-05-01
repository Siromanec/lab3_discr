import random
from modexp import modexp
import string

def enumerate_chars():
    """
    :return dict CHAR_DICT: dict of enumerated characters
    e. g. {'1':'001', '2':'002'}
    :return dict CHAR_INVERSED_DICT: inverse of CHAR_DICT
    :return int MAX_CHAR_VALUE: amount of characters
    enumerates the symbols
    supports latin, german, cyrillic
    three symbols per each character
    amount of symbols: 182
    fictive symbol: \x14 (chr(20))

    """

    cyrillic = "абвгґдееєжзиіїйклмнопрстуфхцчшщьюяэъыё"
    special_chars = "0123456789-=`~!@#$%^&*()_+,./;\'\\[]<>?:\"|{} \t№§\n"

    chars = (special_chars +
             string.ascii_letters +
             "üäößÜÄÖ" +
             cyrillic +
             cyrillic.upper())

    MAX_CHAR_VALUE = len(chars)

    chars_code = zip([i for i in chars],
                     [str(j).rjust(3, "0") for j in range(MAX_CHAR_VALUE)])

    CHAR_DICT = dict(chars_code)
    CHAR_DICT[chr(20)] = str(MAX_CHAR_VALUE)
    CHAR_INVERSED_DICT = dict(zip(CHAR_DICT.values(), CHAR_DICT.keys()))

    return CHAR_DICT, CHAR_INVERSED_DICT, MAX_CHAR_VALUE


def eratosthenes(n):
    """
    generates prime numbers starting from 431
    because other values are too small
    thus the cut
    >>> eratosthenes(460)
    [431, 433, 439, 443, 449, 457]
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


PRIMES = eratosthenes(100000)

CHAR_DICT, CHAR_INVERSED_DICT, MAX_CHAR_VALUE = enumerate_chars()


def encode(msg, n, e):
    """
    this function encodes the messaga uising RSA
    """

    chars_in_block, char_len = find_blocks_len(n)

    blocks = letters_to_codes(split_raw_on_blocks(msg, chars_in_block), n)
    encoded_blocks = encode_blocks(blocks, e, n)

    return "".join(encoded_blocks)


def decode(msg, n, d):
    """
    this function decodes the messaga uising RSA
    """

    chars_in_block, char_len = find_blocks_len(n)

    decoded_blocks = decode_blocks(split_encoded_on_blocks(msg, n), d, n, char_len, chars_in_block)

    return codes_to_letters(decoded_blocks, char_len)


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


def codes_to_letters(decoded_blocks_list, letter_len):

    msg = ''

    for i in decoded_blocks_list:

        msg_list = list(map("".join, zip(*[iter(i)] * letter_len)))

        for j in msg_list:

            msg += CHAR_INVERSED_DICT[j]

    return msg.rstrip(chr(20))


def letters_to_codes(blocks_list, n_key):

    return ["".join([CHAR_DICT[char] for char in letter_block]).
              zfill(len(str(n_key))) for letter_block in blocks_list]


def split_raw_on_blocks(msg, block_len):
    """
    splits message into blocks
    """

    fictive_key = -(len(msg) % block_len) % block_len
    msg_with_tail = msg + chr(20) * fictive_key

    return list(map("".join, zip(*[iter(msg_with_tail)] * block_len)))


def split_encoded_on_blocks(msg, n):

    return [msg[i:i+len(str(n))] for i in range(0, len(msg), len(str(n)))]


def find_blocks_len(n):
    """
    finds how long should letter groups be
    """

    shift = len(str(MAX_CHAR_VALUE))
    block_max_value = 0

    while not block_max_value * 10 ** shift + MAX_CHAR_VALUE >= n:

        block_max_value = block_max_value * 10 ** shift + MAX_CHAR_VALUE

    return len(str(block_max_value)) // shift, shift


def euclid(a, b):
    """
    greatest common divider
    >>> euclid(7, 21)
    7
    >>> euclid(16, 16)
    16
    >>> euclid(7, 18)
    1
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

    >>> gen_relative_primes(210)
    [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,\
 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    """

    relative_primes = []

    for i in range(3, 100, 2):

        gcd = euclid(product, i)

        if gcd == 1:

            relative_primes.append(i)

    return relative_primes


def rand_prime(n_range=100000):
    """
    selects random two primes from a list of primes
    """

    if n_range == 100000:

        primes = PRIMES

    else:

        primes = eratosthenes(n_range)

    return random.choices(primes, k=2)  # change if random cant be used


def gen_keys(n_range=100000):
    """
    key generator
    """

    while True:

        # step 1
        p, q = rand_prime(n_range)

        # step 2
        n = p * q

        # step 3
        product = (p - 1) * (q - 1)
        relative_primes = gen_relative_primes(product)
        e = random.choice(relative_primes)

        # step 4
        d = pow(e, -1, product)

        # print("secret key: {}".format(d))

        try:

            msg = "Test"
            encoded = encode(msg, n, e)
            decoded = decode(encoded, n, d)

            if decoded != msg:

                raise TypeError()

        except Exception:

            continue

        else:

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

            print(n, e, d)
