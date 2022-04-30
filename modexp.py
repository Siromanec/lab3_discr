from time import time
def exp(b: int, n: int, m: int):
    
    x = b ** n % m
    return x # f"{b} ** {n} mod {m} = {x}"

def modexp(b: int, n: int, m: int):
    """
    calculates modular exponents
    e.g. 12 ** 1743 mod 25 = 3
    """
    x = 1
    i = 0
    power = b % m
    n_bin = bin(n)
    n_bin = str(n_bin)
    n_bin = n_bin[2:]
    n_bin = n_bin[::-1]
    for a in n_bin:
        #print(f"i = {i}, a = {a},", end=" ")
        if a  == "1":
            #print(f"x = {power} * {x} mod {m}", end=" = ")
            x = power * x % m
            #print(x, end=", ")
        #else:
        #    print(f"x = {x}", end=", ")
        #print(f"power = {power} * {power} mod {m}", end=" = ")
        power = power * power % m
        #print(power)
        i += 1
    return x #f"{b} ** {n} mod {m} = {x}"
#start = time()
#result = modexp1(10000000, 10000000, 10000000)
#end = time() - start
#print(f"modexp1 finished in {end} s.")
#start = time()
#result = modexp(12, 1743, 25)
#end = time() - start
#print(result)
#print(f"modexp2 finished in {end} s.")

