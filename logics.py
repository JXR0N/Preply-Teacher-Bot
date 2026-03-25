# ================= IMPORTS =================
import random, os
import win32con, win32api
import pyautogui
from win32con import MOUSEEVENTF_WHEEL
from google.genai import types
from pyautogui import ImageNotFoundException
from pathlib import Path
from time import sleep
from .configs import *
from .coords import *
from .prompt import *



def save_completed_chats(savecompletions):
    """saves amount of completed chats in txt"""
    path = os.path.join('chatlogs', "completed_chat_count.txt")
    if not os.path.exists(path):
        with open(path, "x", encoding="utf-8") as f:
            f.write(f"{savecompletions} Beantwortete Chats")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n{savecompletions} Beantwortete Chats")



def chatlogs_dir():
    """creates 'chatlogs' directory"""
    Path('chatlogs').mkdir(exist_ok=True)
    wait(1)
    logger.info("chatlogs directory available")



def wait(num):
    """sleep to wait just because"""
    sleep(num)



def click(x, y):
    """simulates user clicks"""
    x += random.randint(-2, 2)
    y += random.randint(-2, 2)

    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    wait(random.uniform(0.02, 0.08))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)



def format_data(data):
    """formats chathistory for better readability"""
    raw_output = []
    for line in data:
        for item in line:
            raw_output.append(item)
    return "\n".join(raw_output)



def get_student_name(xcoord, ycoord):
    """extracts studentname (might not be necessary)"""
    studentnameimg = pyautogui.screenshot(region=(100, xcoord - 40, ycoord - 250, 25))
    output = pytesseract.image_to_string(studentnameimg)
    return output.split(" ", 1)[0].strip().replace("\n", "").replace("\r", "")



def get_message_id():
    """extracts message id"""
    message_id_img = pyautogui.screenshot(region=MESSAGE_ID_REGION)
    message_id = pytesseract.image_to_string(message_id_img)
    return message_id.strip("\n")






def get_message_history():
    """extracts whole chathistory"""
    textlist = []
    attempts = 0
    max_attempts = 50
    while attempts < max_attempts:
        wait(1)
        chatimg = pyautogui.screenshot(region=CHAT_DISPLAY_REGION)

        x = pytesseract.image_to_string(chatimg)
        lines = x.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        if textlist and lines == textlist[-1]:
            break
        textlist.append(lines)
        win32api.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, 500, 0)
        attempts += 1
    return format_data(reversed(textlist))






def get_ai_response(user_text, studentname, client):
    # formats chat history again with ai
    format_chat_ai = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=f"{format_chat_role}"),
        contents=user_text)

    # sends chat to ai, which replies with an answer
    response_to_student = client.models.generate_content(
        model="gemini-2.5-pro",
        config=types.GenerateContentConfig(
            system_instruction=f"{teacher_role}"),
        contents=f"Studentname: {studentname}, Chatlog:\n{format_chat_ai.text}")

    return response_to_student.text, format_chat_ai.text






def save_chat_log(message_id, format_chat_ai):
    """saves chat history in a txt file"""
    path = os.path.join('chatlogs', f"{message_id}.txt")
    file = f"{message_id}.txt"
    if file not in os.listdir('chatlogs'):
        with open(path, "x", encoding="utf-8") as f:
            f.write(f"{format_chat_ai}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{format_chat_ai}")






def write_message(response_to_student):
    """ writes message"""
    for s in response_to_student.replace("\n", " "):
        keyboard.type(s)
        wait(random.uniform(0.05, 0.1))
    keyboard.type("\n")






def handle_message(client):
    """handles whole message logic"""
    locatemsg = pyautogui.locateOnScreen(
                'img9.png',
                grayscale=True,
                confidence=0.8,
                region=NOTIFICATION_REGION)
    # sets x and y coordinates for new notification
    x, y = pyautogui.center(locatemsg)
    x1 = int(x)
    y1 = int(y)
    x2 = random.randint(50, 150)

    studentname = get_student_name(x1, y1)

    # click and wait block
    wait(2)
    click(*CHAT_ICON)  # clicks on chat icon top right corner
    wait(3)
    click(x1 - x2, y1)  # clicks on student chat
    wait(5)


    message_id = get_message_id() # extracts message id
    user_text = get_message_history() # extracts chathistory
    response_to_student, format_chat_ai = get_ai_response(user_text, studentname, client) #get ai reply
    save_chat_log(message_id, format_chat_ai) # saves chathistory as txt
    click(*TEXT_FIELD) # clicks on textfield
    write_message(response_to_student) # writes message to student


    # click and wait block
    wait(3)
    click(*CHAT_ICON)  # clicks on chat icon top right corner
    wait(3)






def main_loop(client):
    """checks for new messages and starts message handling"""
    completed_chats = savecompletions = 0
    scrolls_done = 0
    max_scrolls = 5
    while True:
        try:
            while True:
                handle_message(client)
                completed_chats += 1

                if completed_chats > 0 and completed_chats % 5 == 0 and scrolls_done != max_scrolls:
                    # if no chat has been found, it will scroll
                    wait(1)
                    win32api.SetCursorPos((470, 470))
                    wait(1)

                    # -660 pixels will be scrolled down
                    win32api.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, -660, 0)
                    wait(1)
                    scrolls_done += 1
        except ImageNotFoundException:

            wait(1)
            logger.info(f"no new chat has been found")
            scrolls_done = 0


            savecompletions += completed_chats
            if savecompletions > 0:
                save_completed_chats(savecompletions) # saves completed chat count to txt file
            completed_chats = 0

            # site will reload after 10 - 20 minutes
            wait(1)
            wait_time = random.randint(600, 1200)
            logger.info(f"reloads site in {wait_time / 60:.1f} minutes")
            wait(wait_time)
            click(*RELOAD_SITE)
            wait(10)