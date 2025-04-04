import os

try:
	from PIL import Image
	import pyautogui
	import matplotlib

except:
	os.system("python3 -m pip install pillow pyautogui, matplotlib")

from PIL import Image
import pyautogui
import matplotlib

import time
import sys


argv = sys.argv

pyautogui.MINIMUM_DURATION = 0

VERSION = "Skin Transferer 1.0 released on 1/25/2025"
DELAY = 0.0
STARTING_DELAY = 2.5

PARTS = ["head", "body", "larm", "rarm", "lleg", "rleg"]
FACES = ["front", "right", "left", "back", "top", "bottom"]
PS3D_OPTI_PARTS = ["head", "body", "rarm", "rleg"]


class Data:

	def __init__(self):
		pass

def _help(context=['']):
	print("Skin Transferer allows you to transfer your Minecraft skin to Pixel Strike 3D.\n")
	print("Here are all the available functions and their description.\n")
	for k in functions.keys():
		print(k+" : " + functions[k][1] + "\n")

def _version(context=['']):
	print(VERSION)

def _exit(context=['']):
	data.running = False

def _open(context=None, auto=False):
	if not context:
		print("Wrong use of the function! - You need to specify the name of the file to open. - Type \"help\" for more.")
		return

	file = context[0]

	try:
		with Image.open(file) as image:
			if image.mode != "RGBA":
				image = image.convert("RGBA")
			data.width, data.height = image.size
			image_data = image.getdata()
			pixels = [[None for i in range(64)] for i in range(64)]
			for x in range(64):
				for y in range(64):
					px = image_data.getpixel((x,y))
					pixels[x][y] = px
			data.pixels = pixels

	except FileNotFoundError:
		print("Wrong use of the function! - File not found!")
		return

	if not auto:
		print("Image opened with success! - You may now select the area to transfer with the \"select\" function.")

def _select(context=None, auto=False):
	if not context:
		print("Wrong use of the function! - You need to specify the mode of the function first! - Type \"help\" for more.")
		return
	elif not data.pixels:
		print("Wrong use of the function! - You need to open an image file as the skin to use first! - Use the \"open\" function.")
		return

	mode = context.pop(0)
	error = False
	if mode == "position":
		v = False
		if len(context) > 3:
			try:
				for i in range(4): context[i] = int(context[i])
			except: error = True
			else:
				x1, y1, x2, y2 = context[0], context[1], context[2], context[3]
				v = True
				
		if not v:
			print("Wrong use of the function! - You need to specify x1 and y1, the top left corner's coordinates and x2 and y2, the bottom right corner's coordinates. - Type \"help\" for more.")
			error = True

	elif mode == "part":
		if context[0] not in partPositions:
			print("Wrong use of the function! - You need to specify the part of the skin you want to use the preset of. - Type \"help\" for more.")
			error = True
		else:
			x1, y1, x2, y2 = partPositions[context[0]]

	else:
		print("Wrong use of the function! - Unknown mode! - Type \"help\" for more.")

	if not error:
		w, h = x2-x1, y2-y1
		selection = [[None for i in range(h)] for i in range(w)]
		for x in range(w):
			for y in range(h):
				selection[x][y] = data.pixels[x1+x][y1+y]
		data.selection = selection
		data.sw, data.sh = w, h

		if not auto:
			print("Area selected with success! - You may now start the transfer with the \"transfer\" function.")

def _store(context=[''], auto=False):
	if not data.selection:
		print("Wrong use of the function! - You need to select an area before. - Type \"help\" for more.")
		return

	if not auto:
		if data.stored:
			ans = input("WARNING! You already have a stored selection! - Do you wish to continue and REPLACE the already stored selection [IRREVERSIBLE] ? [Y/N] ")
			if ans.upper().replace(" ", "") not in ["Y", "YES", "YESSIR"]:
				print("Operation canceled!")
				return

		data.stored = data.selection
		print("Current selection succesfully stored!")

	else:
		data.stored = data.selection

