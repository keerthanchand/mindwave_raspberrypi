import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, BlinkDataPoint, MeditationDataPoint, AttentionDataPoint, EEGPowersDataPoint, PoorSignalLevelDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
from  mindwavemobile import MindwavePacketPayloadParser 
import textwrap
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


lst = []
eyeblinks = 0
armed = False
movingClockWise = False
print("Searching for Mindwave device")



def get_eye_blinks():
    eyeblinks = 0
    
    return eyeblinks



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
            
#             if eyeblinks >3:
#                 if(armed):
#                     print("Vehicle is disarmed")
#                     armed = Falset
#                     GPIO.setup(16, GPIO.OUT)
#                     GPIO.output(16, False)
#                 else:
#                     print("Vehicle is armed")
#                     armed = True
#                     GPIO.setup(16, GPIO.OUT)
#                     GPIO.output(16, True)
#             
#             if armed:
#                 if movingClockWise and eyeblinks == 2:
#                     print("Stopped Moving clockwise")
#                     movingClockWise = False
#                     GPIO.setup(21, GPIO.OUT)
#                     GPIO.output(21, False)
#                 elif not(movingClockWise) and eyeblinks == 2:
#                     print("Moving clockwise")
#                     movingClockWise = True
#                     GPIO.setup(21, GPIO.OUT)
#                     GPIO.output(21, True)
#             
            eyeblinks = 0
                
    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
