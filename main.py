# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////
import os
import math
import sys
import time
import threading

os.environ["DISPLAY"] = ":0.0"

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *

rampStepper = DPiStepper()
rampStepper.setBoardNumber(0)
dpiComputer = DPiComputer()
dpiComputer.initialize()

# ////////////////////////////////////////////////////////////////
# //                     HARDWARE SETUP                         //
# ////////////////////////////////////////////////////////////////
"""Stepper Motor goes into MOTOR 0 )
    Limit Switch associated with Stepper Motor goes into HOME 0
    One Sensor goes into IN 0
    Another Sensor goes into IN 1
    Servo Motor associated with the Gate goes into SERVO 1
    Motor Controller for DC Motor associated with the Stairs goes into SERVO 0"""


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
DEBOUNCE = 0.1
INIT_RAMP_SPEED = 200 * 16
RAMP_LENGTH = 725
stairSpeed = 40

# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)



# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////
class MainScreen(Screen):

    staircaseSpeedText = '0'
    rampSpeed = INIT_RAMP_SPEED
    staircaseSpeed = stairSpeed

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def toggleGate(self):
        print("Gate Opening")
        i = 0
        servoNumber = 1
        for i in range(260):
            dpiComputer.writeServo(servoNumber, i)
            sleep(0.01)
        sleep(0.2)
        k = 0
        print("Gate Closing")
        for k in(260, 0, -1):
            dpiComputer.writeServo(servoNumber, k)
            sleep(0.01)


    def toggleStaircase(self):
        print("Stairs Initiated: Motor on")
        i = 0
        k = 0
        servoNumber = 0
        for i in range(90, 180):
            dpiComputer.writeServo(servoNumber, i)
            sleep(0.1)
        dpiComputer.writeServo(servoNumber, 90)
        print("Stairs are done: Motor off")

    def resetRamp(self):
        rampStepper.enableMotors(True)
        rampStepper.setSpeedInStepsPerSecond(0, INIT_RAMP_SPEED)
        rampStepper.moveToRelativePositionInSteps(0, 46600, False)


        
    def toggleRamp(self):
        print("Move ramp up and down here")
        bottom = self.isBallAtBottom()
        if(bottom):
            print("the ball is not at the bottom")
        else:
            print("the ball is at the bottom")
        if(bottom == False):
            print("Starting Ramp")
            rampStepper.enableMotors(True)
            rampStepper.moveToRelativePositionInSteps(0, -1 * 46600, True)

        print("Ball has reached the top: Resetting Ramp")
        self.resetRamp()


        
    def auto(self):
        print("Automated run through initiated:")
        self.toggleRamp()
        sleep(2)
        self.toggleStaircase()
        sleep(4)
        self.toggleGate()
        
    def setRampSpeed(self, speed):
        rampStepper.setSpeedInStepsPerSecond(0, self.ids.rampSpeed.value)
        
    def setStaircaseSpeed(self, speed):
        print("slkjdf")

    def initialize(self):
        print("Close gate, stop staircase and home ramp here")

    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE

    def isBallAtTop(self):
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        print("Top: " + str(value))
        return(value)


    def isBallAtBottom(self):
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)
        print("Bottom: " + str(value))
        return(value)
    
    def quit(self):
        print("Exit")
        MyApp().stop()

sm.add_widget(MainScreen(name = 'main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # Window.fullscreen = True
    # Window.maximize()
    MyApp().run()
