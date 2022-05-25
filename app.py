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
        self.show()

    def init_stepper(self):
        print('initializing...')
        self.enable = 17
        self.step = 27
        self.dir = 22
        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.step, pigpio.OUTPUT)
        self.pi.set_mode(self.dir, pigpio.OUTPUT)
        self.pi.write(self.dir, 0)

    def initialize_ui(self):
        self.setGeometry(100, 100, 500, 250)

        degree_minus_360 = QPushButton('-360°', self)
        degree_minus_360.move(10, 10)
        degree_minus_360.resize(100, 40)
        degree_minus_360.clicked.connect(lambda: self.decrease_degree(360))
        degree_minus_10 = QPushButton('-10°', self)
        degree_minus_10.move(110, 10)
        degree_minus_10.resize(100, 40)
        degree_minus_10.clicked.connect(lambda: self.decrease_degree(10))
        degree_plus_10 = QPushButton('+10°', self)
        degree_plus_10.move(210, 10)
        degree_plus_10.resize(100, 40)
        degree_plus_10.clicked.connect(lambda: self.increase_degree(10))
        degree_minus_360 = QPushButton('+360°', self)
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

    def start(self):
        print('Starting...')
        rotate_thread = threading.Thread(name='start_rotation', target=self.rotate)
        rotate_thread.daemon = True
        rotate_thread.start()

    def rotate(self):
        self.pi.write(self.enable, 0)
        sleep(10)
        rounds = self.rotations/360*1600  # (1600 * self.rotations*10)/10  # 1600 sind 360°
        for i in range(0, int(rounds)):
            print(i)
            self.pi.write(self.step, 1)
            sleep(0.001)
            self.pi.write(self.step, 0)
            sleep(0.001)

        sleep(5)
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
    sys.exit(app.exec())
