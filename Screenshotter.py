import os
import time
import pyautogui
from PIL import Image
import pytesseract, re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


region = (0, 150, 365, 150+35)
def getScreenshot():
	screenshot = pyautogui.screenshot()
	positionImage = screenshot.crop(region)

	text = OCR(positionImage)

	cas = time.strftime("%Y-%m-%d %H-%M-%S");
	# if dir exists
	os.makedirs("POI", exist_ok=True)
	filename = "POI\\" + str(cas) +" " + text + ".png";
	screenshot.save(filename)
	return (filename, text, cas)

def getCoor():
	# screenshot = takeScreenshot()
	screenshot = pyautogui.screenshot(region=region)
	text = OCR(screenshot)
	return text.strip()

def OCR(image):
	text = pytesseract.image_to_string(image, lang="mc")
	try:
		text = re.search(r"([\-0-9 ]+,[\-0-9 ]+,[\-0-9 ]+)", text).group(0)
	except AttributeError:
		text = "no coor"
	return text

def takeScreenshot():
	screenshot = pyautogui.screenshot()	
	return screenshot

if __name__ == "__main__":
	print(getScreenshot())
	# print(time.strftime("%Y-%m-%d %H:%M:%S"))
	# sc = takeScreenshot()
	# sc.save("screenshot.png")
	# print("Took screenshot and saved as screenshot.png")