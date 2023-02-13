import cv2
import numpy as np
import sys
from image_h import *
from time import sleep
import subprocess
from motor_h import *
from regression import *
from sound import *
#SERVO_ALL_reset()
cmd = 'python servo_h.py'

COLLECT_ORIGINAL_DATA = 0


def aim_the_goal():
    global COLLECT_ORIGINAL_DATA 
    ready = 0
    while ready == 0:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours in the blue mask
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours_blue) > 0:
            c_blue = max(contours_blue, key=cv2.contourArea)
            x_blue,y_blue,w_blue,h_blue = cv2.boundingRect(c_blue)
            position_goal_x = int(x_blue + w_blue/2)
            position_goal_y = int(y_blue + h_blue/2)
            cv2.circle(frame, (position_goal_x, position_goal_y), 5, (0, 0, 255), -1)

            # Check if the rectangle is within the desiblue range
            #if min_length < w_blue < max_length and min_length < h_blue < max_length:
                # Draw a rectangle around the largest contour
            cv2.rectangle(frame, (x_blue, y_blue), (x_blue + w_blue, y_blue + h_blue), (0, 0, 255), 2)
            position_x = frame.shape[1]/2 - x_blue 
            position_y = frame.shape[0]/2 - y_blue - w_blue/2
            position_y_with_ML = predict(position_y)
            set_shot_sapma(position_y)
            
            #cv2.circle(frame, (position_x, position_y), 5, (0, 255, 0), -1)
            #print("rectangle is now on x: ", position_x)
            #print("rectangle is now on y: ", position_y)
            #print(frame.shape[0], frame.shape[1])
            if COLLECT_ORIGINAL_DATA == 1:
                if position_y < -5:
                    MOTOR_turn_left()
                    ready = 0
                elif position_y > 5:
                    MOTOR_turn_right()
                    ready = 0
                else:
                    set_last_goal_location_Y(position_y)
                    MOTOR_stop()
                    ready = 1
            elif COLLECT_ORIGINAL_DATA == 0:
                if -position_y_with_ML < -5:
                    MOTOR_turn_left()
                    ready = 0
                elif -position_y_with_ML > 5:
                    MOTOR_turn_right()
                    ready = 0
                else:
                    set_last_goal_location_Y(position_y)
                    MOTOR_stop()
                    ready = 1
            elif COLLECT_ORIGINAL_DATA == 2:
                if position_y+get_accuracy() < -5:
                    MOTOR_turn_left()
                    ready = 0
                elif position_y +get_accuracy() > 5:
                    MOTOR_turn_right()
                    ready = 0
                else:
                    set_last_goal_location_Y(position_y)
                    MOTOR_stop()
                    ready = 1
        else:
            MOTOR_turn_left()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

try:
        
    while True:
        print("Preparing")
        
        MOTOR_stop()
        for i in range(100):
            aim_the_goal()
        
        print("AIMED , SHOOTING IN 3")
        
        print("AIMED , SHOOTING IN 2")
        
        print("AIMED , SHOOTING IN 1")
        #prepare_and_shot()
        
      

        subprocess.run(cmd,shell = True)
        
        for i in range(100):
            image_process_is_goal()
        
        if(get_goal() == 1):
            set_goal(0)
            reset_all()
            print("SUUUUUUUUUUUUUUUUUU")
        else:
            print("NOT GOAL")

        print("SHOT MADE")

        
        sleep(1)
        
        #image_processing()

        # Check if the user pressed "q" to quit
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
        
except KeyboardInterrupt:
    print(" ")
    MOTOR_stop()



""" 
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
# Create a mask for the blue color
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue) 
"""
