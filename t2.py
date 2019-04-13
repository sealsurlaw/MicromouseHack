from driver import Driver
import time

mouse = Driver()

speed=40

#mouse.forward(speed=speed)

print('Got here')

start = time.time()

mouse.forward(speed=speed)

f = 1000.0
lastF = 1000.0
lSpeed = speed
rSpeed = speed
correction = 0.3
while f > 10.0:
    r, l, f = mouse.ping()
    diff = r - l
    print('f: {}    diff: {}'.format(f, diff))

    if lSpeed != speed:
        mouse.changeSpeed(speed)
        lSpeed = speed
        print('Fixed')
    elif rSpeed != speed:
        mouse.changeSpeed(speed)
        rSpeed = speed
        print('Fixed')
    elif diff > 0.5 and diff < 20:
        rSpeed = speed - correction
        mouse.changeSpeed(rSpeed, side='right')
        print('Corrected')
    elif diff < -0.5 and diff > -20:
        lSpeed = speed - correction
        mouse.changeSpeed(lSpeed, side='left')
        print('Corrected')

    temp = f
    f = (lastF + f) / 2
    lastF = temp

    time.sleep(0.1)

stop = time.time()
elapsed = stop - start
print(elapsed)
