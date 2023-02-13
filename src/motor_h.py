import RPi.GPIO as GPIO
from time import sleep

#################MOTOR CONFIG
#20 21 sol motor geri - ileri
#16 26 sag motor geri- ileri

motor_power = 20

GPIO.setmode(GPIO.BCM)
LEFT_FRONT_pin = 21
LEFT_FRONT_frequency = 1000
LEFT_FRONT_duty_cycle = 0
GPIO.setup(LEFT_FRONT_pin, GPIO.OUT)
LEFT_FRONT_pwm = GPIO.PWM(LEFT_FRONT_pin, LEFT_FRONT_frequency)
LEFT_FRONT_pwm.start(LEFT_FRONT_duty_cycle)

##########

LEFT_BACK_pin = 20
LEFT_BACK_frequency = 1000
LEFT_BACK_duty_cycle = 0
GPIO.setup(LEFT_BACK_pin, GPIO.OUT)
LEFT_BACK_pwm = GPIO.PWM(LEFT_BACK_pin, LEFT_BACK_frequency)
LEFT_BACK_pwm.start(LEFT_BACK_duty_cycle)

##########
RIGHT_FRONT_pin = 26
RIGHT_FRONT_frequency = 1000
RIGHT_FRONT_duty_cycle = 0
GPIO.setup(RIGHT_FRONT_pin, GPIO.OUT)
RIGHT_FRONT_pwm= GPIO.PWM(RIGHT_FRONT_pin, RIGHT_FRONT_frequency)

RIGHT_FRONT_pwm.start(RIGHT_FRONT_duty_cycle)

##########

RIGHT_BACK_pin = 16
RIGHT_BACK_frequency = 1000
RIGHT_BACK_duty_cycle = 0
GPIO.setup(RIGHT_BACK_pin, GPIO.OUT)
RIGHT_BACK_pwm= GPIO.PWM(RIGHT_BACK_pin, RIGHT_BACK_frequency)
RIGHT_BACK_pwm.start(RIGHT_BACK_duty_cycle)

##########

def MOTOR_turn_left():
    
    #RIGHT_FRONT_pwm.ChangeDutyCycle(50)
    #sleep(0.05)
    RIGHT_FRONT_pwm.ChangeDutyCycle(motor_power+2)
    sleep(0.02)
    RIGHT_BACK_pwm.ChangeDutyCycle(0)
    sleep(0.015)
    RIGHT_FRONT_pwm.ChangeDutyCycle(0)



def MOTOR_turn_right():
    
    #LEFT_FRONT_pwm.ChangeDutyCycle(50)
    #sleep(0.05)
    LEFT_FRONT_pwm.ChangeDutyCycle(motor_power)
    sleep(0.02)
    LEFT_BACK_pwm.ChangeDutyCycle(motor_power)
    sleep(0.015)
    LEFT_FRONT_pwm.ChangeDutyCycle(0)
    LEFT_BACK_pwm.ChangeDutyCycle(0)

    


def MOTOR_stop():
    LEFT_FRONT_pwm.ChangeDutyCycle(0)
    RIGHT_FRONT_pwm.ChangeDutyCycle(0)
    
    LEFT_BACK_pwm.ChangeDutyCycle(0)
    RIGHT_BACK_pwm.ChangeDutyCycle(0)
    
    sleep(0.01)



###################### MOTOR DONE







