# coding:gbk
# script builder: f233xdd
# basic code source: https://pynput.readthedocs.io/en/latest/keyboard.html?highlight=keyboard#monitoring-the-keyboard
# third-party dependent libraries: pyautogui, pynput
# run on Python 3.11.1
from threading import Thread
from time import sleep
from sys import exit as sys_exit
from os import _exit as os_exit

import pyautogui
from pyautogui import click
from pynput import keyboard

# debug options
debug: bool = False  # this will show you when functions are start and over if it's True
keyboard_debug: bool = False  # this will show you the keys which Pynput gets if it's True

# optional functions
pyautogui.PAUSE = 0.01  # time(second) between every single click

# unchangeable variables
press = None  # not exactly
clicker_start = False
listener_start = False


def on_press(key):
    """Get press keys and print them on the terminal."""
    global press

    try:
        press = key
        if keyboard_debug:
            print(f"Press: {key}")
    except AttributeError:
        press = key
        if keyboard_debug:
            print(f"Press: {key}")


def on_release(key):
    """Get release keys and control the quit of listener."""
    if key == keyboard.Key.alt_gr:
        # Stop listener
        os_exit(0)


def start_listener():
    """Start keyboard listener thread."""
    global listener_start

    listener = keyboard.Listener(
        on_press=on_press, on_release=on_release)
    listener.start()

    if debug:
        print("——————————— Keyboard listener start! ————————————")  # debugger
    listener_start = True
    listener.join()

    if debug:
        print("———————————— Keyboard listener stop! ————————————")  # debugger
        sys_exit(0)


def clicker():
    """Check the key and control the clicker."""
    global press, clicker_start
    do_press = keyboard.Key.alt_l  # start clicker key
    stop_press = keyboard.Key.alt_l  # stop clicker key

    if debug:
        print("———————————— Clicker thread start! ————————————")  # debugger
    clicker_start = True

    while not (press == keyboard.Key.alt_gr):

        if press == do_press:
            press = None
            run_or_not = True  # set run_or_not to reach one of the start condition

            while run_or_not:
                click()

                if press == stop_press:
                    press = None  # avoid press is still the same as do_press
                    run_or_not = False

    else:
        print("See you next time!")
        if debug:
            print("\n———————————— Clicker thread stop! ————————————")  # debugger
            sys_exit(0)


def print_str():
    """Print something on the terminal to print_str oneself."""
    if debug:
        print("———————————— Print thread start! ————————————")  # debugger

    while not (clicker_start and listener_start):
        for letter in ['w', 'a', 'i', 't', 'i', 'n', 'g', '.', '.', '.']:
            print(letter, end='', flush=True)
            sleep(0.25)
        sleep(1)
        print('\r', end='', flush=True)
        sleep(1)

    if not debug:
        print("\rNow you can use it.")
        print("Type [LEFT_ALT] to start and [RIGHT_ALT] to stop.")
        sys_exit(0)
    else:
        print("———————————— Print thread stop! ————————————")  # debugger
        print("============ All the modules are ready! ============")  # debugger
        sys_exit(0)


def main():
    """Start the whole clicker script."""
    if debug:
        print("———————————— Main thread start! ————————————")  # debugger

    thread1 = Thread(target=clicker)
    thread1.daemon = True
    thread2 = Thread(target=start_listener)
    thread3 = Thread(target=print_str)
    thread_list = [thread1, thread2, thread3]
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    if debug:
        print("———————————— Main thread stop! ————————————")  # debugger
    return 0


if __name__ == '__main__':
    sys_exit(main())
else:
    print("You have imported a wrong extant pack!")
