import time

import pyautogui as pg


def sleep(t: float = 0.4):
    time.sleep(t)


def click(x, y, clicks=1, interval=0.1):
    pg.click(x, y, clicks=clicks, interval=interval)  # you also have a 'duration' attribute that you could set this way


press = pg.press
move = pg.moveTo

# Here we're done with all the setup we need
# Now some examples to showcase how to press a few keyboard buttons
press('a')  # In Python both 'a' and "a" are equivalent
press('x')
press('enter')  # presses the ENTER key
press('num9')  # presses the 9 on the NUMPAD
press("up")  # presses the arrow-key UP
press('f8')  # presses the F8 key

# Here are now some examples to showcase how to make a mouse-movement
# Multi-monitor setups may have negative x pixel values if the second screen is on the left of the primary screen.
move(100, 100)  # moves to pixel x=100,y=100
move(300, 1000)  # moves to pixel x=300,y=1000

# And now some examplse to showcase how to perform clicks at certain pixel values
click(150, 200)  # performs a single click at pixel x=150,y=200
click(300, 500, clicks=3)  # performs 3 consecutive clicks - each with the default interval-duration in between
click(400, 54, clicks=5, interval=1)  # performs 5 consecutive clicks with one second between each click
