import cv2
import numpy as np
from time import sleep
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from sound import *
import os
from regression import *

# Set up the webcam
cap = cv2.VideoCapture(1)
goal = 0
found = 0
first_status = 0
first_size = 0
current_dir = os.getcwd()
files = os.listdir(current_dir)
video_counter = 0
max_video_counter = 0
last_ball_location_Y = 0
last_goal_location_Y = 0
write_status = 0
globalsayac = 0
shot_sapma = 0

ball_is_middle = 0
status_position_ball = 0
accuracy = -20
increase_rate = 4

# 1 for increase, -1 for decrease
def set_accuracy(val):
    global accuracy
    global increase_rate
    if val == 1:
        accuracy += increase_rate
    elif val == 0:
        accuracy -= increase_rate

def get_accuracy():
    global accuracy
    return accuracy

for i in files:
    if 'DATA_VID/test' in i:
        i = i.split('-')
        i = i[-1].split('.')
        video_counter = int(i[0]) + 1
        if video_counter > max_video_counter:
            max_video_counter = video_counter
            
writer = cv2.VideoWriter(f'DATA_VID/test-{max_video_counter}.avi', VideoWriter_fourcc(*'MP42'), 25.0, (640,480))

    
def get_optimal_shot():
    optimal = 0
    return optimal

def train_machine(result):
    return result

#lower_blue = np.array([65, 201, 60]) //BEST
#upper_blue = np.array([144,255,136])

#lower_blue = np.array([65, 155, 60])
#upper_blue = np.array([144,255,136]) //lab

lower_blue = np.array([58, 105, 133])
upper_blue = np.array([135,255,230])

#lower_blue = np.array([83, 88, 64])
#upper_blue = np.array([115,206,168])

#lower_red = np.array([160,83,82])
#upper_red = np.array([180,255,206])

#lower_red = np.array([101,0,0]) //BEST
#upper_red = np.array([180,255,255])

#lower_red = np.array([121,46,0])
#upper_red = np.array([180,143,98])

lower_red = np.array([121,76,70])
upper_red = np.array([180,255,221])

# Set the minimum and maximum length of rectangle
min_length = 10
max_length = 200


def is_goal(x_blue, y_blue, w_blue, h_blue, center_x_red, center_y_red):
    # Check if the center of the red ball is inside the blue rectangle
    if x_blue < center_x_red < x_blue + w_blue and y_blue < center_y_red < y_blue + h_blue:
        set_goal(1)
        return "Goal!"
    else:
        dist_x = abs(center_x_red - x_blue + w_blue/2)
        dist_y = abs(center_y_red - y_blue + w_blue/2)

        return "Not a goal. Distance in x:", dist_x, "Distance in y:", dist_y

def image_process_is_goal():
    global globalsayac
    global first_status
    global first_size
    global last_ball_location_Y
    global last_goal_location_Y
    global write_status
    global shot_sapma
    global ball_is_middle
    global status_position_ball 
    global accuracy 
    global increase_rate

    status2 = 3
    
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the blue mask
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   
    if len(contours_blue) > 0:
        c_blue = max(contours_blue, key=cv2.contourArea)
        global x_blue, y_blue, w_blue, h_blue
        x_blue, y_blue, w_blue, h_blue = 0, 0, 0, 0
        
        x_blue,y_blue,w_blue,h_blue = cv2.boundingRect(c_blue)
        position_goal_x = int(x_blue + w_blue/2)
        position_goal_y = int(y_blue + h_blue/2)
        cv2.circle(frame, (position_goal_x, position_goal_y), 5, (0, 0, 255), -1)
        status1 = 1
        if first_status == 0:
            first_status = 1
            first_size = w_blue*h_blue
            
        #if min_length < w_blue < max_length and min_length < h_blue < max_length:

        cv2.rectangle(frame, (x_blue, y_blue), (x_blue + w_blue, y_blue + h_blue), (0, 0, 255), 2)
            
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours_red) > 0:
            global x_red, y_red, w_red, h_red
            x_red, y_red, w_red, h_red = 0, 0, 0, 0
            c_red = max(contours_red, key=cv2.contourArea)
            x_red,y_red,w_red,h_red = cv2.boundingRect(c_red)
            position_ball_x = int(x_red + w_red/2)
            position_ball_y = int(y_red + h_red/2)
            status2 = 1
            if(status_position_ball == 0){
                if (frame.shape[0]/2 - int(y_red + h_red/2)) > 0:
                    set_accuracy(-1)
                else
                    set_accuracy(1)

                status_position_ball = 1
            }

            oran = (w_red/w_blue)*33
            if x_blue + oran < position_ball_x < x_blue + w_blue - oran and y_blue + oran < position_ball_y < y_blue + h_blue - oran:
                global goal
                last_ball_location_Y = position_ball_y
                cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 255, 0), 2)
                goal = 1
                SOUND_goal()
                #print(f'{w_blue} w kale {h_blue} h kale {w_red} w top {h_red} h top')
        else:
            status2 = 0
    else:
        status1 = 0
        
    if first_status == 1 and  first_size > w_blue*h_blue + first_size*0.10 and write_status == 0 and status2 == 1:
        frame = cv2.putText(frame, f'{(y_blue + h_blue/2) -(last_ball_location_Y)}', (0,400), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 0, 0), 2, cv2.LINE_AA)        
        position_y = frame.shape[0]/2 - y_blue - w_blue/2
        append_data([[shot_sapma, last_goal_location_Y -(frame.shape[0]/2 - last_ball_location_Y)]])
        cv2.imwrite(f"DATA_IMG/frame{globalsayac}.jpg", frame)
        

        #append_data(position_y_with_ML, )
        globalsayac += 1
        write_status = 1
        
    #prepare_and_shot()
        
    writer.write(frame)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(30)

def set_goal(val):
    global goal
    goal = val

def get_goal():
    global goal
    return goal
    
def set_last_goal_location_Y(val):
    global last_goal_location_Y
    last_goal_location_Y = val

def get_last_goal_location_Y():
    global last_goal_location_Y
    return last_goal_location_Y
    


def set_shot_sapma(val):
    global shot_sapma
    shot_sapma = val

def get_shot_sapma():
    global shot_sapma
    return shot_sapma

def reset_all():
    global goal
    global found
    global first_status
    global first_size
    global video_counter
    global max_video_counter
    global last_ball_location_Y
    global last_goal_location_Y
    global write_status
    global status_position_ball

    status_position_ball = 0
    goal = 0
    found = 0
    first_status = 0
    first_size = 0
    video_counter = 0
    max_video_counter = 0
    last_ball_location_Y = 0
    last_goal_location_Y = 0
    write_status = 0
"""

try: 
    while 1 :
        for i in range(100):
            image_process_is_goal()
            
        if goal == 1:
            print("SUUUUUUUUUUUUUUUUUU")
            goal = 0
            sleep(2)
            reset_all()
        else:
            print("NOOOOOOOOOOOOOO")

except KeyboardInterrupt:
    print(" ")

"""
