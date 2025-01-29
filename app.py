
from PyQt5.QtWidgets import QApplication, \
    QWidget, \
    QPushButton, \
    QLineEdit, \
    QLabel
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import platform
if platform.system() == "Linux":
    import pigpio
from time import sleep
import os
import sys
# import threading

from servo import Servo, ServoDummy
# from encoder import encoder
# import global_values

if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class RotateWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, pi, rotations, direction, enable, step):
        super().__init__()
        self.pi = pi
        self.rotations = rotations
        self.dir = direction
        self.enable = enable
        self.step = step

    def run(self):
        try:
            sleep(1)
            rounds = self.rotations / 360 * 1600  # (1600 * self.rotations*10)/10  # 1600 sind 360
            direction = 1 if rounds < 0 else 0
            if rounds < 0:
                rounds = rounds * -1
            if platform.system() == "Linux":
                self.pi.write(self.dir, direction)
                for i in range(0, int(rounds)):
                    # print(i)
                    self.pi.write(self.step, 1)
                    sleep(0.001)
                    self.pi.write(self.step, 0)
                    sleep(0.001)
            else:
                for i in range(0, int(rounds)):
                    sleep(0.001)
                    sleep(0.001)
                    print(i)

            sleep(0.5)  # Motorsperre deaktvieren
            # self.pi.write(self.enable, 1)
        except BaseException as e:
            print("Error in RotationWorker", e)
        finally:
            # print("RotationWorker finished")
            self.finished.emit()


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
        self.pi = None
        self.servo = ServoDummy()
        if platform.system() == 'Linux':
            self.pi = pigpio.pi()
            # self.init_stepper()
            self.servo = Servo(self.pi)
        self.rotations = 360
        self.initialize_ui()
        # self.start_direction_sensor()
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

    # def start_direction_sensor(self):
    #     # encoder()  # Das Starten als Thread ist scheinbar nicht notwendig
    #     # t1 = threading.Thread(target=encoder)
    #     # t1.daemon = True
    #     # t1.start()
    #     t2 = threading.Thread(target=self.update_rotation_direction)
    #     t2.daemon = True
    #     t2.start()
    #
    # def update_rotation_direction(self):
    #     while True:
    #         rot_dir = global_values.get_rot_dir()
    #         # print(f'current value of rot: {rot_dir}')
    #         # self.direction_input.setText(str(rot_dir))
    #
    #         degree = global_values.get_degree()
    #         self.direction_input.setText(str(degree))
    #         sleep(0.1)

    def initialize_ui(self):
        self.setGeometry(20, 200, 700, 350)

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
        start_button.resize(200, 80)
        start_button.clicked.connect(self.servo.move_servo)

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
        # try:
        print('Starting...')
        self.t = QThread()  # parent=self
        self.w = RotateWorker(pi=self.pi, rotations=self.rotations, direction=self.dir, enable=self.enable, step=self.step)
        self.w.moveToThread(self.t)
        self.t.started.connect(self.w.run)
        self.w.finished.connect(self.t.quit)
        self.w.finished.connect(self.w.deleteLater)
        self.t.finished.connect(self.t.deleteLater)
        self.t.start()
        # except BaseException as e:
        #     print("Error in start", e)

    # def rotate(self):
    #     sleep(1)
    #     rounds = self.rotations/360*1600  # (1600 * self.rotations*10)/10  # 1600 sind 360
    #     direction = 1 if rounds < 0 else 0
    #     self.pi.write(self.dir, direction)
    #     if rounds < 0:
    #         rounds = rounds * -1
    #
    #     for i in range(0, int(rounds)):
    #         # print(i)
    #         self.pi.write(self.step, 1)
    #         sleep(0.001)
    #         self.pi.write(self.step, 0)
    #         sleep(0.001)
    #
    #     sleep(0.5)  # Motorsperre deaktvieren
    #     self.pi.write(self.enable, 1)

    def close_app(self):
        print('Exiting application...')
        self.close()

    def increase_degree(self, value):
        self.rotations = round(self.rotations + value, 1)
        self.rotations_input.setText(str(self.rotations))
        # print(f'increased by {self.rotations}')

    def decrease_degree(self, value):
        self.rotations = round(self.rotations - value, 1)
        self.rotations_input.setText(str(self.rotations))
        # print(f'decreased by {self.rotations}')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
