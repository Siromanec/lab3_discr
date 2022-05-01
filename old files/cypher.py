from pprint import pprint
import random
from modexp import modexp
import string
import time

class RSA_Message():
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.PRIMES = self.eratosthenes(10000)
        self.enumerate_chars()
        self.gen_keys()
        self.find_M_len()
        self.split_M()
        self.gen_M()
        self.encode_C()
        self.decode_C()
        self.M_into_msg()
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
        return prime_list[82:]

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
        for i in range(3, 100, 2):
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


    def find_M_len(self):
        """
        need to change to 182182182182 instead of 182182182 later
        """
        repeat = 0

        left = self.supported_chars_len
        right = left * 1000 + self.supported_chars_len
        repeat += 1
        while not left < self.n < right:
            left = right
            right = left * 1000 + self.supported_chars_len
            repeat += 1
        
        print(left, self.n, right, repeat)

        self.repeat = repeat


    def split_M(self):
        """
        :param str l: letter
        """
        fictive_key = (self.repeat * 3 - (len(self.msg) % self.repeat * 3))
        msg_with_tail = self.msg + chr(20) * fictive_key
        M_list = list(map("".join, zip(*[iter(msg_with_tail)] * (self.repeat))))
        self.M_list = M_list

    def gen_M(self):
        M_code_list = []
        for i in self.M_list:
            M_code = ''
            for j in i:
                M_code += self.chars_code_dict[j]
            M_code_list.append(M_code)
        self.M_code_list = M_code_list


    def encode_C(self):
        encoded_C_list = []
        for M in self.M_code_list:
            C = modexp(int(M), self.e, self.n)
            encoded_C_list.append(C)
        print(self.M_code_list)
        print(encoded_C_list)
        print(self.M_list)

        self.encoded_C_list = encoded_C_list
        pass
    def decode_C(self):
        decoded_M_list = []

        for C in self.encoded_C_list:
            M = str(modexp(C, self.d, self.n))
            len_M = len(M)
            if len_M % 3 == 0:
                decoded_M_list.append(M)
            else:
                decoded_M_list.append(M.rjust(len_M + 3 - (len_M % 3), "0"))
        print(decoded_M_list)
        self.decoded_M_list = decoded_M_list
    def M_into_msg(self):
        msg = ''
        for i in self.decoded_M_list:
            #print(str(*[iter(i)] * 3))
            msg_list = list(map("".join, zip(*[iter(i)] * 3)))
            for j in msg_list:
                msg += self.chars_code_dict_inverse[j]
                pass
            #msg = list(map(self.chars_code_dict["".join, zip(*[iter(i)] * 3)]))
        print(msg)
        self.msg = msg
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
        print(self.d)
        return self.d

    def enumerate_chars(self):
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
        self.supported_chars_len = len(chars)

        chars_code = zip([i for i in chars], 
                         [str(j).rjust(3, "0") for j in range(self.supported_chars_len)])

        self.chars_code_dict = dict(chars_code)
        self.chars_code_dict[chr(20)] = str(self.supported_chars_len)
        self.chars_code_dict_inverse = dict(zip(self.chars_code_dict.values(), self.chars_code_dict.keys()))

msg = RSA_Message("message")
#print(msg.eratosthenes(1000))
[2, 3, 5, 7, 11, 13, 17, 19]
#print(msg.rand_prime())
msg.gen_relative_primes(3222)
msg.gen_keys()


#if __name__ == '__main__':
#    import doctest
#    doctest.testmod()