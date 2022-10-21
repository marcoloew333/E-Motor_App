import pigpio
from time import sleep

import global_values

def encoder():
    pi = pigpio.pi()

    pin_a = 19 # m2:14 m1:19
    pin_b = 6 # m2:15 m1:6
    pin_i = 26 # m2:18 m1:26

    pi.set_mode(pin_a, pigpio.INPUT)
    pi.set_mode(pin_b, pigpio.INPUT)
    pi.set_mode(pin_i, pigpio.INPUT)

    degree = global_values.get_degree()
    read_a_prev = pi.read(pin_a)

    print(f'Start values of encoder: Pin A: {pi.read(pin_a)}, Pin B: {pi.read(pin_b)}')

    while True:
        read_a = pi.read(pin_a)
        read_b = pi.read(pin_b)
        read_i = pi.read(pin_i)
        print(read_a, read_b, read_i)
        # print(f'pin_a: {read_a}')
        # print(f'pin_b: {read_b}')
        # print('\n')
        if read_a_prev != read_a:
            # print(f'read_a_prev != read_a: {read_a_prev != read_a}')
            # sleep(0.5)
            if read_b != read_a:
                # print(read_a, read_b)
                # print('links')
                global_values.update_rot_dir('left')
                # print(f'read_b != read_a: {read_b != read_a}')
                # sleep(0.5)
                degree += 1
                global_values.update_degree(degree)
            else:
                # print(read_a, read_b)
                # print('rechts')
                global_values.update_rot_dir('right')
                # print(f'read_b != read_a: {read_b != read_a}')
                degree -= 1
                global_values.update_degree(degree)
            # print(counter)
        read_a_prev = read_a
        sleep(0.01)
        # print('\n')


