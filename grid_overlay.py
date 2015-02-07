#!/usr/bin/env python

# Draw a grid over a picture in GIMP.
# AJ is best pony!
# Copyright 2015 by Solarstorm
# You may use and distribute this plug-in under the terms of the GPL.


from gimpfu import *

def grid_overlay(img, layer, col, row) :
    exists, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
    
	if not exists :
        return
	
	length = x2 - x1
	height = y2 - y1
	
	x_step = int(round(length / col, 0))
	y_step = int(round(height / row, 0))
	
	pdb.gimp_image_undo_group_start(img)
	
	new_layer = pdb.gimp_image_insert_layer(img, layer, 0, 0)
	pdb.gimp_selection_none(img)
	for i in range(0,row) :
		if i == 0 :
			var = x1
		else :
			var = var + y_step
		vec = [x1,var,x2,var]
		pdb.gimp_paintbrush_default(layer, len(vec), vec)
	
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
           (PF_INT, "col",  "Columns", 10),
           (PF_INT, "row",  "Rows", 10),
           #(PF_INT, "t",  "Thickness", 3),
           #(PF_COLOR , "gridcolor",  "Grid Color", (0,0,0)),
		   #(PF_BOOL, "captionenable",  "Enable Caption", 1),
           #(PF_FONT, "fontname",  "Caption Font", "Arial"),
           #(PF_COLOR , "fontcolor",  "Font Color", (0,0,0)),
         ],
         [],
         grid_overlay, menu="<Image>/Filters/Render")

main()