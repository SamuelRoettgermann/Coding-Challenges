"""The OCR stuff here is basically unusable, at least based on the results"""

import csv
import datetime
import random
import time
import math
from pathlib import Path
from typing import Dict, Tuple

import pyautogui as pg
import pytesseract
from PIL import Image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAME_COLOUR = 239, 191, 65
HOVER_COLOUR = WHITE
IM_FOLDER = "sf_ims"


def get_guild_members(guild: str):
    with open(f"SF-{guild}.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, [(e['name'], int(e['level']), int(e['treasure']), int(e['instructor'])) for e in
                                   reader]


def sort_guild_members(guild: str):
    fields, data = get_guild_members(guild)
    s_data = sorted(data, key=lambda x: (x[3], x[2], -x[1], x[0]))

    print(f"[{', '.join(fields)}]")
    for row in s_data:
        print(str(row)[1:-1])


# GUILD_BUTTON = 300, 750
FIRST_PLAYER = 680, 245
TEXT_FIRST_PLAYER = 731, 169
DIFFERENCE_HOVER_TEXT = *tuple(a - b for a, b in zip(TEXT_FIRST_PLAYER, FIRST_PLAYER)), 31, 58
HOVER_LINE_Y = 17
HOVER_LINE_GAP = 5
Y_DIFF = 24
NAME_AFTER_CLICK = (*(1333, 403), 270, 26)


def sleep(t: float = 0.4):
    time.sleep(t)


def click(x, y, clicks=1, interval=0.1):
    pg.click(x, y, clicks=clicks, interval=interval)


press = pg.press


def goto_guild():
    press('g')
    sleep(.5)


def sc_name():
    return clear_img(pg.screenshot(region=NAME_AFTER_CLICK), NAME_COLOUR)


def click_player(y, x=680):
    click(x, y)
    sleep()
    pg.moveTo(100, 100)  # some other part of the screen
    sleep()
    pg.moveTo(x, y)
    sleep()

    def sc_hover():
        """Takes 3 seperate screenshots of all hover values (treasure, instructor, knights)"""
        adj_coords = (x + DIFFERENCE_HOVER_TEXT[0], y + DIFFERENCE_HOVER_TEXT[1], *DIFFERENCE_HOVER_TEXT[2:])
        coords_treasure = *adj_coords[:3], HOVER_LINE_Y
        coords_instructor = (adj_coords[0], adj_coords[1] + HOVER_LINE_Y + HOVER_LINE_GAP, adj_coords[2], HOVER_LINE_Y)
        coords_guild_pet = (
            adj_coords[0], adj_coords[1] + 2 * HOVER_LINE_Y + 2 * HOVER_LINE_GAP, adj_coords[2], HOVER_LINE_Y)

        return [pg.screenshot(region=coords_treasure), pg.screenshot(region=coords_instructor), pg.screenshot(
            region=coords_guild_pet)]

    return [sc_name()] + [clear_img(im, HOVER_COLOUR, tolerance=200) for im in sc_hover()]


def clear_img(im, match_colour, tolerance=5):
    pixels = im.load()

    def in_tolerance(rgb):
        r, g, b = rgb
        ro, go, bo = match_colour
        return abs((ro - r) + (go - g) + (bo - b)) < tolerance

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            im.putpixel((x, y), BLACK if in_tolerance(pixels[x, y]) else WHITE)

    return im


def save_guild_members():
    TIMESTAMP = datetime.datetime.now().strftime("%d-%m-%Y#%H-%M-%S")
    HEAD_PATH = Path(__file__).parent / f"{IM_FOLDER}/{TIMESTAMP}"
    Path(HEAD_PATH).mkdir(parents=True, exist_ok=True)
    goto_guild()

    i = 0
    y = FIRST_PLAYER[1]

    data = []

    while True:
        old: Image

        def has_next():
            nonlocal y
            nonlocal old

            if i == 0:
                click(FIRST_PLAYER[0], y)
                sleep()
                old = sc_name()
                return True

            def player_cmp():
                nonlocal old
                click(FIRST_PLAYER[0], y)
                sleep()
                comp: Image = sc_name()
                ret = list(comp.getdata()) != list(old.getdata())
                old = comp
                return ret

            if player_cmp():
                return True

            # if the name is the same then y might be too low and we need to scroll from now on
            y -= Y_DIFF
            pg.moveTo(FIRST_PLAYER[0], y)
            pg.scroll(-1)  # scroll down by 1
            return player_cmp()

        if not has_next():
            break

        clean_ims = click_player(y)
        data.append(tuple(map(parse_image, clean_ims)))

        i += 1
        y += Y_DIFF

    display_data(data)


