from hashlib import sha256
import asyncio
from io import open

class PoH_generator:
    def __init__(self, initial: bytes, accept_len: int, tick_dur: int):
        self.__last = initial
        self.__acc_len = accept_len
        self.__tick_dur = tick_dur
        self.__win = []
        self.__log_f = open('logs/poh.log', 'w+')
        self.__counter = 0
        self.update()

    def log(self, line):
        self.__log_f.write(line)
        self.__log_f.write('\n')

    def update(self):
        self.__counter += 1
        m = sha256()
        m.update(self.__last)
        self.__last = m.digest()
        if len(self.__win) == self.__acc_len:
            self.__win.pop(0)
        self.log(f'{self.__counter}. {self.__last.hex()}')
        self.__win.append(self.__last)

    def finish(self):
        self.__log_f.close()

    @property
    def recent_hash(self):
        return self.__last

    async def run(self):
        while True:
            await asyncio.sleep(self.__tick_dur)
            self.update()

    def get_sorted(self, txns: list[tuple[bytes, bytes]]):
        res = list()
        for hash in self.__win:
            for tx_hash, tx in txns:
                if hash == tx_hash:
                    res.append((tx_hash, tx))
        return res


async def poh_test():
    poh = PoH_generator(b'privet', 10, 1)
    while True:
        await poh.tick_vdf()
        print(poh.recent_hash.hex(), len(poh.recent_hash))

if __name__ == '__main__':
    asyncio.run(poh_test())
