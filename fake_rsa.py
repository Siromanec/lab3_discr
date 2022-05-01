def generate_keys():
    return "n_key", "e_key", "d_key"


def encode(msg, n, e):
    if n == "n_key" and e == "e_key":
        return "encoded message"


def decode(msg, d):
    if d == "d_key":
        return "decoded message"