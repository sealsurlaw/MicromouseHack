from driver import Driver
from threading import Timer
import time

mouse = Driver()

def ping(mouse):
    sen1, sen2, sen3 = mouse.ping()

    print('right: {0:7.2f}    left: {1:7.2f}    forward: {2:7.2f}'.format(sen1,sen2,sen3))

    t = Timer(0.1, ping(mouse))
    t.start()

t = Timer(0.1, ping(mouse))
t.start()

while True:
    sleep(10)
