from cypher import RSA_Message
def test():
    rsa_msg = RSA_Message("hello")
    assert rsa_msg.euclid(30, 30) == 30
    assert rsa_msg.euclid(17, 30) == 1
test()
