#this will eventually be the main loop, renderer and player controls etc.

#camera ray starts at player location and ends at max draw distance
import poly, camera, gen_world, convert_coor, render;
import math, numpy; #TODO: only import functions that are needed
from PIL import Image, ImageDraw;
import subprocess;

#create cameras here
cam = camera.camera("camgirl", [0,0,0], math.pi/1.5, 15);
#cam.yaw(-1*math.pi/4);
#cam.get_info();
width = 144;
height = 144;
up_sampling = 1;
threads = 16; #must be a square number
if(width%threads != 0 or height%threads != 0): #and divisible by the resolution to avoid tiling effect
    raise Exception("thread count resolution incompatibility");
#main_loop
#run gen_world to get list of possibly visible polygons
#TODO: replace poly with rectangular prisims where polys make up the faces
poly_list = gen_world.list_polys();
#[print(x.get_coor()) for x in poly_list];
#print(poly_list);

#convert polygon coordinates to coor relative to the camera
rel_cam_poly_list = convert_coor.convert_coor(poly_list, cam.get_pos(), cam.get_forward());
#[print(x.get_coor()) for x in rel_cam_poly_list];
#print(rel_cam_poly_list);

#pass new polygon coor into render
frame = render.render(width, height, rel_cam_poly_list, cam, threads);

#TODO: post processing blur/blend pixels
im = Image.new("RGB",(width*up_sampling,height*up_sampling));
im_draw = ImageDraw.Draw(im);

for x in range(0, width*up_sampling, up_sampling):
    for y in range(0, height*up_sampling, up_sampling):
        
        #print(x,y, type(frame[x][y]));
        if(isinstance(frame[int(x/up_sampling)][int(y/up_sampling)], str)):
            frame[int(x/up_sampling)][int(y/up_sampling)] = eval(frame[int(x/up_sampling)][int(y/up_sampling)]);
            
        temp = [];
        for a in range(up_sampling):
            for b in range(up_sampling):
                temp.append(x+a);
                temp.append(y+b);
        #print(temp);
        
        im_draw.point(temp, fill=frame[int(x/up_sampling)][int(y/up_sampling)]);
f= "./output.png";
im.save(f);
#subprocess.run(["gwenview", f]);
#int(y/up_sampling)
