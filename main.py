import pynput
import pyautogui
from PIL import Image
import pytesseract
import time
import auto_accept
import subprocess
import yuumi_script


search_x = 0
search_y = 0
tick = 0

champion = "Ahri"

find_button = "./Resources/find_button.png"
confirm_button = "./Resources/confirm_button.png"
search_bar = "./Resources/search.png"
lock_button = "./Resources/lock_button.png"
top_offset = "./Resources/top_offset.png"
continue_button = "./Resources/continue_button.png"
play_again_btn = "./Resources/play_again.png"
pfp_btn = "./Resources/pfp.png"
lock_wait = "./Resources/lock_wait.png"
ok_button = "./Resources/ok_button.png"

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

#####################################################
############ Pick champion ##########################
#####################################################

def lock_in():
    global tick
    try:
        x, y = pyautogui.locateCenterOnScreen(lock_button, confidence = 0.9)
        pyautogui.click(x, y)
        print("Attempt to lock in champ...")
        time.sleep(1)
        is_locked()
    except:
        print("Couldn't find lock in button...Trying again...")
        time.sleep(1)
        tick += 1
        if tick > 100:
            tick = 0
            main()
        lock_in()

def click_champ():
    global tick
    try:
        x, y = pyautogui.locateCenterOnScreen(top_offset, confidence=0.9)
        pyautogui.click(x+30, y+83)
        pyautogui.click(x+30, y+83)
        pyautogui.click(x+30, y+83)
        print("Clicked champ, locking in!")
        time.sleep(3)
        lock_in()
    except:
        print("Can't find top_off. Trying Again...")
        tick += 1
        if tick > 100:
            tick = 0
            main()
        time.sleep(1)
        click_champ()

def lock(champion):
    global search_x
    global search_y
    global tick
    try:
        if search_x == 0 and search_y == 0:
            x, y = pyautogui.locateCenterOnScreen(search_bar, confidence=0.9)
            search_x = x
            search_y = y
        pyautogui.click(search_x, search_y)
        with pyautogui.hold('ctrl'):
            pyautogui.press('backspace')
        pyautogui.write(champion)
        print("Wrote Champion..")
        click_champ()
    except:
        print("Can't find search_bar. Trying again in 1 seconds...")
        time.sleep(1)
        tick += 1
        if tick > 100:
            tick = 0
            main()
        lock(champion)

#####################################################
############ Queue Match Up #########################
#####################################################

def get_lobby():
    try:
        x, y = pyautogui.locateCenterOnScreen(find_button, confidence=0.9)
        print("Started Queue!")
        pyautogui.click(x, y)
        pyautogui.move(0, -150)
        auto_accept.main()
        time.sleep(10)
    except:
        print("Can't find begin match button.. I'll try to press continue... ")
        click_continue_button()

def click_play_again():
    global tick
    try:
        x, y = pyautogui.locateCenterOnScreen(play_again_btn, confidence=0.9)
        pyautogui.click(x, y)
        pyautogui.move(0, -150)
        print("Clicked Play Again!")
        get_lobby()
    except:
        print("Can't find play again button, Trying again!")
        time.sleep(1)
        tick += 1
        if tick > 100:
            tick = 0
            main()
        click_play_again()

def click_ok():
    try:
        x, y = pyautogui.locateCenterOnScreen(ok_button, confidence=0.9)
        pyautogui.click(x, y)
        pyautogui.move(0, -150)
        print("Pressed Ok!")
        click_continue_button()
    except:
        print("Ok not found...")
        get_lobby()

def click_continue_button():
    try:
        x, y = pyautogui.locateCenterOnScreen(continue_button, confidence=0.9)
        pyautogui.click(x, y)
        pyautogui.move(0, -150)
        print("Pressed continue!")
        click_play_again()
    except:
        print("Can't find continue... Trying to start match")
        time.sleep(1)
        click_ok()

#####################################################
############ Verification Functions##################
#####################################################

def raw_check_dodge():
    try:
        x, y = pyautogui.locateCenterOnScreen(pfp_btn, confidence=0.9)
        print("Dodge detected! Starting AA script again.")
        auto_accept.main()
    except:
        print("No dodge detected...")

def check_dodge():
    try:
        x, y = pyautogui.locateCenterOnScreen(pfp_btn, confidence=0.9)
        print("Dodge detected! Starting AA script again.")
        auto_accept.main()
        wait_for_lock()
    except:
        print("No dodge detected. Waiting...")
        wait_for_lock()

def wait_for_lock():
    try:
        x, y = pyautogui.locateCenterOnScreen(lock_wait, confidence=0.9)
        print("Detected lock button.")
    except:
        time.sleep(1)
        check_dodge()

def is_locked():
    global champ_index
    global champion
    try:
        x, y = pyautogui.locateCenterOnScreen(lock_wait, confidence=0.9)
        print("Lock in failed, trying again..")
        champion = "Annie"
        lock(champion)
    except:
        print("Successfully locked in " + champion +"!")


#####################################################
############ Main Logic #############################
#####################################################

def start_game():
    click_continue_button()
    # Queue started at this point
    wait_for_lock()
    lock(champion)
    time.sleep(1)
    # Champ locked with no dodge, dodge still possible
    while process_exists("League of Legends.exe") is False:
        raw_check_dodge()
        time.sleep(3)
    # Game 100% Started!
    tick = 0

def main():
    tick = 0
    while True:
        time.sleep(2)
        if not process_exists("League of Legends.exe"):
            start_game()
        # TODO: MAKE Sure Game Is Open!
        if process_exists("League of Legends.exe"):
            yuumi_script.main() # TODO: Replace this with py file that handles afk behaviors


if __name__ == '__main__':
    print("Running...")
    main()
