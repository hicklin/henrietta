"""Print 'Hello World' every two seconds, using a callback."""

import asyncio
import time

def print_and_repeat(loop, timea):
    print(timea)
    timeb = timea+0.01
    loop.call_at(timeb, print_and_repeat, loop, timeb)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    timea = loop.time()
    print_and_repeat(loop, timea)
    loop.run_forever()
    time.sleep(2)
    print("hello")
    loop.close()
