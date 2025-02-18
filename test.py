from time import sleep
import pigpio


pi = pigpio.pi()


class Stepper:
    def __init__(self):
        self.enable = 0
        self.step = 0
        self.dir = 0
        self.init_stepper()

    def init_stepper(self):
        print('initializing...')
        self.enable = 17 # 17
        self.step = 23 # 27
        self.dir = 24 # 22
        pi.set_mode(self.enable, pigpio.OUTPUT)
        pi.set_mode(self.step, pigpio.OUTPUT)
        pi.set_mode(self.dir, pigpio.OUTPUT)
        pi.write(self.dir, 0)

    def start(self):
        print('start')

    def lock(self):
        print('loose')
        pi.write(self.enable, 0)  # Stepper loesen
        sleep(3)
        print('lock')
        pi.write(self.enable, 1)  # Stepper sperren
        sleep(15)

    def turn(self):
        try:
            counter = 0
            while counter < 10000:
                counter += 1
                pi.write(self.dir, 1)
                # pi.write(self.enable, 0)
                sleep(0.5)
                rounds = 200
                for i in range(rounds):
                    pi.write(self.step, 1)
                    sleep(0.001)
                    pi.write(self.step, 0)
                    sleep(0.001)

                pi.write(self.dir, 0)
                for i in range(rounds):
                    pi.write(self.step, 1)
                    sleep(0.001)
                    pi.write(self.step, 0)
                    sleep(0.001)

                sleep(0.5)
                pi.write(self.enable, 1)

        except KeyboardInterrupt:
            print('interrupted')
        finally:
            print('finished')



tmc2208 = Stepper()
tmc2208.start()

tmc2208.turn()

pi.stop()

