# TODO: Extremely unfinished, but a basic PyQt6 / PySide6 setup

import random as rand
import sys
from typing import List, Tuple

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

FOLDER = "pictures"
ROCK, PAPER, SCISSOR = "rock", "paper", "scissor"
IMAGES = {
    ROCK: f"{FOLDER}/rock.png",
    PAPER: f"{FOLDER}/paper.png",
    SCISSOR: f"{FOLDER}/scissor.png"
}

AMOUNT = 10
WIDTH, HEIGHT = 500, 500
FRAMES = 10


class Element:
    SIZE: int = 15
    SPEED: int = 5

    img: QLabel
    elem: str
    x: int
    y: int
    horizontal: float  # [-1, 1]
    vertical: float  # [-1, 1]

    def __init__(self, elem: str, win: QMainWindow):
        self.x, self.y, self.horizontal, self.vertical = Element._get_start_values()
        self.img = QLabel(win)
        self.img.setScaledContents(True)
        self.change_elem(elem)
        self.show()

    @staticmethod
    def _get_start_values():
        """Return x, y, horizontal, vertical values"""
        return rand.randrange(WIDTH - Element.SIZE), rand.randrange(HEIGHT - Element.SIZE), rand.random(), rand.random()

    def change_elem(self, elem: str):
        self.elem = elem
        self.img.setPixmap(QPixmap(IMAGES[elem]))

    def _randomize_dir(self):
        def get_change():
            return rand.randint(-1, 1) * (rand.random() / (FRAMES * 3))

        def new_val(old: float):
            op, bound = (min, 1) if (change := get_change()) > 0 else (max, 0)
            return op(old + change, bound)

        self.horizontal = new_val(self.horizontal)
        self.vertical = new_val(self.vertical)

    def show(self):
        self.img.setGeometry(int(self.x), int(self.y), Element.SIZE, Element.SIZE)
        self.img.show()

    def update_pos(self):
        self._randomize_dir()
        self.x += self.horizontal * Element.SPEED
        self.y += self.vertical * Element.SPEED
        self.show()

    def _check_collision(self, other: "Element") -> bool:
        return abs(self.x - other.x) < Element.SIZE > abs(self.y - other.y) and self.elem != other.elem

    def handle_collision(self, other: "Element"):
        if self._check_collision(other):
            if (self.elem == ROCK and other.elem == SCISSOR) \
                    or (self.elem == SCISSOR and other.elem == PAPER) \
                    or (self.elem == PAPER and other.elem == ROCK):
                other.change_elem(self.elem)
            else:
                self.change_elem(other.elem)


def init_game(win: QMainWindow):
    return [Element(elem, win) for elem in IMAGES for _ in range(AMOUNT)], [AMOUNT] * len(IMAGES)


def game_loop(win: QMainWindow, xss: Tuple[List[Element], List[int]]):
    elems = xss[0]

    for elem in elems:
        elem.update_pos()

    for i, elem in enumerate(elems):
        for j in range(i, len(elems)):
            elem.handle_collision(elems[j])

    win.update()


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()

    win.setGeometry((1920 - WIDTH) // 2, (1080 - HEIGHT) // 2, WIDTH, HEIGHT)
    win.setWindowTitle("Rock Paper Scissors")
    win.show()

    game_data = init_game(win)

    timer = QTimer()
    timer.setInterval(1000 // FRAMES)
    timer.timeout.connect(lambda: game_loop(win, game_data))
    timer.start()

    sys.exit(app.exec())


if __name__ == '__main__':
    window()



