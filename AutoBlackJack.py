import pyautogui
from PIL import Image
import pytesseract
import time
import io
import pyperclip
import win32clipboard  # For Windows - requires 'pywin32' package

# Set the path to Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Remot\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Function to capture the entire screen
def capture_full_screen():
    return pyautogui.screenshot()

# Function to extract the rightmost window (blackjack screen) based on screen size
def extract_blackjack_screen(full_screenshot):
    screen_width, screen_height = pyautogui.size()
    
    # Assume blackjack window is on the right, taking ~25% of the screen width from the right
    blackjack_left = int(screen_width * 0.75)  # Start 75% from left (right 25%)
    blackjack_width = int(screen_width * 0.25)  # Width of 25%
    blackjack_height = int(screen_height * 0.9)  # Height covering most of the screen (adjust as needed)
    
    bounding_box = (blackjack_left, 0, blackjack_left + blackjack_width, blackjack_height)
    return full_screenshot.crop(bounding_box)

# Function to clear the screen output (simulated via typing)
def clear_screen_output():
    pyautogui.hotkey('ctrl', 'a')  # Select all
    pyautogui.press('backspace')   # Clear
    time.sleep(0.5)  # Brief pause to ensure clear

# Function to copy a PIL Image to the clipboard using pyperclip
def copy_image_to_clipboard(pil_image):
    """
    Copies a PIL Image to the system clipboard (Windows-specific implementation)
    """
    try:
        # Convert PIL Image to BMP format (required for Windows clipboard)
        output = io.BytesIO()
        # Convert to RGB if image has alpha channel
        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')
        pil_image.save(output, format="BMP")
        data = output.getvalue()[14:]  # Skip BMP header (first 14 bytes)
        output.close()

        # Copy to Windows clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        print("Image successfully copied to clipboard.")
        
    except Exception as e:
        print(f"Error copying image to clipboard: {str(e)}")

# Function to enter Grok prompt and paste blackjack screenshot
def get_grok_command(blackjack_image):
    # Move to Grok window (updated left side, based on 1919x1079 resolution, lower position)
    pyautogui.moveTo(300, 940)  # Adjusted to lower position for Grok chat input (left side, centered lower)
    pyautogui.click()
    time.sleep(0.5)
    
    # Copy the blackjack screenshot (PIL Image) to clipboard
    copy_image_to_clipboard(blackjack_image)
    
    # Paste the blackjack screenshot (now using the copied image)
    pyautogui.hotkey('ctrl', 'v', interval=0.1)  # Paste the image from clipboard
    time.sleep(1)  # Wait for Grok to respond (adjust timing as needed)
    pyautogui.press('enter')  # Submit the image (adjust if Grok requires different input)
    time.sleep(5)  # Wait for Grok to respond (adjust timing as needed)
    
    # Clear any existing output
    clear_screen_output()
    
    # Enter the prompt
    prompt = "use the last screenshot, using blackjack standard rules output a single command, one of the following {hit, stand, split, double, play}. Output only this command after clearing the whole screen output prior.If the green play button is available, always response play, otherwise use standard blackjack rules for the other actions."
    pyautogui.typewrite(prompt)
    time.sleep(2)  # Wait for prompt to register
    pyautogui.press('enter')
    time.sleep(5)  # Wait for prompt to register
    
    return capture_grok_output()

# Function to capture and OCR the Grok output from the left side, saving as lastGrokResponse.jpg
def capture_grok_output():
    screen = pyautogui.screenshot()
    screen_width, screen_height = pyautogui.size()
    
    # Bounding box for Grok output (left side, approximate 25% of screen width, updated for 1919x1079)
    grok_left = 0
    grok_width = int(screen_width * 0.1)  # 47.9 pixels
    grok_height = int(screen_height * 0.8)  # ~971 pixels
    
    grok_bounding_box = (grok_left, 300, grok_left + grok_width, grok_height)
    grok_screenshot = screen.crop(grok_bounding_box)
    
    # Save the Grok screenshot
    grok_screenshot.save('lastGrokResponse.jpg')
    
    # Convert to grayscale and perform OCR
    image = grok_screenshot.convert('L')
    text = pytesseract.image_to_string(image)
    
    # Process text to remove extra whitespace and empty lines
    text = ' '.join(text.split()).strip().lower()
    print("Grok OCR output:", text)
    return text

# Resilient function to interpret OCR string and match to blackjack commands
def interpret_blackjack_command(ocr_text):
    valid_commands = {"hit", "stand", "split", "double", "play"}
    
    # Clean and normalize the OCR text
    cleaned_text = ocr_text.strip().lower()
    
    # Check for the most likely command using fuzzy matching (simple substring check)
    best_match = None
    highest_similarity = 0
    
    for command in valid_commands:
        if command in cleaned_text:
            # Simple scoring: exact match gets 1.0, partial match gets 0.5
            similarity = 1.0 if cleaned_text == command else 0.5 if command in cleaned_text else 0
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = command
    
    if best_match:
        print(f"Interpreted command: {best_match}")
        return best_match
    print("No valid command recognized.")
    return None

# Function to click blackjack buttons based on command, saving blackjack screenshot as lastBlackJack.jpg
def click_blackjack_button(command):
    button_locations = {
        "hit": (1573, 489),    # Updated "Hit" button (right side, based on 1919x1079)
        "stand": (1767, 489),  # Updated "Stand" button
        "split": (1573, 548),  # Updated "Split" button
        "double": (1767, 548), # Updated "Double" button
        "play": (1750, 700)    # Updated "Play" button
    }
    
    if command in button_locations:
        x, y = button_locations[command]
        pyautogui.click(x=x, y=y)
        print(f"Clicked {command} button at ({x}, {y})")
    else:
        print(f"No action for command: {command}")

def main_loop():
    while True:
        # User input to continue or stop
        #user_input = input("Do you want to stop? (enter to continue): ").lower().strip()
        #if user_input != '':
        #    print("Exiting LLMFiniteBattle.")
        #    break
        
        print("Starting iteration...")
        
        # Step 1: Capture the full screen and extract the blackjack window
        full_screen = capture_full_screen()
        blackjack_screenshot = extract_blackjack_screen(full_screen)
        
        # Step 2: Save the blackjack screenshot (optional, for debugging or reference)
        blackjack_screenshot.save('lastBlackJack.jpg')
        
        # Step 3: Enter Grok prompt and paste blackjack screenshot
        grok_response = get_grok_command(blackjack_screenshot)
        
        # Step 5: Capture and OCR Grok output from left side
        ocr_text = capture_grok_output()
        
        # Step 6: Interpret OCR text as blackjack command
        blackjack_command = interpret_blackjack_command(ocr_text)
        
        # Step 7: Click corresponding button on blackjack screen
        if blackjack_command:
            click_blackjack_button(blackjack_command)
        
        # Step 8: Add delay before next iteration
        time.sleep(5)  # Adjust delay as needed

if __name__ == "__main__":
    main_loop()