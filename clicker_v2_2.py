# coding:gbk
# script builder: f233xdd
# basic code source: https://pynput.readthedocs.io/en/latest/keyboard.html?highlight=keyboard#monitoring-the-keyboard
# third-party dependent libraries: pyautogui, pynput, PySide6
# run on Python 3.11.1
import threading
import time

import pyautogui
from pynput import keyboard
from PySide6.QtWidgets import (QApplication, QLabel, QDialog,
                               QPushButton, QLineEdit, QVBoxLayout)

import debugger

debug: bool = True
show_press_key: bool = True

pyautogui.PAUSE = 0.1
is_GUI: bool = True


class Clicker(keyboard.Listener):

    def __init__(self, do_key, stop_key):
        super().__init__(on_press=self.__on_press)
        self.do_key = do_key  # start clicker key
        self.stop_key = stop_key  # stop clicker key
        self.press = ''

    def __on_press(self, p_key):
        """Get press keys and print them on the terminal."""
        time.sleep(0.001)  # lower use of CPU
        try:
            self.press = p_key.char
            if show_press_key:
                print(f"Press: {self.press}", flush=True)

        except AttributeError:
            self.press = p_key
            if show_press_key:
                print(f"Press: {self.press}", flush=True)

    @debugger.start_and_exit_sign(debug=debug)
    def start(self):
        """Start keyboard listener thread."""
        super().start()
        self.clicker()

    @debugger.start_and_exit_sign(debug=debug)
    def clicker(self):
        """Check the key and control the clicker."""
        while True:
            time.sleep(0.001)  # lower use of CPU

            if self.press == self.do_key:
                self.press = None
                run_or_not = True  # set run_or_not to reach one of the start condition

                while run_or_not:
                    time.sleep(0.001)  # lower use of CPU
                    pyautogui.click()

                    if self.press == self.stop_key:
                        self.press = None  # avoid press is still the same as do_press
                        run_or_not = False


class MainWindow(QDialog):

    def __init__(self):
        super().__init__()
        # create the parts
        self.label = QLabel("You've run this script successfully.\nType key 'F' to start and to stop.")
        self.pause = QLineEdit("Enter pause time (seconds).")
        self.button = QPushButton("Change it!")
        # create the box, add the parts into the box
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.pause)
        self.layout.addWidget(self.button)
        # use the box
        self.setLayout(self.layout)
        # connect the button with the function
        self.button.clicked.connect(self.set_pause)

    def set_pause(self):
        """Set the pause time."""
        try:
            pyautogui.PAUSE = float(self.pause.text())
        except ValueError:
            print('\a')  # FIXME: say something to warn user!

    @staticmethod
    def create_window():
        """Create the main window"""
        if is_GUI:
            window = QApplication([])
            main_window = MainWindow()
            main_window.show()
            window.exec()
        else:
            print("WARNING: is_GUL is False.")


def main():
    a_clicker = Clicker('f', 'f')
    thread_window = threading.Thread(target=MainWindow.create_window)
    thread1 = threading.Thread(target=a_clicker.start, daemon=True)

    thread_window.start()
    thread1.start()

    if is_GUI:
        thread_window.join()
    else:
        thread1.join()

    return 0


if __name__ == '__main__':
    main()
