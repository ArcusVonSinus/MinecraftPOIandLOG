# MinecraftPOIandLOG
 Logs position and saves POIs

### Requirements:
- You need show the coordinates in bedrock Minecraft
	- Go to settings
	- Go to video
	- Go to HUD
	- Turn on "Show Coordinates"
- You should have a minecraft font, see https://fontmeme.com/fonts/minecraft-font/
- It needs resolution of 2560x1440
- Minecraft GUI scale modifier should be -2
- You need teseract for ocr installed
	- https://github.com/tesseract-ocr/tesseract/releases/tag/5.4.1
	- Together with the minecraft font training data from here: https://hayden.gg/blog/minecraft-ocr-with-pytesseract/ 
- Some python packages

### Usage:
- After running it loads previous POIs from the folder POI.
- If you toggle the "Work?" button it will log the position every 5 seconds.
	- The position is appended to the file `log.txt`.
	- If the position is far from previous one (most significantly if you die) it will display the last position in the Jumps list.
	- If you press the **numpad 5** key it will add another POI (it will take the screenshot and save the coordinates)

### ToDo:
- Remove old log entries, when there are too many of those it will get stuck (but the coors are sill saved to log.txt)
