import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, BlinkDataPoint, MeditationDataPoint, AttentionDataPoint, EEGPowersDataPoint, PoorSignalLevelDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
from  mindwavemobile import MindwavePacketPayloadParser 
import textwrap
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


attention_treshold = 60

lst = []
eyeblinks = 0
armed = False
left = False
right = False
forward = False
print("Searching for Mindwave device")

in1 = 26
in2 = 19
in3 = 13
in4 = 6


TRIG = 23                                  #Associate pin 23 to TRIG
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN) 

def turn_on(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.OUT)
    GPIO.output(gpio_pin, True)

def turn_off(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.OUT)
    GPIO.output(gpio_pin, False)



def move_forward():
    turn_on(in1)
    turn_off(in2)
    turn_on(in3)
    turn_off(in4)

def stop():
    turn_off(in1)
    turn_off(in2)
    turn_off(in3)
    turn_off(in4)

def turn_left():
    turn_on(in1)
    turn_off(in2)
    turn_off(in3)
    turn_off(in4)
    
def turn_right():
    turn_off(in1)
    turn_off(in2)
    turn_on(in3)
    turn_off(in4)



if _name_ == '_main_':
    mindwaveDataPointReader = MindwaveDataPointReader("00:81:F9:29:B3:EE")#"00:81:F9:29:B3:EE"
    mindwaveDataPointReader.start()
    if (mindwaveDataPointReader.isConnected()):
        while(True):
            GPIO.setup(21, GPIO.OUT)
            GPIO.output(21, True)
            for i in range(0, 800):
                dataPoint = mindwaveDataPointReader.readNextDataPoint()
                #if (not dataPoint._class_ is RawDataPoint):
                    #print(dataPoint)
                if(len(lst) > 100):
                #print("Difference:",max(lst)-min(lst))
                    if(700<max(lst)-min(lst)<1500):
                        eyeblinks+=1
                    lst[:] =[]        
                if dataPoint._class.name_=='RawDataPoint':
                    lst.append(dataPoint.rawValue)
            print("Eyeblinks:",eyeblinks)
            GPIO.setup(21, GPIO.OUT)
            GPIO.output(21, False)
            attentaion_list = []
            for i in range (1000):
                dataPoint = mindwaveDataPointReader.readNextDataPoint()
                if dataPoint._class.name_ == 'AttentionDataPoint':
                    attentaion_list.append(dataPoint.attentionValue)
            attention_level = sum(attentaion_list)/len(attentaion_list)
            print("attention_level",attention_level)
                
            if dataPoint._class.name_ == 'PoorSignalLevelDataPoint':
                print(dataPoint)
                poor_signal_level = dataPoint.amountOfNoise
#             if (not dataPoint._class_ is EEGPowersDataPoint and not dataPoint._class_ is RawDataPoint):
#                 print(dataPoint)
            
            if eyeblinks >3:
                if(armed):
                    print("Vehicle is disarmed")
                    armed = False
                    movingClockWise = False
                    left = False
                    right = False
                    forward = False
                    GPIO.setup(20, GPIO.OUT)
                    GPIO.output(20, False)
                else:
                    print("Vehicle is armed")
                    armed = True
                    GPIO.setup(20, GPIO.OUT)
                    GPIO.output(20, True)
            
            if armed:
                if attention_level > attention_treshold:
                    print("Moving Forward")
                    left = False
                    forward = True
                    right = False
                else:
                    print("Not Moving Forward")
                    left = False
                    forward = False
                    right = False
                if eyeblinks == 2:
                    left = True
                    forward = False
                    right = False
                elif eyeblinks == 3:
                    left = False
                    right = True
                    forward = False
                
            
            eyeblinks = 0
            if forward:
                loop_start = time.time()
                loop_end = time.time()
                while(loop_end - loop_start < 2):
                    loop_end = time.time()
                    GPIO.output(TRIG, False)
                    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
                    time.sleep(0.00001)                      #Delay of 0.00001 seconds
                    GPIO.output(TRIG, False)
                    while GPIO.input(ECHO)==0:
                        pulse_start = time.time()
                    while GPIO.input(ECHO)==1:
                        pulse_end = time.time()
                    pulse_duration = pulse_end - pulse_start
                    distance = pulse_duration * 17150
                    distance = round(distance, 2)
                    if distance < 30:
                        stop()
                    else:
                        move_forward()
            else:
                stop()
            if left:
                stop()
                turn_left()
                time.sleep(1)
                left = False
                stop()
            if right:
                stop()
                turn_right()
                time.sleep(1)
                right = False
                stop()
                
                
                
                
    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
