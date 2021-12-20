from dataclasses import dataclass
from io import open

@dataclass
class Transaction:
    __raw: bytes

    @staticmethod
    def new(from_pub: bytes, to_pub: bytes, amt: int):
        return Transaction(from_pub + to_pub + amt.to_bytes(2, 'big'))

    @property
    def raw(self):
        return self.__raw

    @property
    def from_pub(self):
        return self.__raw[0:2]

    @property
    def to_pub(self):
        return self.__raw[2:4]

    @property
    def amt(self):
        return int.from_bytes(self.__raw[4:6], 'big')

    def __repr__(self):
        res =  f"from: 0x{self.from_pub.hex()}\n"
        res += f"to: 0x{self.to_pub.hex()}\n"
        res += f"amt: {self.amt}"
        return res

def test_tx():

    from_pub = bytes([1,2])
    to_pub = bytes([2,3])
    amt = 5

    tx = Transaction.new(from_pub, to_pub, amt)

    assert tx.from_pub == from_pub
    assert tx.to_pub == to_pub
    assert tx.amt == amt
    print(tx)
    print("ok!")

if __name__ == "__main__":
    test_tx()
