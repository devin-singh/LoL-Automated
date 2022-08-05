import pyautogui
import time
import subprocess
import main
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import win32api, win32con
import random




keyboard = Controller()

team_lock = 'f1'
center_x = 0
center_y = 0

shop_bar_x = 0
shop_bar_y = 0

gold = 50
gps = 4.5
t0 = 0
ctime = 0


starter_item = "Spectral"

f_keys=[Key.f2, Key.f3, Key.f4, Key.f5]

items=["Moonstone", "Kindle", "Ruby", "Fae", "Ampli", "Band"]
item_index = 0
level_up = "./Resources/level_up.png"
death_pic = "./Resources/death.png"
hp_bar = "./Resources/hp_bar.png"
base = "./Resources/base.png"
shop_bar = "./Resources/shop_bar.png"


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print('Left Click')

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    print('Left Click')

def click(Key):
    keyboard.press(Key)
    keyboard.release(Key)

def use_q():
    #TODO: Move cursor to center of window
    click('q')

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

def update_center_coords():
    global center_x
    global center_y
    try:
        x, y = pyautogui.locateCenterOnScreen(hp_bar, confidence=0.7)
        center_x = x
        center_y = y + 80
        pyautogui.dragTo(center_x, center_y, 1)
    except:
        print("Can't find hp bar. Trying again...")
        time.sleep(1)
        update_center_coords()

def ff():
    time.sleep(2)
    print("Attempting to ff..")
    click(Key.enter)
    time.sleep(0.4)
    keyboard.type('/ff')
    time.sleep(0.4)
    click(Key.enter)

def try_to_level():
    try:
        x, y = pyautogui.locateCenterOnScreen(level_up, confidence=0.8)
        keyboard.press(Key.ctrl_l)
        click('r')
        click('q')
        click('e')
        click('w')
        keyboard.release(Key.ctrl_l)
        print("Found level up")
    except:
        print("Not ready to level up...")


def w_top_lane():
    global f_keys
    key = random.choice(f_keys)
    keyboard.press(key)
    time.sleep(1)
    pyautogui.dragTo(center_x-200, center_y+100)
    time.sleep(0.4)
    click('w')
    click('w')
    rightClick()
    rightClick()
    time.sleep(0.4)
    keyboard.release(key)

def random_right_click():
    pyautogui.moveTo(center_x+400, center_y-100, 1)
    pyautogui.click(button='right')
    pyautogui.click(button='right')
    print("Random right click activated..")

def update_shop_coords():
    global shop_bar_x
    global shop_bar_y
    try:
        x, y = pyautogui.locateCenterOnScreen(shop_bar, confidence=0.8)
        shop_bar_x = x
        shop_bar_y = y
    except:
        print("Can't find shop bar. Trying again...")
        time.sleep(1)
        update_shop_coords()

def buy_items():
    global shop_bar_x
    global shop_bar_y
    global items
    global item_index
    while item_index < len(items):
        pyautogui.dragTo(shop_bar_x, shop_bar_y, 1)
        time.sleep(1)
        leftClick()
        leftClick()
        keyboard.press(Key.backspace)
        time.sleep(2)
        keyboard.release(Key.backspace)
        keyboard.type(items[item_index])
        time.sleep(1)
        click(Key.enter)

        item_index+=1
        print("Tried to buy an item.")
    item_index = 0
    click(Key.esc)

def attempt_to_buy(item):
    global items
    global item_index

    try:
        x, y = pyautogui.locateCenterOnScreen(death_pic, confidence=0.8)
        time.sleep(0.3)
        click('p')
        time.sleep(0.3)
        print("Opened shop...")
        update_shop_coords()
        buy_items()
        click('p')
    except:
        print("Not dead...")

def main():
    global t0
    time.sleep(2)
    if process_exists("League of Legends.exe"):
        t0 = time.process_time()
        win = gw.getWindowsWithTitle('League of Legends')[0]
        win.activate()
        time.sleep(1)
        click('y')
        time.sleep(1)
        update_center_coords()
    while process_exists("League of Legends.exe") is True:
        ff()
        try_to_level()
        use_q()
        w_top_lane()
        attempt_to_buy(items[item_index])
        time.sleep(10)

if __name__ == '__main__':
    print("Running yuumi script...")
    main()
