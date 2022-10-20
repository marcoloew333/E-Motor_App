import pigpio
from time import sleep

pi = pigpio.pi()

pin_a = 27
pin_i = 27
pin_b = 17

pi.set_mode(pin_a, pigpio.INPUT)
pi.set_mode(pin_i, pigpio.INPUT)
pi.set_mode(pin_b, pigpio.INPUT)

clkLastState = pi.read(pin_a)

while True:
    read_a = pi.read(pin_a)
    read_i = pi.read(pin_i)
    read_b = pi.read(pin_b)
    print(f'pin_a: {read_a}')
    print(f'pin_i: {read_i}')
    print(f'pin_b: {read_b}')
    # print('\n')
    # if read_a != clkLastState:
    #     if dtState != read_a:
    #         counter += 1
    #     else:
    #         counter -= 1
    #     print(counter)
    # clkLastState = clkState
    sleep(1)
    print('\n\n')


