#takes info from gen_world and calculates what can actually be seen
#treats camera as origin
#returns 2D array
import math, numpy;
import multiprocessing;
#from PIL import Image, ImageDraw;

#1.) main function
def render(width, height, poly_list, camera, threads): #shouldn't be able to modify camera from here. pass vars one by one?
    
    origin = camera.get_pos();
    look = camera.get_forward();
    fov = camera.get_fov();
    frame_buffer = numpy.empty((width, height), dtype=tuple);
    frame_buffer.fill((0,0,0));
    
    ray = look.copy(); # starts looking forward
    
    #mult = 50;
    #im_draw.point(( (ray.item(0)*mult)+51 , (ray.item(1)*mult)+mult ),fill=(0,255,255));
    sqrt_threads = int(math.sqrt(threads));
    quad = [];
    for i in range(sqrt_threads):
        for j in range(sqrt_threads):
            quad.append([ray, look, fov, poly_list, width, height, sqrt_threads, i, j]);
    
    #TODO: rotate and then draw misses first column. and vice versa
    
    #Multithread spawning
    with multiprocessing.Pool(threads) as p:
        arr_list = p.starmap(func, quad);
        
    for x in range(width):
        for y in range(height):
            for v in range(threads):
                if(arr_list[v][x,y]):
                    frame_buffer[x,y] = arr_list[v][x,y]; #formerly arr
    #print(frame_buffer);
    return frame_buffer;

##########

#2.) iterates through all the ray angles and every polygon and runs intersection function
def func(ray, look, fov, poly_list, width, height, sqrt_threads, i, j):
    w = width//sqrt_threads;
    h = height//sqrt_threads;
    
    arr_test = numpy.empty((width,height), dtype=tuple);
    for x in range(w*i, w*i+w):
        for y in range(h*j, h*j+h):
            ray = look.copy();
            ray = ray_yaw(ray,(fov/2) - (x*fov/width));
            ray = ray_pitch(ray,(fov/2) - (y*fov/height));
            
            for poly in poly_list:
                fb = intersects_plane_of_poly(ray, poly);
                
                if(fb != (0,0,0)):
                    arr_test[x, height-1-y] = fb;
    
    return arr_test;

##########

#2.5.) helper functions for rotating rays
def ray_yaw(temp, angle):
        return numpy.matrix([[math.cos(angle), 0, math.sin(angle)],
                            [0, 1, 0],
                            [-1*math.sin(angle), 0, math.cos(angle)]]).dot(temp);
#TODO: replace all the math.cos/sin(angle) with predetermined values math.cos/sin(fov/width or height)    
def ray_pitch(temp, angle):
    return numpy.matrix([[1, 0, 0],
                        [0, math.cos(angle), -1*math.sin(angle)],
                        [0, math.sin(angle), math.cos(angle)]]).dot(temp);

##########

#5.) calculates area of triangles     opencl here?
def area_of_poly(point1, point2, ray_point):
    temp = tuple(numpy.cross( (point1[0]-point2[0], point1[1]-point2[1], point1[2]-point2[2]) ,
                              (ray_point[0]-point2[0], ray_point[1]-point2[1], ray_point[2]-point2[2]) ));
    area = math.sqrt(temp[0]**2 + temp[1]**2 + temp[2]**2)/2;
    #normal_vector_magnitude/2 = area of triangle
    return area;

##########
    
#4.) checks if ray intersects polygon by comparing triangle areas
def in_poly(poly, plane_intersect): #input where camera ray intersects plane and check if inside polygon
    poly_area = poly.get_vector_magnitude()/2;
    point_area_1 = area_of_poly(poly.get_coor()[0], poly.get_coor()[1] , plane_intersect);
    point_area_2 = area_of_poly(poly.get_coor()[0], poly.get_coor()[2], plane_intersect);
    point_area_3 = area_of_poly(poly.get_coor()[1], poly.get_coor()[2], plane_intersect);
    if(point_area_1+point_area_2+point_area_3 <= poly_area+1e-13): #rounding errors cause visual artifacts hence the +small number
        return True;
    else:
        return False;

##########

#3.) checks to see if ray intersects plane of polygon then runs function to see if ray intersects polygon
def intersects_plane_of_poly(ray, poly): #input camera ray and poly object
    
    poly_vec = poly.get_unit_vector(); #using get_vector() doesn't seem to make a difference
    """#OLD
    dot = ray.item(0)*poly_vec[0] + ray.item(1)*poly_vec[1] + ray.item(2)*poly_vec[2];
    print(poly.get_name(), dot);
    if(dot < 0 and poly.get_coor()[1][2] > 0):
        print(poly.get_name(), "is visible");
    """
    dot1 = poly_vec[0]*poly.get_coor()[1][0] + poly_vec[1]*poly.get_coor()[1][1] + poly_vec[2]*poly.get_coor()[1][2] #precalculate and store?
    dot2 = ray.item(0)*poly_vec[0] + ray.item(1)*poly_vec[1] + ray.item(2)*poly_vec[2]; #if 0 then no intersection?
    
    if(dot2 != 0):
        u = dot1/dot2;
        
        if(u > 0): #culls something so that polygons stop drawing in places they shouldnt be (i.e. bit flipped over an axis)
            #if(poly.get_name() == "top"):
                #print("dots", dot1, dot2, u);
            plane_intersect = (u*ray.item(0), u*ray.item(1), u*ray.item(2));
            
            if(in_poly(poly, plane_intersect)):
                return poly.get_color();
            else:
                return (0,0,0);
        else:
            return (0,0,0);
    else:
        return (0,0,0);


#NOTES
#https://www.gamedev.net/tutorials/programming/math-and-physics/practical-use-of-vector-math-in-games-r2968/
#P1 = camera coor
#P2 = max draw distance along ray from camera which is a previously calculated vector
#SP = one of the points from the inputted polygon
#SN = polygon unit? normal vector
#dot1 = SN dot (SP - P1) #subtracting one point tuple from another
#dot2 = SN dot (P2 - P1) 

#u = (SN dot (SP - P1)) / (SN dot (P2 - P1)) 
#if u == 0, line is parallel the plane. #dont draw  also maybe dont draw if u very close to 0 like 0.0001
#if u > 1, no intersection. #dont draw
#if u <= 1 and u > 0, line intersects the plane. #draw if point inside polygon
    
    #intersection point = (P2 - P1) * u #only use if u between 0 and 1
    #pass on to in_poly()
