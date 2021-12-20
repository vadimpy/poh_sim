from random import randint
from dataclasses import dataclass

def euclid_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def extended_euclid_gcd(a, b): 
    if a == 0 :  
        return b, 0, 1

    gcd, x1, y1 = extended_euclid_gcd(b%a, a) 
    x = y1 - (b // a) * x1 
    y = x1

    return gcd,x,y 

def inverse(a, p):
    g, x, _ = extended_euclid_gcd(a, p)
    assert g == 1
    if x < 0:
        x = p + x
    return x

@dataclass
class ElGamalSigner:
    __p: int
    __g: int

    @property
    def g(self):
        return self.__g

    @property
    def secret(self):
        return self.__x

    @property
    def pub(self):
        return pow(self.__g, self.__x, self.__p) 

    @property
    def p(self):
        return self.__p

    def set_secret(self):
        self.__x = randint(0, self.__p - 2)
        return self.__x

    def sign(self, m: bytes):
        m_num = int.from_bytes(m, 'big')
        k = randint(0, self.__p-1)
        while euclid_gcd(k, self.p - 1) != 1:
            k = randint(0, self.__p-1)
        r = pow(self.__g, k, self.__p)
        s = (m_num - self.__x * r) * inverse(k, self.__p - 1) % (self.__p - 1)

        if s == 0:
            return self.sign(m)

        s_bits_len = len(bin(self.__p - 1)) - 2
        s_bytes_len = s_bits_len // 8 + (s_bits_len % 8 != 0)
        s_bytes = s.to_bytes(s_bytes_len, 'big')

        r_bits_len = len(bin(self.__p)) - 2
        r_bytes_len = r_bits_len // 8 + (r_bits_len % 8 != 0)
        r_bytes = r.to_bytes(r_bytes_len, 'big')

        return r_bytes_len, r_bytes + s_bytes

    def verify(self, m: bytes, sig: tuple[int, bytes], pub=None):
        if pub is None:
            pub = self.pub
        else:
            pub = int.from_bytes(pub, 'big')

        m_num = int.from_bytes(m, 'big')
        s_off, rs = sig
        r = int.from_bytes(rs[:s_off], 'big')
        s = int.from_bytes(rs[s_off:], 'big')

        if r >= self.__p or s >= self.__p - 1:
            return False

        return pow(self.__g, m_num, self.__p) == (pow(pub, r, self.__p) * pow(r, s, self.__p)) % self.__p

def test_rand():

    m_len = 5
    M = randint(0, 1000)

    p = 997
    g = 7

    eg_signer = ElGamalSigner(p, g)
    eg_signer.set_secret()

    m = M.to_bytes(m_len, 'big')
    sig = eg_signer.sign(m)
    print('s len', sig[0], 'rs_len', len(sig[1]))

    print('')

    print(eg_signer.verify(m, sig))


if __name__ == "__main__":
    test_rand()
