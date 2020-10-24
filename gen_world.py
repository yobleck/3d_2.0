#reads info from map file and creates a list of 2D polygon objects
#eventually turn this into a file that reads octree/bsp(whtev) and returns list of polygons     see notes.txt Section 2
from poly import poly;
import tree;
import math, numpy;

def list_polys():
    f = open("./map.txt","r");
    polys = f.readlines();
    #print(polys);
    f.close();

    poly_obj = [];
    for x in polys:
        #print("pre new line",x);
        if(x != "\n"): #ignore empty lines
            temp = x.rstrip("\r\n");
            #print("post strip",temp);
            temp = temp.split("/");
            #print("temp:",temp);
            #if( eval(temp[2])[2] > 0 or eval(temp[3])[2] > 0 or eval(temp[4])[2] > 0): #wrong file
            poly_obj.append(poly(temp[0],temp[1],eval(temp[2]),eval(temp[3]),eval(temp[4])));
        else:
            #print("empty line");
            pass;
    #TODO: rotate objects around camera forward by vector indicated by camera up
    """
    print(poly_obj);
    for x in poly_obj:
        x.get_info();
    """
    #TODO: sort objects to that farthest away is first in list
    return poly_obj;

#GARBAGE
def build_tree():
    poly_list = list_polys();
    boundary = 0;
    for x in poly_list:
        for point in x.get_coor():
                if(max(point) > boundary):
                       boundary = max(point); #DRY
    print(boundary);
    
    temp_tree = tree.Node((0,0,0),boundary);
    recursion(temp_tree, list(poly_list), (0,0,0), boundary);
    #print(temp_tree.get_children());
    print_tree(temp_tree, 0);
    
    

#GARBAGE
def recursion(input_node,input_list, center, size):
    if(len(input_list) == 1): #sub region has one polygon in it
        input_node.add_child(input_list[0]);
    
    else: #sub region has multiple polygons in it
        quad = [-1,1]; #TODO: this only works when the center is the origin. this needs to work no matter what the value of temp_center is
        for x in quad: #iterate thru the 8 sub regions
            for y in quad:
                for z in quad:
                    #calculate sub regions center and boundary
                    half_size = size/2;
                    temp_center = (x*half_size,y*half_size,z*half_size);
                    #print("size",half_size,"center",temp_center);
                    #TODO: maybe rework this whole section so that if any of the points in a poly are in a region then that poly
                    #is added to that region
                    #ignoring size of poly and where is centroid is
                    #and for testing purposes maybe jsut do a fixed numer of sub divisions like 2 or 3
                    is_in_region = [];
                    for poly in input_list:
                        #print(poly.get_name());
                        #check if poly centroid is in sub region
                        coors = poly.get_coor();
                        centroid = ((coors[0][0]+coors[1][0]+coors[2][0])/3, #x
                                    (coors[0][1]+coors[1][1]+coors[2][1])/3, #y
                                    (coors[0][2]+coors[1][2]+coors[2][2])/3); #z value of centroid
                        #print("centroid",centroid);
                        dif = numpy.subtract(temp_center,centroid);
                        #print("dif",dif);
                        #c_magnitude = math.sqrt((dif[0])**2+(dif[1])**2+(dif[2])**2);
                        #print("dis frm cent to roid",c_magnitude);
                        
                        cross_product = numpy.cross((coors[0][0]-coors[1][0],coors[0][1]-coors[1][1],coors[0][2]-coors[1][2]),
                                                   (coors[2][0]-coors[1][0],coors[2][1]-coors[1][1],coors[2][2]-coors[1][2]));
                        #print("cross product",cross_product);
                        sa_magnitude = math.sqrt(cross_product[0]**2+cross_product[1]**2+cross_product[2]**2);
                        surface_area = sa_magnitude/2;
                        #print("surface area",surface_area);
                        
                        #and if poly surface area is larger than sub regions largest surface   to deal with large polys
                        if(surface_area < size**2):
                            if(abs(dif[0]) <= half_size and abs(dif[1]) <= half_size and abs(dif[2]) <= half_size):
                                is_in_region.append(poly);
                            
                    #print("num poly in sub",len(is_in_region));
                    #[print(x.get_name()) for x in is_in_region];
                    #print("");
                    #"""
                    temp_node = tree.Node(temp_center,half_size)
                    input_node.add_child(temp_node);
                    if(is_in_region):
                        recursion(temp_node, is_in_region, temp_center, half_size);
                    #"""


def print_tree(input_tree, tier):
    print("tier",tier);
    if(len(input_tree.get_children()) > 1):
        for x in input_tree.get_children():
            print_tree(x, tier+1);
    if(len(input_tree.get_children()) == 1):
        print(input_tree.get_info());
    if(len(input_tree.get_children()) <= 0):
        print("empty");
