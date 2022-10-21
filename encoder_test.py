import pigpio
from time import sleep

def encoder_test():
    pi = pigpio.pi()

    pin_a = 9
    pin_b = 5

    pi.set_mode(pin_a, pigpio.INPUT)
    pi.set_mode(pin_b, pigpio.INPUT)
    
    while True:
        print(pi.read(pin_a), pi.read(pin_b))

encoder_test()
