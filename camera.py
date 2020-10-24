#camera class/file with location, view angle, fov etc.
import math, numpy;

class camera():
    
    def __init__(self, name, pos, fov, render_distance, forward_v=numpy.matrix([[0],[0],[1]]), 
                 up_v=numpy.matrix([[0],[1],[0]]), left_v=numpy.matrix([[1],[0],[0]])):
        self.name = name;
        
        self.fov = fov; #input in radians    convert to vectors later?
        #alternatively we could just define the projection matrix size
        
        self.render_distance = render_distance;
        
        if(not isinstance(pos, list) or len(pos) != 3):
            raise TypeError("position must be a list with 3 values x,y,z");
        else:
            self.pos = pos;
        
        #camera rotation
        self.forward = forward_v;
        self.up = up_v;
        self.left = left_v;
        
        self.rounder = numpy.vectorize(lambda x: round(x,14)); #TODO:this is mostly for my sanity while testing. can be removed for speed later
        
        """#OLD
        #these values dont change if the camera moves (but doesnt rotate). should they change?
        self.base_vectors = [self._angles_to_vector(self.render_distance,[angle[0]+fov/2, angle[1]+fov/2]), #top left
                             self._angles_to_vector(self.render_distance,[angle[0]+fov/2, angle[1]-fov/2]), #bottom left
                             self._angles_to_vector(self.render_distance,[angle[0]-fov/2, angle[1]-fov/2]), #bottom right
                             self._angles_to_vector(self.render_distance,[angle[0]-fov/2, angle[1]+fov/2])]; #top right
        """
    
    #functions  # TODO: write a quick helper program that displays get_pos and get_ful after key presses(wasdqe,ijkluo)
    def get_pos(self):
        return self.pos;
    
    def translate(self, translation_v): #TODO: thsi uses absolute world coordinates instead of coordinates relative to the camera direction
        if(not isinstance(translation_v, list) or len(translation_v) != 3):
            raise TypeError("position translation must be a list with 3 values +x,+y,+z");
        else:
            self.pos[0] += translation_v[0];
            self.pos[1] += translation_v[1];
            self.pos[2] += translation_v[2];
    
    def pitch(self, angle): #looking up and down
        self.up = self.rounder(numpy.matrix([[1, 0, 0],
                                [0, math.cos(angle), -1*math.sin(angle)],
                                [0, math.sin(angle), math.cos(angle)]]).dot(self.up));
        self.forward = self.rounder(numpy.matrix([[1, 0, 0],
                                     [0, math.cos(angle), -1*math.sin(angle)],
                                     [0, math.sin(angle), math.cos(angle)]]).dot(self.forward));
        pass;
    
    def yaw(self, angle): #turning left and right
        self.forward = self.rounder(numpy.matrix([[math.cos(angle), 0, math.sin(angle)],
                                     [0, 1, 0],
                                     [-1*math.sin(angle), 0, math.cos(angle)]]).dot(self.forward));
        self.left = self.rounder(numpy.matrix([[math.cos(angle), 0, math.sin(angle)],
                                     [0, 1, 0],
                                     [-1*math.sin(angle), 0, math.cos(angle)]]).dot(self.left));
        pass;
    
    def roll(self, angle): #tilting clockwise and counterclockwise
        self.left = self.rounder(numpy.matrix([[math.cos(angle), -1*math.sin(angle), 0],
                                  [math.sin(angle), math.cos(angle), 0],
                                  [0, 0, 1]]).dot(self.left));
        self.up = self.rounder(numpy.matrix([[math.cos(angle), -1*math.sin(angle), 0],
                                [math.sin(angle), math.cos(angle), 0],
                                [0, 0, 1]]).dot(self.up));
        pass;
    
    def get_forward(self):
        return self.forward;
    def get_up(self):
        return self.up;
    def get_left(self):
        return self.left;
    def get_ful(self):
        print("forward:\n",self.forward);
        print("up:\n",self.up);
        print("left:\n",self.left);
    
    """#OLD
    def get_angle(self):
        return self.angle;
    def set_angle(self, new_target):
        if(not isinstance(new_target, list) or len(new_target)!= 2):
            raise TypeError("target vector must be a list with 2 values theta and phi");
        else:
            self.angle = new_target;     #rotation doesn't work at all
            self.base_vectors = [self._angles_to_vector(self.render_distance,[self.angle[0]+self.fov/2, self.angle[1]+self.fov/2]), #top left
                             self._angles_to_vector(self.render_distance,[self.angle[0]+self.fov/2, self.angle[1]-self.fov/2]), #bottom left
                             self._angles_to_vector(self.render_distance,[self.angle[0]-self.fov/2, self.angle[1]-self.fov/2]), #bottom right
                             self._angles_to_vector(self.render_distance,[self.angle[0]-self.fov/2, self.angle[1]+self.fov/2])]; #top right
    
    def get_base_vectors(self):
        return self.base_vectors;
    """
    def get_fov(self):
        return self.fov;
    
    def get_info(self):
        print("name:", self.name);
        print("fov:", self.fov);
        print("pos:", self.pos);
        print("render dist:", self.render_distance);
        
    """#OLD
    def _angles_to_vector(self, r_dist, angles):
        return [r_dist*math.sin(angles[0])*math.cos(angles[1]), 
                r_dist*math.sin(angles[0])*math.sin(angles[1]),
                r_dist*math.cos(angles[0])];
    """
