import os, re, time, keyboard, threading
import customtkinter as ctk
from playsound import playsound
from PIL import Image, ImageTk

from Screenshotter import getCoor, getScreenshot

# Create the main window
app = ctk.CTk()
app.geometry("900x800")
app.title("POI and LOG Viewer")
app.after(201, lambda :app.iconbitmap('icon.ico'))

app.grid_columnconfigure(0, weight=3)
# app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

app.configure(fg_color="black")
title_color = "#d4cfc9"
title_bg_color = "#222d42"
# boldFont = ("AntykwaTorunska", 19,"bold")
boldFont = ("Minecraft", 18,"bold")


# Set up two main frames: one for "POI" and one for "LOG"
poi_frame = ctk.CTkScrollableFrame(app, corner_radius=0, label_text="POIs",
									label_font=boldFont, label_text_color=title_color, label_fg_color=title_bg_color)
poi_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
poi_frame.grid_columnconfigure(0, weight=1)



logs_frame = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color="transparent")
logs_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
logs_frame.grid_rowconfigure(0, weight=5)
logs_frame.grid_rowconfigure(1, weight=1)

log_frame = ctk.CTkScrollableFrame(logs_frame, width=200, corner_radius=0, label_text="log",
									label_font=boldFont, label_text_color=title_color, label_fg_color=title_bg_color)
log_frame.grid(row=0, column=0, sticky="nsew",pady=(0,10))

jumps_frame = ctk.CTkScrollableFrame(logs_frame, width=200, corner_radius=0, border_color="blue", border_width=0, label_text="Jumps",
									label_font=boldFont, label_text_color=title_color, label_fg_color=title_bg_color)
jumps_frame.grid(row=1, column=0, sticky="nsew")

# button = ctk.CTkButton(app, text="TEST", fg_color="blue", bg_color="white", font=("Minecraft", 15))
# button.grid(row=1,column=0,pady=5)
# button.bind("<Button-1>", lambda e: add_poi("screenshot.png", f"-15, 20, 2\n2024-09-30 2:24"))
# button.bind("<Button-1>", lambda e: add_log_entry("10, 5, -15"))


toggle_var = ctk.BooleanVar(value=False)
toogle = ctk.CTkCheckBox(app, text="Work?", fg_color="#519f50", font=("Minecraft", 15),
						 variable=toggle_var, onvalue=True, offvalue=False)
toogle.grid(row=1,column=0,columnspan=2,pady=(5,10))

# Function to add POI (image and text)
numperOfPOI = 0
def add_poi_entry(image_path, coor, date,scroll=True):
	global numperOfPOI
	global poi_frame

	img = Image.open(image_path)
	img = img.resize((256, 144))
	my_image = ctk.CTkImage(img,size=(256,144))
	img_tk = ImageTk.PhotoImage(img)
	
	poi = ctk.CTkFrame(poi_frame, corner_radius=3, height=300, border_color="#5a647e", border_width=2)
	poi.grid(row=numperOfPOI, column=0, padx=5, pady=5, sticky="nsew")
	numperOfPOI += 1
	# poi.columnconfigure(0, width=100)
	poi.columnconfigure(1, weight=1)


	poiImage = ctk.CTkLabel(poi, text="", fg_color="red", image=my_image, width=256, anchor=ctk.W)
	poiImage.grid(row=0,column=0,padx = 10, pady = 10)


	labels = ctk.CTkFrame(poi,fg_color="transparent")
	labels.grid(row=0,column=1,padx = 5, pady = 5)

	poiTextCoor = ctk.CTkLabel(labels,text_color="white", fg_color = "transparent", text=coor, font= ("Minecraft", 30))
	poiTextCoor.grid(row=0,column=0,padx = 5,pady=5)
	poiTextTime = ctk.CTkLabel(labels,fg_color="transparent", text=date, font= ("Mensch", 15))
	poiTextTime.grid(row=1,column=0,padx = 5)
	
	if scroll:
		poi_frame._parent_canvas.yview_moveto(1.0)



# lastLog = None
def add_log_entry(entry):	
	# global lastLog
	log_entry = ctk.CTkLabel(log_frame, text=entry, font=("Minecraft",10))
	# if(lastLog == None):
	# 	log_entry.pack(pady=0)
	# else:
	# 	log_entry.pack(pady=0, before=lastLog)
	# lastLog = log_entry
	log_entry.pack(pady=0)
	log_frame._parent_canvas.yview_moveto(1.0)


def add_jump_entry(entry):
	jump_entry = ctk.CTkLabel(jumps_frame, text=entry, font=("Minecraft",12,"bold"))
	jump_entry.pack(pady=0)
	jumps_frame._parent_canvas.yview_moveto(1.0)



# Function to periodically fetch data
last_coors = None
def fetch_data():
	time.sleep(1)
	poi_frame._parent_canvas.yview_moveto(1.0)
	time.sleep(4)
	global last_coors
	while True:
		if(toggle_var.get()):
			coor = getCoor()
			if(coor != "no coor"):
				coors = coor.split(",")
				try:
					x = int(coors[0].strip())
					y = int(coors[1].strip())
					z = int(coors[2].strip())
					cas = time.strftime("%Y-%m-%d %H:%M:%S");
					save_data(f"{cas}: {x}, {y}, {z}")
					add_log_entry(f"{x}, {y}, {z}")

					if last_coors is not None:
						xprev, yprev, zprev = last_coors
						if (x-xprev)**2 + (y-yprev)**2 + (z-zprev)**2 > 50**2:
							add_jump_entry(f"{xprev}, {yprev}, {zprev}")
					last_coors = (x, y, z)
				except ValueError:
					add_log_entry("no coor - ocr problem")

			else:
				add_log_entry("no coor")
		time.sleep(5)

# Function to save data to a file
def save_data(text):
	with open("log.txt", "a") as f:
		f.write(f"{text}\n")

def addNewPOI():
	image, coor, time  = getScreenshot()
	add_poi_entry(image, coor, time)

def listen_for_key():
	# This will listen for the numpad 5 key press globally
	while True:
		keyboard.wait('num 5')
		if(toggle_var.get()):
			sound_thread = threading.Thread(target=lambda:playsound('click.wav'))
			sound_thread.start()
			addNewPOI()


# Start the background thread to fetch data
thread = threading.Thread(target=fetch_data, daemon=True)
thread.start()

# Start the global key listener thread
key_listener_thread = threading.Thread(target=listen_for_key, daemon=True)
key_listener_thread.start()



# loads all files from folder 
def loadPOIs():
	os.makedirs("POI", exist_ok=True)
	for filename in os.listdir("POI"):
		if filename.endswith(".png"):
			try:
				res = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}) ([\-0-9 ]+,[\-0-9 ]+,[\-0-9 ]+)", filename)
				time = res.group(1)
				coor = res.group(2)
			except AttributeError:
				time = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})", filename).group(0)
				coor = "no coor"
			timeArray = list(time)
			timeArray[13] = ":"
			timeArray[16] = ":"			
			time = "".join(timeArray);
			add_poi_entry(f"POI\\{filename}", coor, time,scroll=False)
	
loadPOIs()
# Start the application loop
app.mainloop()
