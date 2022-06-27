import numpy as np 
import matplotlib.pyplot as plt

# gives coordinates on a coordinate system
# centered at (0, 0)
# figures are in milimeters

print("""


40106: 


     14  13  12  11  10  9   8
     |   |   |   |   |   |   |
 -------------------------------
|                               |
|                               |
 -------------------------------
     |   |   |   |   |   |   |   
     1   2   3   4   5   6   7


                      width 
                        ^
                        |              
         <------------------------------>
                                       
         ---------------------------------        -
        |                                 |       | -> height
        |                                 |       |
         ---------------------------------        -
             |   |   |   |   |   |   |      
             *   *   *   *   *   *   *
             <--->      
    distance_between_pins 



                      width 
                        ^
                        |              
         <------------------------------>
                                                                  -
        |-----*---*---*---*---*---*---*----|                      |
              |   |   |   |   |   |   |                           |  
         ---------------------------------        -               |     
        |                                 |       | -> height     | -> height
        |                                 |       |               |   counting 
         ---------------------------------        -               |     pins
             |   |   |   |   |   |   |                            |  
        |----*---*---*---*---*---*---*----|                       |  
                                                                  -  

""")


width  = 19.939
height = 7.874
distance_between_pins = 2.540
distance_both_ends    = 2       #2.489
height_counting_pins  = 8.128


print("-"*60)
print("Width  = {} mm".format(width))
print("Height = {} mm".format(height))
print("Distance between pins = {} mm".format(distance_between_pins))
print("Distance between both ends = {} mm".format(distance_both_ends))
print("Height counting distance to pins = {} mm".format(distance_both_ends))
print("-"*60)

# x position of pins
pins_x    = np.arange(  start = 0, 
                        stop  =  (width/2) - distance_both_ends,
                        step  =  distance_between_pins)

# number of pins
number_of_pins = pins_x.shape[0]

#
pins_y_upper = np.ones(number_of_pins) * (-height/2)
pins_y_lower = np.ones(number_of_pins) * (height/2)


print("Number of pins: {}".format(number_of_pins))
print("X position of pins: {} | {}".format(pins_x, -pins_x))
print("Y position of higher pins: {}".format(height/2))
print("Y position of lower  pins: {}".format(-height/2))



# variables for drawing de box that represents the 
# package box of the 40106, just for correctness
# check with graphics

# draws both of the horizontal lines that delimit the box 
inner_box_width_x = np.arange(start =  0, 
                              stop  =  width/2, step = 0.01)
nbox_points       = inner_box_width_x.shape[0]

inner_box_widht_y_upper = np.ones(nbox_points) *  height/2
inner_box_widht_y_lower = np.ones(nbox_points) * -height/2


# draws the vertical lines that delimit the box
inner_box_height_y = np.arange( start =  0, 
                                stop  =  height/2, step = 0.01)
nbox_points        = inner_box_height_y.shape[0]

inner_box_height_x_right = np.ones(nbox_points) *  -width/2
inner_box_height_x_left  = np.ones(nbox_points) *   width/2


plt.plot(inner_box_width_x, inner_box_widht_y_upper)
plt.plot(inner_box_width_x, inner_box_widht_y_lower)

plt.plot(-inner_box_width_x, inner_box_widht_y_upper)
plt.plot(-inner_box_width_x, inner_box_widht_y_lower)
#plt.plot(inner_box_height_x_left, inner_box_height_y)
#plt.plot(inner_box_height_x_right, inner_box_height_y)

plt.scatter(x = pins_x, y = pins_y_upper)
plt.scatter(x = pins_x, y = pins_y_lower)

plt.scatter(x = -pins_x, y = pins_y_upper)
plt.scatter(x = -pins_x, y = pins_y_lower)
plt.show()




