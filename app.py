from PyQt5.QtWidgets import QApplication, \
    QWidget, \
    QPushButton, \
    QLineEdit, \
    QLabel
import pigpio
from time import sleep
import os
import sys
import platform
import threading

from encoder import encoder
import global_values

if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class PushBtn(QPushButton):
    def __init__(self):
        super().__init__()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.dir = None
        self.step = None
        self.enable = None
        self.rotations_input = None
        if platform.system() == 'Linux':
            self.pi = pigpio.pi()
            self.init_stepper()
        self.rotations = 360
        self.initialize_ui()
        self.start_direction_sensor()
        self.show()

    def init_stepper(self):
        print('initializing...')
        self.enable = 16
        self.step = 23
        self.dir = 24
        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.step, pigpio.OUTPUT)
        self.pi.set_mode(self.dir, pigpio.OUTPUT)
        self.pi.write(self.dir, 0)

    def start_direction_sensor(self):
        t1 = threading.Thread(target=encoder)
        t1.daemon = True
        t1.start()
        t2 = threading.Thread(target=self.update_rotation_direction)
        t2.daemon = True
        t2.start()

    def update_rotation_direction(self):
        while True:
            rot_dir = global_values.get_rot_dir()
            # print(f'current value of rot: {rot_dir}')
            # self.direction_input.setText(str(rot_dir))

            degree = global_values.get_degree()
            self.direction_input.setText(str(degree))
            sleep(0.1)

    def initialize_ui(self):
        self.setGeometry(100, 100, 500, 250)

        degree_minus_360 = QPushButton('-360 deg', self)
        degree_minus_360.move(10, 10)
        degree_minus_360.resize(100, 40)
        degree_minus_360.clicked.connect(lambda: self.decrease_degree(360))
        degree_minus_10 = QPushButton('-10 deg', self)
        degree_minus_10.move(110, 10)
        degree_minus_10.resize(100, 40)
        degree_minus_10.clicked.connect(lambda: self.decrease_degree(10))
        degree_plus_10 = QPushButton('+10 deg', self)
        degree_plus_10.move(210, 10)
        degree_plus_10.resize(100, 40)
        degree_plus_10.clicked.connect(lambda: self.increase_degree(10))
        degree_minus_360 = QPushButton('+360 deg', self)
        degree_minus_360.move(310, 10)
        degree_minus_360.resize(100, 40)
        degree_minus_360.clicked.connect(lambda: self.increase_degree(360))

        rotations_lbl = QLabel('Degree:', self)
        rotations_lbl.move(10, 60)
        self.rotations_input = QLineEdit(str(self.rotations), self)
        self.rotations_input.move(70, 60)

        start_button = QPushButton('Start', self)
        start_button.move(10, 100)
        start_button.resize(100, 40)
        start_button.clicked.connect(self.start)

        exit_btn = QPushButton('Exit', self)
        exit_btn.move(380, 200)
        exit_btn.resize(100, 40)
        exit_btn.clicked.connect(self.close_app)

        direction_lbl = QLabel('Rotary Direction', self)
        direction_lbl.move(10, 160)
        # direction_lbl.resize(150, 40)
        self.direction_input = QLineEdit('Stopped', self)
        self.direction_input.move(150, 160)


    def start(self):
        if platform.system() == 'Linux':
            print('Starting...')
            rotate_thread = threading.Thread(name='start_rotation', target=self.rotate)
            rotate_thread.daemon = True
            rotate_thread.start()
        else:
            print("Can't start. Not on Linux System.")

    def rotate(self):
        # self.pi.write(self.enable, 0)  # Motorsperre aktivieren
        sleep(1)
        rounds = self.rotations/360*1600  # (1600 * self.rotations*10)/10  # 1600 sind 360
        direction = 1 if rounds < 0 else 0
        print(f'direction: {direction}')
        self.pi.write(self.dir, direction)
        if rounds < 0:
            rounds = rounds * -1

        print(rounds)
        for i in range(0, int(rounds)):
            # print(i)
            self.pi.write(self.step, 1)
            sleep(0.001)
            self.pi.write(self.step, 0)
            sleep(0.001)

        sleep(0.5)  # Motorsperre deaktvieren
        self.pi.write(self.enable, 1)

    def close_app(self):
        print('Exiting application...')
        self.close()

    def increase_degree(self, value):
        self.rotations = round(self.rotations + value, 1)
        self.rotations_input.setText(str(self.rotations))
        print(f'increased by {self.rotations}')

    def decrease_degree(self, value):
        self.rotations = round(self.rotations - value, 1)
        self.rotations_input.setText(str(self.rotations))
        print(f'decreased by {self.rotations}')



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    # appex = app.exec()
    sys.exit(app.exec())