def display_data(data: list):
    for name, treasure, instructor, pet in data:
        print(f"{name},{treasure},{instructor},{pet}")


def parse_image(im):
    return pytesseract.image_to_string(im, config='--psm 6')


# HOF = 300, 865
# HOF2 = (-1920 + HOF[0]), (HOF[1] + 25)  # offset cause no taskbar on 2nd screen
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


def goto_hof():
    press('h')
    sleep(0.5)


def sc_items(coords: Dict[str, Tuple[int, int]]):
    return {item: pg.screenshot(region=(*xy, *ITEM_SIZE)) for item, xy in coords.items()}


def eval_cur_items() -> int:
    old = sc_items(ITEM_COORDS)
    sleep()
    new = sc_items(ITEM_COORDS)

    # for now I only care about the item count, but in later versions one may also want to be able to figure out
    # which items are unowned still
    def comp_ims(im1, im2, item):
        im1.show()
        im2.show()
        if list(im1.getdata()) != list(im2.getdata()):
            # print(f"diff in {item}. Opening both pictures now...")
            # im1.show()
            # im2.show()
            # input("press enter to continue")
            return True

        return False

    return sum(comp_ims(old_im, new[item], item) for item, old_im in old.items())


def find_scrapbook(start=15000, exact=False, alert=1, direction=None, auto_attack=False):
    """Main event loop.
    :param start: leaderboard position to start the search at
    :param exact: Weather the exact start value should be used, otherwise it's randomized around the start value
    :param alert: minimum amount of uncollected items for the script to trigger
    :param direction: 'up' if you want to go upwards in the HoF, 'down' for downwards, 'None' for random direction
    :param auto_attack: False => script stops when it spots a matching player, True => script automatically attacks and
                continues its search"""

    print("starting search in 5 seconds...")
    sleep(5)
    # start_time = time.time()

    if not exact:
        start += random.randint(-start // 2, start // 2)

    if direction is None or direction not in ('up', 'down'):
        direction = 'up' if random.randint(0, 1) else 'down'

    goto_hof()
    sleep()
    click(*SEARCH_FIELD, clicks=1)
    for c in str(start):
        pg.press(c)

    pg.press("enter")

    attempts = 0

    while True:
        attempts += 1
        sleep(0.6)
        diffs: int = eval_cur_items()
        print(f"{attempts:4d}: {diffs = }")
        if diffs >= alert:
            if not auto_attack:
                print("!FOUND SOMEONE!")
                break
            else:
                pg.press('num9')  # num 9 is attack
                sleep(0.1)
                pg.press('enter')
                sleep()
                pg.press('enter')

        pg.press(direction)

    # print(f"Evaluated {attempts} players over {time.time() - start_time:.1f} seconds to find a match.")


def max_effective_luck(level: int) -> int:
    # 50 = luck * 5 / (level * 2)
    # luck * 5 = 50 * (level * 2)
    # luck = 50 * (level * 2) / 5
    luck_required = 50 * (level * 2) / 5
    return math.ceil(luck_required)


def max_effective_luck_range(start: int, stop: int, increment: int = 1):
    for level in range(start, stop, increment):
        print(f"{level}: {max_effective_luck(level)}")


def find_colours():
    im = Image.open("452_haupt.jpg")
    pix_vals = list(im.getdata())
    pix_val_flat = {x for sets in pix_vals for x in sets}
    print(len(pix_val_flat))
