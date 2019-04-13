from driver import Driver
from threading import Timer
import time

mouse = Driver()
count = 0

def checkSides(mouse):
    global count

    right, left, forward = mouse.ping()
    print(right)
    count += 1

t = Timer(0.5, checkSides(mouse))
t.start()

#mouse.forward(speed=40)

while count < 5:
    print(count)
    time.sleep(5)

#mouse.stop()

del mouse
