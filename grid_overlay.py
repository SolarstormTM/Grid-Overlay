#!/usr/bin/env python

# Draw a grid over a picture in GIMP.
# AJ is best pony!
# Copyright 2015 by Solarstorm
# You may use and distribute this plug-in under the terms of the GPL.


from gimpfu import *
# This is a copy from http://stackoverflow.com/questions/14381940/python-pair-alphabets-after-loop-is-completed
from itertools import count, product, islice
from string import ascii_uppercase

def multiletters(seq):
	for n in count(1):
		for s in product(seq, repeat=n):
			yield ''.join(s)
# End

def grid_overlay(img, layer, col, row) :
	exists, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)

	if not exists :
		pdb.gimp_message("No area selected.")
		return

	length = x2 - x1
	height = y2 - y1

	x_step = int(round(length / col, 0))
	y_step = int(round(height / row, 0))

	pdb.gimp_image_undo_group_start(img)

	new_layer = pdb.gimp_layer_new(img, layer.width, layer.height, 1, "Grid", 100, 0)
	#pdb.gimp_layer_add_alpha(new_layer)
	pdb.gimp_image_insert_layer(img, new_layer, None, -1)
	savesel = pdb.gimp_selection_save(img)
	pdb.gimp_selection_none(img)

	for i in range(0,row + 1) :
		if i == 0 :
			var = y1
			#pdb.gimp_message("var: " + str(var) + " i: " + str(i))
		else :
			var = var + y_step
		vec = [x1,var,x2,var]
		pdb.gimp_pencil(new_layer, len(vec), vec)

	for i in range(0, col + 1) :
		if i == 0 :
			var = x1
		else :
			var = var + x_step
		vec = [var, y1, var, y2]
		pdb.gimp_pencil(new_layer, len(vec), vec)

	pdb.gimp_selection_load(savesel)
	pdb.gimp_image_undo_group_end(img)		

def grid_overlay_quadrat(img, layer, pixel) :
	exists, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)

	if not exists :
		pdb.gimp_message("No area selected.")
		return

	length = x2 - x1
	height = y2 - y1

	x_step = int(round(length / pixel, 0))
	y_step = int(round(height / pixel, 0))


	# Test if we add an extra column.
	check = x_step * pixel
	if check == length :
		# Perfect, nothing to do!
		x_step = x_step
	elif check < length :
		if (length - check) > (float(pixel) / 2) :
			x_step = x_step + 1
	elif check > length :
		if (check - length) > (float(pixel) / 2) :
			x_step = x_step + 1

	# Test if we add an extra row.
	check = y_step * pixel
	if check == height :
		# Perfect, nothing to do!
		y_step = y_step
	elif check < height :
		if (height - check) > (float(pixel) / 2) :
			y_step = y_step + 1
	elif check > height :
		if (check - height) > (float(pixel) / 2) :
			y_step = y_step + 1

	new_length = x_step * pixel
	new_height = y_step * pixel

	#Let's draw.
	#Start the undo recording.
	pdb.gimp_image_undo_group_start(img)
	#Make a new Layer.
	new_layer = pdb.gimp_layer_new(img, layer.width, layer.height, 1, "Grid", 100, 0)
	pdb.gimp_image_insert_layer(img, new_layer, None, -1)
	savesel = pdb.gimp_selection_save(img)
	pdb.gimp_selection_none(img)
	# Let's draw the horizontal lines and caption
	m = multiletters(ascii_uppercase)
	for i in range(0,y_step + 1) :
		letter = next(m)
		
		#pdb.gimp_message(letter)
		if i == 0 :
			var = y1
			y_letter = y1 + int(round(float(pixel)/4, 0))
		else :
			var = var + pixel
			y_letter = y_letter + pixel
		if i != y_step :
			fontlayer = pdb.gimp_text_fontname(img, None, 0, 0, letter, 0, TRUE, float(pixel)/2, 0, "Arial")
			pdb.plug_in_autocrop_layer(img, fontlayer)
			pdb.gimp_layer_set_offsets(fontlayer, x1 - int(round(float(pixel)/2)) * len(letter), y_letter)
		vec = [x1,var,x1 + new_length,var]
		pdb.gimp_pencil(new_layer, len(vec), vec)

		# Let's draw the vertical lines and caption
	for i in range(0, x_step + 1) :
		if i == 0 :
			var = x1
			x_letter = x1 + int(round(float(pixel)/2, 0))
		else :
			var = var + pixel
			x_letter = x_letter + pixel
		if i != x_step :
			fontlayer = pdb.gimp_text_fontname(img, None, 0, 0, str(i+1), 0, TRUE, float(pixel)/2, 0, "Arial")
			pdb.plug_in_autocrop_layer(img, fontlayer)
			pdb.gimp_layer_set_offsets(fontlayer, x_letter - int(round(float(fontlayer.width), 0))/2, y1 - int(round(float(pixel)/2)))
		vec = [var, y1, var, y1 + new_height]
		pdb.gimp_pencil(new_layer, len(vec), vec)

	pdb.gimp_selection_load(savesel)
	pdb.gimp_image_undo_group_end(img)		
register(
         "python_fu_grid_overlay",
         "Draw a grid",
         "Draw a grid over a selection",
         "Solarstorm", "Solarstorm",
         "2015",
         "<Image>/Filters/Render/Grid Overlay...",
         "*",
         [
			#(PF_INT, "col",  "Columns", 10),
			#(PF_INT, "row",  "Rows", 10),
			(PF_INT, "pixel",  "Quadrat Pixel", 60),
			#(PF_INT, "t",  "Thickness", 3),
			#(PF_COLOR , "gridcolor",  "Grid Color", (0,0,0)),
			#(PF_BOOL, "captionenable",  "Enable Caption", 1),
			#(PF_FONT, "fontname",  "Caption Font", "Arial"),
			#(PF_COLOR , "fontcolor",  "Font Color", (0,0,0)),
         ],
         [],
         grid_overlay_quadrat)

main()