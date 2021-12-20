from dataclasses import astuple
import user
import tx_handler
import asyncio
from tqdm import tqdm

class UserExec:
    def __init__(self, u: user.User, scenario: list[tuple[int, float]]):
        self.u = u
        self.scenario = scenario

    async def run(self, to_pub: bytes):
        for dur_before_hash, dur_before_send, amt in self.scenario:
            await asyncio.sleep(dur_before_hash)
            time_hash = self.u.get_recent_hash()
            await asyncio.sleep(dur_before_send)
            self.u.send_with_timehash(to_pub, amt, time_hash)

async def pbar(step: float, dur: float, *args):
    n = int(dur / step)
    for _ in tqdm(range(n)):
        await asyncio.sleep(step)
    for arg in args:
        arg.finish()
    asyncio.get_running_loop().stop()

p = 997
g = 7

acc_len = 100
poh_initial = b'poh_initial'
poh_per = 0.1

duration = 10
step = 0.1
unwind_per = 0.8

tx_h = tx_handler.TxHandler(p, g, poh_initial, acc_len, poh_per, unwind_per)

u1_scenario = [
    (1, 0, 10),
    (0.5, 0, 15),
    (0.1, 0, 1)
]

u2_scenario = [
    (1, 0, 10),
    (0.5, 0, 15),
    (0.1, 0, 1)
]

u1 = UserExec(user.User(tx_h, p, g), u1_scenario)
u2 = UserExec(user.User(tx_h, p, g), u2_scenario)

coros = [
    u1.run(u2.u.pub),
    u2.run(u1.u.pub),
    tx_h.handle_transactions(),
    tx_h.poh.run(),
    pbar(step, duration, u1.u, u2.u, tx_h)
]

for coro in coros:
    asyncio.ensure_future(coro)

loop = asyncio.get_event_loop()
print(f"Run simulation for {duration} seconds")
loop.run_forever()
