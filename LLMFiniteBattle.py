import pyautogui
from PIL import Image
import pytesseract
import time

# Set the path to Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Remot\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def capture_and_ocr(bounding_box=None):
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    
    # If a bounding box is provided, crop the screenshot to that region
    if bounding_box:
        screenshot = screenshot.crop(bounding_box)
    
    # Convert to grayscale for better OCR
    image = screenshot.convert('L')
    
    # Perform OCR only on the (possibly cropped) image
    text = pytesseract.image_to_string(image)
    
    # Process the text to remove the first two lines
    lines = text.split('\n')
    if len(lines) > 2:
        text = '\n'.join(lines[2:])
    else:
        text = ''  # In case there's only one or two lines or no content after the first two lines

    text = ' '.join(text.split())

    # Print the recognized text
    print(text)
    
    return text

if __name__ == "__main__":
    # Define the actions for each side in an array
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

    # Number of iterations
    N = 100  # You can change this to any number of iterations you want
    
    # Loop over the actions N times, switching each iteration
    for i in range(N):
        for j, action in enumerate(actions):
            # Determine the index of the other action
            other_action_index = (j + 1) % len(actions)
            
            print(f"Iteration {i+1}, Processing {action['side']} side:")
            
            # Perform OCR on the specified bounding box
            partial_text = capture_and_ocr(bounding_box=action['bounding_box'])
            
            # Give some time for the user to switch to the desired application or field
            time.sleep(max(3,min(i+1,30)))

            # Click using the click location of the opposite action
            click_x, click_y = actions[other_action_index]['click_location']
            pyautogui.click(x=click_x, y=click_y)

            time.sleep(1)

            # Enter the recognized text into the keyboard
            if partial_text:
                pyautogui.typewrite(partial_text)
            
            time.sleep(max(3,min(i+1,30)))
            pyautogui.typewrite("\n")
            
            print(f"Finished processing {action['side']} side.\n")