import asyncio
import poh_gen
import chain
import elgamal
import tx
from io import open

class TxHandler:

    def __init__(self, p: int, g: int, poh_initial: bytes, acc_len: int, poh_per: float, unwind_per: float):
        self.__verif = elgamal.ElGamalSigner(p, g)
        self.__chain = chain.Chain()
        self.__poh   = poh_gen.PoH_generator(poh_initial, acc_len, poh_per)
        self.__tx_queue = []
        self.__unwind_per = unwind_per
        self.__log_f = open('logs/tx_handler.log', 'w+')

    @property
    def poh(self):
        return self.__poh

    def push_tx(self, txn: bytes):
        self.__tx_queue.append(txn)

    def log(self, line):
        self.__log_f.write(line)
        self.__log_f.write('\n')

    async def handle_transactions(self):
        while True:
            await asyncio.sleep(self.__unwind_per)
            self.log('')
            self.log('#' * 80)
            self.log('\nHandle transactions:\n')
            block = list()
            if len(self.__tx_queue) > 0:
                for tx_signed in self.__tx_queue:
                    sig = tx_signed[:4]
                    tx_time_hash = tx_signed[4:36]
                    tx_raw = tx_signed[36:]
                    txn = tx.Transaction(tx_raw)
                    tx_is_verified = self.__verif.verify(m=tx_time_hash + tx_raw, sig=(2, sig), pub=txn.from_pub)

                    self.log(f"\ntx_signed: {tx_signed.hex()}")
                    self.log(f"time_hash: {tx_time_hash.hex()}")
                    self.log(f"from: {txn.from_pub.hex()}")
                    self.log(f"to: {txn.to_pub.hex()}")
                    self.log(f"amt: {txn.amt}")
                    self.log(f'verified: {tx_is_verified}')

                    if tx_is_verified:
                        block.append((tx_time_hash, tx_raw))

            block = self.__poh.get_sorted(block)
            for _, tx_raw in block:
                self.__chain.push(tx_raw)

            self.__tx_queue = []

    def finish(self):
        self.__chain.finish()
        self.__poh.finish()
        self.__log_f.close()
