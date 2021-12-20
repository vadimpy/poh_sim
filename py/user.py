import elgamal
import tx
import tx_handler
from io import open

class User:
    uid = 0

    def __init__(self, tx_handler: tx_handler.TxHandler, p: int, g: int):
        self.__signer = elgamal.ElGamalSigner(p, g)
        self.__signer.set_secret()
        self.__tx_handler = tx_handler
        self.__log_f = open(f'logs/user{User.uid}.log', 'w+')
        self.log(f"Pub: {self.pub.hex()}")
        User.uid += 1

    @property
    def pub(self):
        return self.__signer.pub.to_bytes(2, 'big')

    def log(self, line):
        self.__log_f.write(line)
        self.__log_f.write('\n')

    def get_recent_hash(self):
        return self.__tx_handler.poh.recent_hash

    def send_with_timehash(self, to_pub: bytes, amt: int, time_hash: bytes):
        
        self.log('\n')
        self.log('#' * 80)
        self.log('\n')

        self.log(f"to: 0x{to_pub.hex()}")
        self.log(f"amt: {amt}")
        self.log(f"time hash: {time_hash.hex()}")

        txn = tx.Transaction.new(self.pub, to_pub, amt)
        txn = time_hash + txn.raw
        off, sig = self.__signer.sign(txn)
        assert self.__signer.verify(txn, (off, sig))
        self.__tx_handler.push_tx(sig + txn)

    def finish(self):
        self.__log_f.close()