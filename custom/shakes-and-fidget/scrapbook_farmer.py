import random
from typing import Dict, Tuple
import pyautogui as pg
import time


def _sleep(t: float = 0.4):
    time.sleep(t)


def _click(x, y, clicks=1, interval=0.2):
    pg.click(x, y, clicks=clicks, interval=interval)  # interval is only useful if multiple clicks should be done


_press = pg.press

SEARCH_FIELD = 680, 980
ITEM_SIZE = 126, 126
ITEM_COORDS: Dict[str, Tuple[int, int]] = {
    "hat": (1161, 120),
    "body": (1161, 252),
    "gloves": (1161, 385),
    "boots": (1161, 518),
    "weapon1": (1343, 518),
    "weapon2": (1477, 518),
    "talisman": (1659, 518),
    "ring": (1659, 385),
    "belt": (1659, 252),
    "necklace": (1659, 120)
}


def _goto_hof():
    _press('g')
    _sleep()
    _press('h')
    _sleep(0.5)


def _sc_items(coords: Dict[str, Tuple[int, int]]):
    return {item: pg.screenshot(region=(*xy, *ITEM_SIZE)) for item, xy in coords.items()}


def _eval_cur_items() -> int:
    old = _sc_items(ITEM_COORDS)
    _sleep()
    new = _sc_items(ITEM_COORDS)

    # for now I only care about the item count, but in later versions one may also want to be able to figure out
    # which items are unowned still
    def comp_ims(im1, im2, item):
        # im1.show()
        # im2.show()
        if list(im1.getdata()) != list(im2.getdata()):
            # print(f"diff in {item}. Opening both pictures now...")
            # im1.show()
            # im2.show()
            # input("press enter to continue")
            return True

        return False

    return sum(comp_ims(old_im, new[item], item) for item, old_im in old.items())


def find_scrapbook(start=15000, exact=True, alert=1, direction=None, auto_attack=False):
    """Main event loop.
    :param start: leaderboard position to start the search at
    :param exact: Weather the exact start value should be used, otherwise it's randomized around the start value
    :param alert: minimum amount of uncollected items for the script to trigger
    :param direction: 'up' if you want to go upwards in the HoF, 'down' for downwards, 'None' for random direction
    :param auto_attack: False => script stops when it spots a matching player, True => script automatically attacks and
                continues its search"""

    print("starting search in 5 seconds...")
    _sleep(5)
    # start_time = time.time()

    if not exact:
        start += random.randint(-start // 2, start // 2)

    if direction is None or direction not in ('up', 'down'):
        direction = 'up' if random.randint(0, 1) else 'down'

    _goto_hof()
    _sleep()
    _click(*SEARCH_FIELD, clicks=1)
    for c in str(start):
        _press(c)

    _press("enter")

    attempts = 0

    while True:
        attempts += 1
        _sleep(0.6)
        diffs: int = _eval_cur_items()
        print(f"{attempts:4d}: {diffs = }")
        if diffs >= alert:
            if not auto_attack:
                print("!FOUND SOMEONE!")
                break
            else:
                _press('num9')  # num 9 is attack
                _sleep(0.1)
                _press('enter')
                _sleep()
                _press('enter')

        _press(direction)

    # print(f"Evaluated {attempts} players over {time.time() - start_time:.1f} seconds to find a match.")


if __name__ == '__main__':
    _click(680, 980)
    _press('g')
    _sleep()
    _press('h')
    _sleep(0.5)
    _press('enter')
    _press('num9')
    target_coords = 500, 450
    _click(*target_coords, clicks=100, interval=1)


