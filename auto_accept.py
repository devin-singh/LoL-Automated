import pyautogui
from python_imagesearch.imagesearch import imagesearch_loop, imagesearch
import time
import main

pyautogui.FAILSAFE = False
TIMELAPSE = 1
ticks = 0

acceptButtonImg = './Resources/sample.png'
acceptedButtonImg = './Resources/sample-accepted.png'
championSelectionImg_flash = './Resources/flash-icon.png'
championSelectionImg_emote = './Resources/emote-icon.png'
playButtonImg = './Resources/play-button.png'
find_button = './Resources/find_button.png'

def checkGameAvailableLoop():
    while True:
        pos = imagesearch(acceptButtonImg, 0.8)
        if not pos[0] == -1:
            pyautogui.click(pos[0], pos[1])
            print("Game accepted!")
            break
        can = imagesearch(find_button, 0.8)
        if not can[0] == -1:
            print("Queue ended!")
            main.main()
            break

        time.sleep(TIMELAPSE)


def checkChampionSelection():
    flash = imagesearch(championSelectionImg_flash)
    emote = imagesearch(championSelectionImg_emote)

    if not emote[0] == -1 or not flash[0] == -1:
        return True
    else:
        return False

def checkGameCancelled():
    accepted = imagesearch(acceptedButtonImg)
    play = imagesearch(playButtonImg)

    if accepted[0] == -1 and not play[0] == -1:
        return True
    else:
        return False


def main():
    global ticks
    run = True

    while run is True:
        ticks += 1
        checkGameAvailableLoop()
        time.sleep(TIMELAPSE)
        if ticks >= 2000:
            main.main()
        while True:
            cancelled = checkGameCancelled()
            if cancelled is True:
                print("Game has been cancelled, waiting...")
                break

            csResult = checkChampionSelection()

            if csResult is True:
                print("Champion selection!")
                time.sleep(TIMELAPSE)
                run = False
                break

            time.sleep(TIMELAPSE)


if __name__ == '__main__':
    print("Running...")
    main()
