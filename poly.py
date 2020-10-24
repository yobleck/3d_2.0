#defines an object that is a 2D polygon defined by 3 coordinates and a normal vector
import math, numpy;
class poly():
    def __init__(self, name, color, p1, p2, p3):
        self.name = name;
        self.color = color; #TODO: convert to numpy matrix
        if(not isinstance(p1,tuple) or not isinstance(p2,tuple) or not isinstance(p3,tuple)):
            raise TypeError("points must be of the tuple type");
        elif(len(p1) != 3 or len(p2) != 3 or len(p3) != 3):
            raise Exception("tuples must have 3 values x,y,z");
        else:
            self.p1 = p1;
            self.p2 = p2;
            self.p3 = p3;
        
        self.normal_vector = tuple(numpy.cross( (self.p1[0]-self.p2[0], self.p1[1]-self.p2[1], self.p1[2]-self.p2[2]) ,
                                                (self.p3[0]-self.p2[0], self.p3[1]-self.p2[1], self.p3[2]-self.p2[2]) ));
        
        self.normal_vector_magnitude = math.sqrt(self.normal_vector[0]**2 + self.normal_vector[1]**2 + self.normal_vector[2]**2);
        
        #TODO: use numpy .normalize function?
        self.unit_normal_vector = (self.normal_vector[0]/self.normal_vector_magnitude, #this wont work if 2 coordinates are the same which shouldnt happen but still
                                   self.normal_vector[1]/self.normal_vector_magnitude,
                                   self.normal_vector[2]/self.normal_vector_magnitude);
        
        self.unit_normal_vector_magnitude = math.sqrt(self.unit_normal_vector[0]**2 + 
                                                      self.unit_normal_vector[1]**2 + 
                                                      self.unit_normal_vector[2]**2);
        
                                                #arbitrary values to fix floating point precision issue
        if(self.unit_normal_vector_magnitude < 0.9999 or self.unit_normal_vector_magnitude > 1.0001): #TODO: see round(x,10)
            raise Exception("unit_normal_vector_magnitude != 1 \n something went wrong with calculating vectors");
        
    def get_coor(self):
        return (self.p1,self.p2,self.p3);
    def set_coor(self,ip1,ip2,ip3):
        if(not isinstance(ip1,tuple) or not isinstance(ip2,tuple) or not isinstance(ip3,tuple)):
            raise TypeError("points must be of the tuple type");
        elif(len(ip1) != 3 or len(ip2) != 3 or len(ip3) != 3):
            raise Exception("tuples must have 3 values x,y,z");
        else:
            self.p1 = ip1;
            self.p2 = ip2;
            self.p3 = ip3;
    
    def get_vector(self):
        return self.normal_vector;
    def get_vector_magnitude(self):
        return self.normal_vector_magnitude;
    
    def get_unit_vector(self):
        return self.unit_normal_vector;
    
    def get_name(self):
        return self.name;
    def get_color(self):
        return self.color;
        
    def get_info(self):
        print("name:",self.name);
        print("color:",self.color);
        print("coor:",self.p1,self.p2,self.p3);
        print("normal vector:",self.normal_vector);
        print("normal vector magnitude",self.normal_vector_magnitude);
        print("unit normal vector",self.unit_normal_vector);
        print("unit normal vector magnitude",self.unit_normal_vector_magnitude);