def _restore(context=[''], auto=False):
	if not data.stored:
		print("Wrong use of the function! - You need to store an area before. - Type \"help\" for more.")
		return

	if not auto:
		ans = input("WARNING! You already have a selection! - Do you wish to continue and REPLACE the selection [IRREVERSIBLE] ? [Y/N] ")
		if ans.upper().replace(" ", "") not in ["Y", "YES", "YESSIR"]:
				print("Operation canceled!")
		else:
			data.selection = data.stored
			print("Stored selection succesfully restored!")
	else:
		data.selection = data.stored

def _show(context=['']):
	if context[0] == "stored":
		if not data.stored:
			print("Wrong use of the function! - You cannot display the stored selection if you do not have a selection stored. - Type \"help\" for more.")
			return
		
		print("Showing stored data!")
		print(data.stored)
	elif context[0] == "image":
		if not data.pixels:
			print("Wrong use of the function! - You need to open an image file as the skin to use first! - Use the \"open\" function.")
			return

		print("Showing opened image file!")
		print(data.pixels)
	else:
		if not data.selection:
			print("Wrong use of the function! - You need to select an area before. - Type \"help\" for more.")
			return

		print("Showing selected data!")
		print(data.selection)

def _add_on_top(context=[''], auto=False):
	if not data.stored:
		print("Wrong use of the function! - You need to select an area before. - Type \"help\" for more.")
		return
	elif not data.selection:
		print("Wrong use of the function! - You need to store an area before. - Type \"help\" for more.")
		return
	if (len(data.selection[0]) != len(data.stored[0])) or (len(data.selection[0][0]) != len(data.stored[0][0])):
		print("Wrong use of the function! - Selected and stored areas are not of the same size. - Type \"help\" for more.")
		return

	for i in range(len(data.stored)*len(data.stored[0])):
		selection_pixel_color = data.selection[i%data.sw][i//data.sw]
		stored_pixel_color = data.stored[i%data.sw][i//data.sw]

		if selection_pixel_color[3] == 255:
			data.stored[i%data.sw][i//data.sw] = selection_pixel_color
		else:
			color = blend_colors(stored_pixel_color, selection_pixel_color)
			data.stored[i%data.sw][i//data.sw] = color

	if not auto:
		print("Done! Current selection succesfully added on top of the stored selection.")

def _transfer(context=None, auto=False, starting_delay=STARTING_DELAY):
	if not context:
		print("Wrong use of the function! - You need to specify the preset to use. - Type \"help\" for more.")
		return
	elif context[0] not in buttonPositions[1]:
		print("Wrong use of the function! - Unknown preset. - Type \"help\" for more.")
		return

	pattern = buttonPositions[1][context[0]]
	pw, ph = pattern[1][0], pattern[1][1]
	if not (pw == data.sw and ph == data.sh):
		print("Wrong use of the function! - Preset's size is different than your selection's size. - Type \"help\" for more.")
		return

	if not auto:
		input(f"You will have {starting_delay} seconds to switch to the Pixel Strike 3D window after you hit [ENTER]. Before you do that, make sure that you are in the paint menu of the face that will get transfered.")
	
	time.sleep(starting_delay)

	input_dict = dict()
	for i in range(len(pattern[0])):
		input_dict[(i%data.sw, i//data.sw)] = data.selection[i%data.sw][i//data.sw]
	output_dict = invert_dict(input_dict)

	for color in output_dict:
		r, g, b, a = color
		r /= 255
		g /= 255
		b /= 255
		a /= 255

		if a != 0:
			hc = matplotlib.colors.rgb2hex((r, g, b, a))
			pyautogui.click(buttonPositions[0]["button01"])
			pyautogui.click(buttonPositions[0]["button02"])
			pyautogui.typewrite(hc)
			pyautogui.click(buttonPositions[0]["button03"])

			for pixel in output_dict[color]:
				position = (pixel[0] + pixel[1] * len(data.selection))
				pyautogui.click(pattern[0][position])

				time.sleep(DELAY)
	if not auto:
		print("Done! The area you have selected has succesfully been transfered.")

def _auto_transfer_face(context=None, auto=False, starting_delay=STARTING_DELAY):
	if not context:
		print("Wrong use of the function! - You need to specify the part of the skin you want to use the preset of. - Type \"help\" for more.")
		return
	elif len(context[0].split("_")) != 2:
		print("Wrong use of the function! - Unknown preset. - Type \"help\" for more.")
		return

	part, face = context[0].split("_")

	if part not in PARTS or face not in FACES:
		print("Wrong use of the function! - Unknown preset. - Type \"help\" for more.")
		return

	if not auto:
		input(f"You will have {starting_delay} seconds to switch to the Pixel Strike 3D window after you hit [ENTER]. Before you do that, make sure that you are in the paint menu of the face that will get transfered.")

	time.sleep(starting_delay)

	_select(context=["part", f"{part}_{face}"], auto=True)
	_store(auto=True)
	_select(context=["part", f"{part}_{face}_layer"], auto=True)
	_add_on_top(auto=True)
	_restore(auto=True)
	_transfer(context=[get_pattern(part, face)], auto=True, starting_delay=0)

	print(("  " if auto else "") + f"Done! Face ({face}) transfered with success.")

def _auto_transfer_part(context=None, auto=False, starting_delay=STARTING_DELAY):
	if not context:
		print("Wrong use of the function! - You need to specify the preset to use. - Type \"help\" for more.") 
		return

	part = context[0]

	gpart = part

	if gpart in ["rarm", "larm", "rleg", "lleg"]:
		gpart = gpart[1:]

	if not auto:
		input(f"You will have {starting_delay} seconds to switch to the Pixel Strike 3D window after you hit [ENTER]. Before you do that, make sure that you are in the face selection menu of the part that will get transfered.")

	time.sleep(starting_delay)

	for face in FACES:
		pyautogui.click(buttonPositions[0][gpart]["faces"][face])
		_auto_transfer_face(context=[f"{part}_{face}"], auto=True, starting_delay=0)
		pyautogui.click(buttonPositions[0]["button04"])
		time.sleep(DELAY)

	print((" " if auto else "") + f"Done! Part ({part}) transfered with success.")

def _auto_transfer_skin(context=[''], auto=False, starting_delay=STARTING_DELAY):
	if not data.pixels:
		print("Wrong use of the function! - You need to open an image file as the skin to use first! - Use the \"open\" function.")
		return

	if not auto:
		input(f"You will have {starting_delay} seconds to switch to the Pixel Strike 3D window after you hit [ENTER]. Before you do that, make sure that you are in the part selection menu of the skin that will transfer to.")

	time.sleep(starting_delay)

	for part in PS3D_OPTI_PARTS:
		gpart = part

		if part in ["rarm", "rleg",]:
			side = part[0]
			gpart = part[1:]
			position = buttonPositions[0][gpart]["menu"][side]
		else:
			position = buttonPositions[0][gpart]["menu"]
 
		pyautogui.click(position)
		_auto_transfer_part(context=[part], auto=True, starting_delay=0)
		pyautogui.click(buttonPositions[0]["button05"])

	print("Done! Skin transfered with success.")

def blend_colors(color1, color2):
	r1, g1, b1, a1 = color1
	r2, g2, b2, a2 = color2

	a1 /= 255
	a2 /= 255

	a_result = a1 + a2 * (1 - a1)
	
	r_result = (r1 * a1 + r2 * a2 * (1 - a1)) / a_result if a_result != 0 else 0
	g_result = (g1 * a1 + g2 * a2 * (1 - a1)) / a_result if a_result != 0 else 0
	b_result = (b1 * a1 + b2 * a2 * (1 - a1)) / a_result if a_result != 0 else 0

	a_result *= 255
	
	return (r_result, g_result, b_result, a_result)

def invert_dict(input_dict):
	output_dict = {}
	for key, value in input_dict.items():
		if value not in output_dict:
			output_dict[value] = []
		output_dict[value].append(key)
	return output_dict

def get_pattern(part, face):
	if part != "head":
		if part in ["rarm", "larm", "rleg", "lleg"]:
			if face in ["front", "right", "left", "back"]:
				part = part[1:] + "0"
			elif face in ["top", "bottom"]:
				part = part[1:] + "1"
		else:
			part += default_pattern(face)
	return part

def default_pattern(face):
	if face in ["front", "back"]:
		return "0"
	elif face in ["right", "left"]:
		return "1"
	elif face in ["top", "bottom"]:
		return "2"

functions = {
	"help": [
		_help,
		"Displays all the currently available functions"
		],
	"version": [
		_version,
		"Displays the version of the current release of the application."],
	"exit": [
		_exit,
		"Exits the application."
		],
	"open": [
		_open,
		"Opens an image file as the skin to use.\n - Usage: open [filename]"
		],
	"select": [
		_select,
		"Selects the area to transfer.\n - Usage: select [mode]\n - The two modes are:\n  - \"position\": select position x1 y1 x2 y2\n   - Here x1 and x2 represent the coordinates of the top left corner of the selection\n   - And x2 and y2 the coordinates of the bottom right corner\n  - \"part\": select part [part]\n   - Here [part] represents the part. Here are the available part presets:\n    - All the part have this form: [part]_[face] or [part]_[face]_[layer].\n    - The available parts are \"head\", \"body\", \"rarm\", \"larm\", \"rleg\" and \"lleg\".\n    - The available faces are \"front\", \"right\", \"left\", \"back\", \"top\" and \"bottom\"."
		],
	"store": [
		_store,
		"Stores the current selection in memory. Confirmation required if a selection is already stored."
		],
	"restore": [
		_restore,
		"Restores the stored selection from the memory as the active selection. Confirmation required."
		],
	"show": [
		_show,
		"Displays the current selection.\n - Type \"show stored\" to show the stored selection."
		],
	"add_on_top": [
		_add_on_top,
		"Adds the current selection on top of the stored selection."
		],
	"transfer": [
		_transfer,
		"Transfers the selected area using a specific pattern that you specify.\n - Usage: transfer [preset]\n  - Here [preset] represents the preset you want to use.\n  - You can choose any of the following:\n   - \"head\": 16 x 16\n   - \"body0\": 8 x 12\n   - \"body1\": 4 x 12\n   - \"body2\": 12 x 4\n   - \"arm0\": 4 x 12\n   - \"arm1\": 4 x 4\n   - \"leg0\": 4 x 12\n   - \"leg1\": 4 x 4"
		],
	"auto_transfer_face": [
		_auto_transfer_face,
		"Transfers a face of a part of the skin while adding the layer of the face on top of it as well.\n - Usage: auto_transfer_face [part]_[face].\n  - The available parts are \"head\", \"body\", \"rarm\", \"larm\", \"rleg\" and \"lleg\".\n  - The available faces are \"front\", \"right\", \"left\", \"back\", \"top\" and \"bottom\"."
		],
	"auto_transfer_part": [
		_auto_transfer_part,
		"Transfers a part of the skin.\n - Usage: auto_transfer_face [part].\n  - The available parts are \"head\", \"body\", \"rarm\", \"larm\", \"rleg\" and \"lleg\"."
		],
	"auto_transfer_skin": [
		_auto_transfer_skin,
		"Transfers the skin. Need to open an image file as the skin to use first."
	]

}


partPositions = {
	"head_front": (8, 8, 16, 16),
	"head_right": (0, 8, 8, 16),
	"head_left": (16, 8, 24, 16),
	"head_back": (24, 8, 32, 16),
	"head_top": (8, 0, 16, 8),
	"head_bottom": (16, 0, 24, 8),
	"head_front_layer": (40, 8, 48, 16),
	"head_right_layer": (32, 8, 40, 16),
	"head_left_layer": (48, 8, 56, 16),
	"head_back_layer": (56, 8, 64, 16),
	"head_top_layer": (40, 0, 48, 8),
	"head_bottom_layer": (48, 0, 56, 8),
	"body_front": (20, 20, 28, 32),
	"body_right": (16, 20, 20, 32),
	"body_left": (28, 20, 32, 32),
	"body_back": (32, 20, 40, 32),
	"body_top": (20, 16, 28, 20),
	"body_bottom": (28, 16, 36, 20),
	"body_front_layer": (20, 36, 28, 48),
	"body_right_layer": (16, 36, 20, 48),
	"body_left_layer": (28, 36, 32, 48),
	"body_back_layer": (32, 36, 40, 48),
	"body_top_layer": (20, 32, 28, 36),
	"body_bottom_layer": (28, 32, 36, 36),
	"rarm_front": (44, 20, 48, 32),
	"rarm_right": (40, 20, 44, 32),
	"rarm_left": (48, 20, 52, 32),
	"rarm_back": (52, 20, 56, 32),
	"rarm_top": (44, 16, 48, 20),
	"rarm_bottom": (48, 16, 52, 20),
	"rarm_front_layer": (44, 36, 48, 48),
	"rarm_right_layer": (40, 36, 44, 48),
	"rarm_left_layer": (48, 36, 52, 48),
	"rarm_back_layer": (52, 36, 56, 48),
	"rarm_top_layer": (44, 32, 48, 36),
	"rarm_bottom_layer": (48, 32, 52, 36),
	"larm_front": (36, 52, 40, 64),
	"larm_right": (32, 52, 36, 64),
	"larm_left": (40, 52, 44, 64),
	"larm_back": (44, 52, 48, 64),
	"larm_top": (36, 48, 40, 52),
	"larm_bottom": (40, 48, 44, 52),
	"larm_front_layer": (52, 52, 56, 64),
	"larm_right_layer": (48, 52, 52, 64),
	"larm_left_layer": (56, 52, 60, 64),
	"larm_back_layer": (60, 52, 64, 64),
	"larm_top_layer": (52, 48, 56, 52),
	"larm_bottom_layer": (56, 48, 60, 52),
	"rleg_front": (4, 20, 8, 32),
	"rleg_right": (0, 20, 4, 32),
	"rleg_left": (8, 20, 12, 32),
	"rleg_back": (12, 20, 16, 32),
	"rleg_top": (4, 16, 8, 20),
	"rleg_bottom": (8, 16, 12, 20),
	"rleg_front_layer": (4, 36, 8, 48),
	"rleg_right_layer": (0, 36, 4, 48),
	"rleg_left_layer": (8, 36, 12, 48),
	"rleg_back_layer": (12, 36, 16, 48),
	"rleg_top_layer": (4, 32, 8, 36),
	"rleg_bottom_layer": (8, 32, 12, 36),
	"lleg_front": (20, 52, 24, 64),
	"lleg_right": (16, 52, 20, 64),
	"lleg_left": (24, 52, 28, 64),
	"lleg_back": (28, 52, 32, 64),
	"lleg_top": (20, 48, 24, 52),
	"lleg_bottom": (24, 48, 28, 52),
	"lleg_front_layer": (4, 52, 8, 64),
	"lleg_right_layer": (0, 52, 4, 64),
	"lleg_left_layer": (8, 52, 12, 64),
	"lleg_back_layer": (12, 52, 16, 64),
	"lleg_top_layer": (4, 48, 8, 52),
	"lleg_bottom_layer": (8, 48, 12, 52)
}

buttonPositions = {
	0: {
		"button01": (167, 280),
		"button02": (1021, 815),
		"button03": (1369, 157),
		"button04": (1815, 100),
		"button05": (830, 100),
		"head": {
			"menu": (360, 285),
			"faces": {
				"front": (480, 470),
				"right": (300, 470),
				"left": (650, 470),
				"back": (480, 640),
				"top": (480, 300),
				"bottom": (650, 300)
			}
		},
		"body": {
			"menu": (360, 450),
			"faces": {
				"front": (480, 470),
				"right": (270, 470),
				"left": (360, 470),
				"back": (650, 480),
				"top": (480, 310),
				"bottom": (480, 640)
			}
		},
		"arm": {
			"menu": {"r": (255, 450), "l": (475, 450)},
			"faces": {
				"front": (520, 480),
				"right": (350, 480),
				"left": (440, 480),
				"back": (610, 480),
				"top": (480, 315),
				"bottom": (480, 640)
			}
		},
		"leg": {
			"menu": {"r": (330, 660), "l": (400, 660)},
			"faces": {
				"front": (520, 480),
				"right": (350, 480),
				"left": (440, 480),
				"back": (610, 480),
				"top": (480, 315),
				"bottom": (480, 640)
			}
		},

	},
	1: {
		"head": [
			[(703, 82), (774, 84), (850, 81), (920, 83), (996, 83), (1069, 86), (1140, 86), (1219, 84), (701, 155), (779, 157), (850, 156), (925, 158), (995, 158), (1060, 156), (1137, 156), (1211, 154), (705, 225), (780, 227), (846, 230), (911, 229), (988, 229), (1070, 227), (1144, 229), (1214, 229), (704, 296), (779, 301), (856, 300), (923, 301), (992, 302), (1066, 304), (1130, 302), (1206, 303), (703, 368), (780, 370), (848, 371), (914, 372), (986, 372), (1062, 375), (1135, 376), (1205, 376), (709, 442), (780, 447), (850, 448), (920, 446), (990, 448), (1068, 450), (1140, 448), (1203, 448), (701, 518), (777, 519), (849, 519), (928, 518), (1002, 517), (1061, 519), (1137, 522), (1219, 522), (711, 590), (775, 591), (851, 595), (918, 596), (991, 594), (1064, 596), (1142, 598), (1213, 594)], # all the pixels to click
			(8, 8)
			],
		"body0": [
			[(705, 87), (779, 80), (851, 82), (922, 86), (999, 83), (1069, 83), (1144, 84), (1211, 81), (704, 156), (777, 155), (852, 161), (924, 158), (997, 160), (1062, 157), (1140, 157), (1206, 158), (701, 226), (782, 229), (852, 231), (924, 230), (998, 229), (1063, 230), (1133, 232), (1218, 228), (704, 302), (784, 303), (854, 301), (927, 303), (993, 302), (1071, 302), (1144, 303), (1210, 304), (706, 374), (782, 374), (854, 372), (921, 374), (998, 374), (1067, 375), (1141, 377), (1208, 377), (700, 448), (781, 448), (852, 451), (920, 448), (995, 446), (1066, 444), (1139, 447), (1213, 451), (700, 518), (776, 521), (853, 521), (922, 523), (997, 522), (1066, 519), (1137, 521), (1210, 521), (712, 590), (778, 589), (846, 591), (921, 591), (998, 590), (1073, 590), (1142, 590), (1220, 591), (705, 658), (778, 663), (852, 662), (922, 666), (999, 664), (1062, 662), (1139, 667), (1212, 668), (713, 731), (778, 733), (847, 734), (916, 738), (992, 735), (1067, 735), (1136, 735), (1212, 737), (705, 807), (775, 821), (846, 808), (921, 806), (999, 806), (1071, 808), (1141, 811), (1214, 810), (703, 879), (776, 884), (850, 885), (928, 885), (992, 885), (1068, 883), (1139, 885), (1207, 885)],
			(8, 12)
			],
		"body1": [
			[(851, 85), (921, 84), (993, 84), (1069, 85), (846, 155), (922, 157), (993, 158), (1065, 156), (849, 228), (921, 223), (995, 228), (1069, 227), (856, 291), (923, 299), (992, 299), (1067, 304), (846, 372), (928, 375), (995, 375), (1068, 376), (851, 450), (926, 445), (992, 443), (1065, 444), (847, 516), (923, 521), (996, 517), (1064, 514), (853, 592), (922, 589), (995, 587), (1070, 591), (851, 669), (922, 662), (995, 664), (1071, 666), (850, 735), (920, 736), (993, 734), (1069, 733), (848, 806), (927, 809), (996, 809), (1075, 807), (851, 881), (929, 878), (999, 883), (1062, 881)],
			(4, 12)
			],
		"body2": [
			[(705, 81), (779, 84), (852, 82), (923, 82), (994, 83), (1064, 82), (1148, 84), (1214, 85), (705, 158), (787, 158), (848, 161), (930, 158), (992, 155), (1068, 155), (1147, 156), (1215, 160), (708, 228), (777, 229), (844, 227), (922, 228), (999, 226), (1066, 228), (1139, 231), (1212, 228), (705, 297), (778, 298), (853, 300), (921, 304), (990, 301), (1074, 304), (1145, 306), (1209, 306)],
			(8, 4)
			],
		"arm0": [
			[(850, 84), (923, 84), (990, 83), (1067, 81), (850, 155), (928, 158), (992, 159), (1066, 157), (849, 228), (915, 227), (994, 228), (1066, 230), (845, 302), (923, 300), (996, 298), (1063, 300), (848, 375), (923, 374), (992, 373), (1065, 372), (854, 443), (924, 444), (993, 448), (1069, 447), (846, 515), (927, 514), (996, 516), (1062, 518), (852, 589), (926, 595), (993, 593), (1068, 594), (852, 666), (920, 665), (992, 664), (1067, 662), (852, 731), (918, 733), (993, 739), (1065, 735), (853, 813), (922, 806), (988, 806), (1063, 806), (849, 878), (922, 882), (992, 882), (1076, 881)],
			(4, 12)
			],
		"arm1": [
			[(848, 80), (923, 85), (994, 82), (1074, 82), (846, 155), (920, 160), (992, 162), (1070, 159), (851, 231), (922, 228), (992, 232), (1062, 232), (850, 294), (921, 302), (990, 302), (1067, 302)],
			(4, 4)
			],
		"leg0": [
			[(850, 84), (923, 84), (990, 83), (1067, 81), (850, 155), (928, 158), (992, 159), (1066, 157), (849, 228), (915, 227), (994, 228), (1066, 230), (845, 302), (923, 300), (996, 298), (1063, 300), (848, 375), (923, 374), (992, 373), (1065, 372), (854, 443), (924, 444), (993, 448), (1069, 447), (846, 515), (927, 514), (996, 516), (1062, 518), (852, 589), (926, 595), (993, 593), (1068, 594), (852, 666), (920, 665), (992, 664), (1067, 662), (852, 731), (918, 733), (993, 739), (1065, 735), (853, 813), (922, 806), (988, 806), (1063, 806), (849, 878), (922, 882), (992, 882), (1076, 881)],
			(4, 12)
			],
		"leg1": [
			[(848, 80), (923, 85), (994, 82), (1074, 82), (846, 155), (920, 160), (992, 162), (1070, 159), (851, 231), (922, 228), (992, 232), (1062, 232), (850, 294), (921, 302), (990, 302), (1067, 302)],
			(4, 4)
			]
	}
}

def run():
	print("Type \"help\" for more.")

	data.running = True
	while data.running:
		_input = input(">>> ")
		context = _input.split(" ")
		f = context.pop(0)

		if f in functions:
			if not context:
				functions[f][0]()
			else:
				functions[f][0](context)
		else:
			print("Function not available! Type \"help\" for more.")

data = Data()
data.pixels = None
data.selection = None
data.stored = None

_version()

if len(argv) >= 2:
	file = argv[1]

	_open(context=[file], auto=True)
	_auto_transfer_skin()

else:
	run()
