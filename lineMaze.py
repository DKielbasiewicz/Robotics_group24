from robots import *
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from time import sleep

client = RemoteAPIClient()
sim = client.require("sim")

# HANDLES FOR ACTUATORS AND SENSORS
"""
left_motor, right_motor:
    Basically robot has left and right wheel
    Methods we can use:
        - run(speed):
            It gives certain speed to the left wheel (we can steer the robot)

color_sensor:
    Color sensor is used to detect the color of the line
"""

left_motor = Motor(sim, DeviceNames.MOTOR_LEFT_LINE, Direction.CLOCKWISE) # left wheel engine
right_motor = Motor(sim, DeviceNames.MOTOR_RIGHT_LINE, Direction.CLOCKWISE) # right wheel engine
# Color sensor is the 
color_sensor = ImageSensor(sim, DeviceNames.IMAGE_SENSOR_LINE) #what robot sees

def is_red_detected(color_sensor):
    """
    Calculates the relative intensity of the red channel compared to
    other channels
    """
    red_ratio_threshold = 1.5
    red, green, blue = color_sensor.rgb()
    print(red, green, blue)
    red_intensity = red / (green + blue)

    return red_intensity > red_ratio_threshold


def is_blue_detected(color_sensor):
    """
       Calculates the relative intensity of the blue channel compared to
       other channels
       """
    blue_ratio_threshold = 1.5
    red, green, blue = color_sensor.rgb()
    blue_intensity = blue / (red + green)

    return blue_intensity > blue_ratio_threshold

# def turn(image_array):
#     # First, check if all values in the array are 23
#     if (image_array == 23).all():
#         return 1
#     elif (image_array == 0).all():
#         return 1

#     # Now count how many 23s are on left half vs right half
#     left_half = image_array[:, :8, :]
#     right_half = image_array[:, 8:, :]

#     count_left = np.sum(left_half == 23)
#     count_right = np.sum(right_half == 23)

#     if count_left > count_right:
#         if count_left < 64:
#             return 0.2 # turn left faster, increase the speed in the right wheel
#         else:
#             return 0.1  # Turn left slower, 
#     elif count_right > count_left:
#         if count_right < 64:
#             return 2.2 # Turn right faster
#         else:
#             return 2.1  # Turn right slower

base_speed = 4.2
target = 49
Kp = 0.071
Ki = 0.006294
Kd = 0.0062
error_sum = 0
last_error = 0 

"""
Setup that works the full track
base_speed = 4.2
target = 49
Kp = 0.071
Ki = 0.0061
Kd = 0.0062
time :: 1m 20s

----
Smoother turn
base_speed = 4.2
target = 49
Kp = 0.071
Ki = 0.00581
Kd = 0.00668


base_speed = 4.2
target = 49
Kp = 0.071
Ki = 0.006294
Kd = 0.0062
error_sum = 0
last_error = 0 
"""

def follow_line():
    """
    A very simple line follower that should be improved.
    """
    color_sensor._update_image() # Updates the internal image
    image = color_sensor.get_image()
    reflection = color_sensor.reflection() # Gets the reflection from the image
    print(reflection)
    #black color reflection max 9
    #white color refl max 85
    global error_sum, last_error
    error = target - reflection
    error_sum += error

    P = error * Kp
    I = error_sum * Ki
    D = (error - last_error) * Kd
    control_signal = P + I + D
    last_error = error

    left_motor.run(int(base_speed + control_signal))
    right_motor.run(int(base_speed - control_signal))
    


    # turn_decision = turn(image)
    # # left_motor.run(speed=5) # Runs the left motor at speed=5
    # # right_motor.run(speed=5) # Runs the right motor at speed=5
    # if turn_decision == 1:
    #     left_motor.run(speed=5)
    #     right_motor.run(speed=5)

    # elif turn_decision == 0.1:
    #     right_motor.run(speed=0.5)
    #     left_motor.run(speed=4.3)
    # elif turn_decision == 0.2:
    #     right_motor.run(speed=0)
    #     left_motor.run(speed=4.5)

    # elif turn_decision == 2.1:
    #     right_motor.run(speed=4.3)
    #     left_motor.run(speed=0.5)
    # elif turn_decision == 2.2:
    #     right_motor.run(speed=4.5)
    #     left_motor.run(speed=0)
    # # elif turn_decision == 4:
    # #     left_motor.run(speed=3)
    # #     right_motor.run(speed=0)
        

# Starts coppeliasim simulation if not done already
sim.startSimulation()

# MAIN CONTROL LOOP
while True:
    # image = color_sensor.get_image()
    # show_image(image)
    follow_line()
