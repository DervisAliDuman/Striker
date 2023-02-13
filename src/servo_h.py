from gpiozero import Servo
from time import sleep
import cv2
import numpy as np
from sound import *

#################SERVO CONFIG
sleep_time = 0.5

SERVO1 = Servo(27)
SERVO2 = Servo(22)
SERVO3 = Servo(23)
SERVO4 = Servo(24)

powerset = 1

def get_angle(ang):
    if ang == 0:
        return -1
    return 2 * (ang/180) -1

def get_max_angle():
     return 1

def get_min_angle():
     return -1

SERVO1_max_1 = -1
SERVO1_middle = 0
SERVO1_max_2 = 1

SERVO2_max = get_angle(60)
SERVO2_min = get_angle(10) 

SERVO3_max = get_angle(40)
SERVO3_min = get_angle(0)

SERVO4_max = 1
SERVO4_min = -1

def SERVO1_load_the_ball():
    SERVO1.value = SERVO1_max_1
    sleep(sleep_time)
    SERVO1.value = SERVO1_max_2
    sleep(sleep_time)
    SERVO1.value = SERVO1_middle
    sleep(sleep_time)

def SERVO2_3_pull_trigger(num):
    if(num == 1):
        SERVO2.value = SERVO2_max
    elif(num == 2):
        SERVO3.value = SERVO3_max
    sleep(0.1)
    

def SERVO2_3_set_trigger(num):
    if(num == 1):
        SERVO2.value = SERVO2_min
    elif(num == 2):
        SERVO3.value = SERVO3_min
    sleep(sleep_time)

def SERVO4_pull_string():
    SERVO4.value = SERVO4_min
    sleep(sleep_time)

def SERVO4_release_string():
    SERVO4.value = SERVO4_max
    sleep(sleep_time)
        
def SERVO_ALL_reset():
    SERVO2.value =  get_angle(40)
    SERVO3.value =  get_angle(40)
    SERVO4.value =  get_angle(180)
    sleep(0.2)



def prepare_and_shot():
    #sleep
    #optimal = get_optimal_shot()
    
    SERVO1_load_the_ball()
    
    SERVO4_pull_string()
    SERVO2_3_set_trigger(powerset)
    SOUND_prep4()
    SERVO4_release_string()
    
    SERVO2_3_pull_trigger(powerset)

prepare_and_shot()

"""
try:
	while True:
		prepare_and_shot()
except KeyboardInterrupt:
	print("Program stopped")
"""
