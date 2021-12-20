from hashlib import sha256
from tx import Transaction
from io import open

class Chain:
    def __init__(self):
        h = sha256()
        tx_first = (0).to_bytes(5, 'big')
        h.update(tx_first)
        self.__chain = [(tx_first, h.digest())]

    def push(self, tx: bytes):
        h = sha256()
        last_hash = self.__chain[-1][1]
        h.update(last_hash + tx)
        self.__chain.append((tx, h.digest()))

    def verify(self):
        for i in range(1, len(self.__chain)):
            h = sha256()
            h.update(self.__chain[i-1][1] + self.__chain[i][0])
            if h.digest() != self.__chain[i][1]:
                return False
        return True

    def finish(self):
        logs = open("logs/chain.log", 'w+')
        for i, tx_raw_hash in enumerate(self.__chain):
            tx_raw, hash = tx_raw_hash
            txn = Transaction(tx_raw)
            logs.write(f"Tr {i}:\n{txn}\n")
            logs.write(f"hash: {hash.hex()}\n\n")
        logs.close()

def chain_test():
    c = Chain()
    for _ in range(5):
        txn = Transaction.new(b"ab", b"ab", 5)
        c.push(txn.raw)
    print(c.verify())

if __name__ == '__main__':
    chain_test()
