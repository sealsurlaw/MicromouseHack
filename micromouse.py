from driver import Driver
import time

mouse = Driver()

print('forward')

mouse.forward()

time.sleep(2)

mouse.stop()

time.sleep(0.5)

print('backward')

mouse.backward()

time.sleep(2)

print('slow down')

mouse.changeSpeed(20)

time.sleep(2)

print('go left')

mouse.left()

print('stop')

mouse.stop()

right, left, forward = mouse.ping()

print('right: {}'.format(right))
print('left: {}'.format(left))
print('forward: {}'.format(forward))

del mouse
