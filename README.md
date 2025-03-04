# AutoBlackJack
Repo sets up LLM with copy paste image support on left side, and stake.us on right side. It asks the best response, uses OCR, associates that response with an action and performs the action on the right.

# FiniteLLMBattle
This repository is thrown together quickly with grok. It pits two chats against eachother, uses OCR currently for response interpretation, uses pyautogui for mouse click and text input.

# requirements
- OCR done with tesseract https://github.com/tesseract-ocr/tesseract
- pip install pytesseract pyautogui

# Tesseract application installation
replace LLMFiniteBattle.py:
	pytesseract.pytesseract.tesseract_cmd = r'abs\path\to\Tesseract-OCR\tesseract.exe'
	
# Usage

# first configure your screen with the bounding 
1. Screenshot whole screen with both chat windows open
2. Edit in paint
3. Rectangle selection tool shows the current cursor position on the bottom left of the paint window.
--Record this for each corner of the chat windows.
--Record the location of the input (enter is used for sending text)
4. set actions in LLMFiniteBattle.py, currently they are defined 
actions = [
        {
            "side": "left",
            "bounding_box": (147, 134, 640, 744),  # Example bounding box for the left side (left, top, right, bottom)
            "click_location": (156, 963),
            "sleep_time": 5
        },
        {
            "side": "right",
            "bounding_box": (1300, 134, 1800, 744),  # Example bounding box for the right side (left, top, right, bottom)
            "click_location": (1343, 970),
            "sleep_time": 5
        }
    ]
	
5. Set the number of iterations N in the main section.

call python LLMFiniteBattle.py

# todo items
-add point and click for OCR
-add command line argumnets for N, bounding boxes, click_locations, etc.
-split out sleep_times based on which stage
-get better indication that response is done
-add detection for out of credits
-use this with pc
-integrate with LLM to modify certain part of browser
-add ability to copy screenshots (really a subselection of current whole screen screenshot)
-interact with python browser emulator directly for sending and receiving input
--eliminates pyautogui altogether
