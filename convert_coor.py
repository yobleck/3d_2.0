#converts world coordinates to camera relative coordinates
import poly;
import copy;
#TODO: this handles translation but not rotation
def convert_coor(poly_list, cam_pos, cam_look):
    new_list = [];
    for poly in poly_list:
        temp_poly = copy.copy(poly); #create new poly object   this is inefficient. is it ok to just modiy source?
        temp_coor = temp_poly.get_coor();
        
        temp_poly.set_coor(tuple([y-cam_pos[x] for x,y in enumerate(temp_coor[0])]) , #go thru x,y,z of p1 and shift by cam x,y,z
                           tuple([y-cam_pos[x] for x,y in enumerate(temp_coor[1])]) ,
                           tuple([y-cam_pos[x] for x,y in enumerate(temp_coor[2])]) );
        
        #temp_poly.set_coor(rotate(),
                           #rotate(),
                           #rotate());
        
        new_list.append(temp_poly);
    
    return new_list;


def rotate():
    return;
