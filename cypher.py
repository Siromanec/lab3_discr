from pprint import pprint
import random
from modexp import modexp
import string
import time

class RSA_Message():
    def __init__(self, msg: str) -> None:
        self.PRIMES = self.eratosthenes(1000)
        self.enumerate_chars()
        self.gen_keys()
        self.msg = msg
        self.encoded_msg = self.encode(msg)
        pass
    def encode(self, msg):
        pass
    def eratosthenes(self, n):
        """
        generates prime numbers starting from 53
        because other values are too small
        thus the cut
        >>> msg = RSA_Message("hi")
        >>> msg.eratosthenes(100)
        [53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        """
        prime_list = []
        numbers = {}
        for i in range(2, n + 1):
            numbers[i] = True
        curr = 2
        while curr != n + 1:
            if numbers[curr] == True:
                if curr + curr < n + 1:
                    prime_list.append(curr)
                    for i in range(curr+curr, n + 1, curr):
                        numbers[i] = False
                else:
                    prime_list.append(curr)    
            curr += 1
        return prime_list[15:]

        pass
    def euclid(self, a, b):
        """
        greatest common divider
        """
        while a!= 0 and b!=0:
            if a > b:
                a = a % b
            else:
                b = b % a
        return a + b
    def rand_prime(self):
        return random.choices(self.PRIMES, k=2) #change if random cant be used


    def gen_relative_primes(self, product):
        """
        generates a list of small relatiive primes
        """
        relative_primes = []
        for i in range(3, 50, 2):
            gcd = self.euclid(product, i)
            if gcd == 1:
                relative_primes.append(i)
        return relative_primes

    def gen_mod_inverse(self, e, product):
        """
        calculates inverse
        better use pow()
        """
        curr = 0
        mod_to_one = 1 % product
        while (e * curr) % product != mod_to_one:
            curr += 1
        return curr
    def gen_M(self, l):
        """
        :param str l: letter
        """
        ord_num = self.chars_code_dict[l]
        pass
    def gen_keys(self):
        """
        key generator
        """
        # step 1
        p, q = self.rand_prime()
        # step 2
        self.n = p * q
        # step 3
        product = (p - 1) * (q - 1)
        relative_primes = self.gen_relative_primes(product)
        self.e = random.choice(relative_primes)
        # step 4
        e_inverse = pow(self.e, -1, product)
        self.d = (e_inverse % product)
        
        return self.d

    def enumerate_chars(self):
        """
        enumerates the symbols
        supports latin, german, cyrillic
        three symbols per each character
        """

        cyrillic = "абвгґдееєжзиіїйклмнопрстуфхцчшщьюяэъыё"
        special_chars = "0123456789-=`~!@#$%^&*()_+,./;\'\\[]<>?:\"|{} \t№§\n"

        chars = special_chars + string.ascii_letters + "üäößÜÄÖ" + cyrillic + cyrillic.upper()

        chars_code = zip([i for i in chars], [str(j).rjust(3, "0") for j in range(182)])

        self.chars_code_dict = dict(chars_code)

msg = RSA_Message("hi")
#print(msg.eratosthenes(1000))
[2, 3, 5, 7, 11, 13, 17, 19]
print(msg.rand_prime())
msg.gen_relative_primes(3222)
msg.gen_keys()
msg.gen_M("a")


if __name__ == '__main__':
    import doctest
    doctest.testmod()