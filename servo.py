import pigpio

class Servo:
    def __init__(self, pigpio_pi, pwm_pin=18):
        self.pi = pigpio_pi
        self.freq = 50  # in Hz
        self.pwm = pwm_pin
        self.angle_min = 0
        self.angle_max = 180
        self.pulse_width_min = 500
        self.pulse_width_max = 2500

    def angle_to_pulse_width(self, angle):
        return int(
            (angle - self.angle_min) * (self.pulse_width_max - self.pulse_width_min) / (self.angle_max - self.angle_min) + self.pulse_width_min)

    def move_servo(self, angle=90):
        pulse_width = self.angle_to_pulse_width(angle)
        print(pulse_width)
        self.pi.set_servo_pulsewidth(self.pwm, 500)

pi = pigpio.pi()
my_servo = Servo(pi)
my_servo.move_servo()
my_freq = my_servo.freq  # Lesen
my_servo.freq = 60  # Schreiben
















class ServoDummy:
    def angle_to_pulse_width(self):
        pass

    def move_servo(self):
        pass





if __name__ == '__main__':
    print("start")
    pi = pigpio.pi()
    s = Servo(pi)
    s.move_servo()
    pi.stop()
