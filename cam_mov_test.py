#TODO: write a quick helper program that displays get_pos and get_ful after key presses(wasdqe,ijkluo) 
import camera, math, os;
cam = camera.camera("test",[0,0,0],90,20)

while(True):
    key = input();
    
    if(key == "w"):
        cam.translate([0,0,1]);
    if(key == "a"):
        cam.translate([1,0,0]);
    if(key == "s"):
        cam.translate([0,0,-1]);
    if(key == "d"):
        cam.translate([-1,0,0]);
    if(key == "q"): #move up
        cam.translate([0,1,0]);
    if(key == "e"): #move down
        cam.translate([0,-1,0]);
    
    if(key == "i"): #look down
        cam.pitch(math.pi/4);
    if(key == "j"): #look left
        cam.yaw(math.pi/4);
    if(key == "k"): #look up
        cam.pitch(-1*math.pi/4);
    if(key == "l"):#look right
        cam.yaw(-1*math.pi/4);
    if(key == "u"): #roll counterclockwise
        cam.roll(-1*math.pi/4);
    if(key == "o"): #roll clockwise
        cam.roll(math.pi/4);
    
    os.system("clear");
    print("position:", cam.get_pos(), "\n",
          "forward:\n", cam.get_forward(), "\n",
          "up:\n", cam.get_up(), "\n",
          "left:\n", cam.get_left());
