from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util.log import LOG

import RPi.GPIO as GPIO
import threading
import time
import re

__author__ = 'dony71'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
#class GPIOSkill(MycroftSkill):
class Respeaker2MicGpioSkill(MycroftSkill):

    # The constructor of the skill, which calls Mycroft Skill's constructor
    def __init__(self):
        #super(GPIOSkill, self).__init__(name="GPIOSkill")
        super(Respeaker2MicGpioSkill, self).__init__(name="Respeaker2MicGpioSkill")
#        GPIO_STATE = {}    # This is an object of tracking GPIO
#        GPIO_ON = ()       # This maps functions to gpio activity 
        #self. blink_active = False
        #GPIO.on("Button",self.on_button_change)
        self.myKeywords = []

#    def on(key,function):
#        """Used to set the function for the GPIO interface
#           Args:
#           key(int or str): Used to identify the gpio to interface
#           function(function): The function for the gpioi"""
#        GPIO_ON[key]= function
#
#    def get(key):
#        """ Returns the value of the givien GPIO
#            Args:
#            key(int or str): Used to identify the gpio to interface"""
#        return GPIO_STATE[key]
#
#    def set(key,value):
#        """This function is used to set values for each of GPIO's Will also call
#           the GPIO's function if it exisits.
#           Args:
#           key(int or str): Used to identify the gpio to interface
#           value(int or str): The value to set the gpio to."""
#        GPIO_STATE[key] = value
#        if key in GPIO_ON:
#            GPIO_ON[key]()
#
#    def on_button_change(self):
#        status = self.get("Button")
#        self.speak("Button is %s" % status)
#
#    # This handels the button press and sets the stat
#    def ButtonHandeler(channel):
#        if GPIO.input(channel) == GPIO.HIGH:
#            self.speak("Button is Released")
#        else:
#            self.speak("Button is Pressed")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        #self.io_pins = [3, 5, 7, 29, 31, 26, 24, 21, 19, 23, 32, 33, 8, 10, 36, 11, 12, 35, 38, 40, 15, 16, 18, 22, 37, 13]
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(11,GPIO.IN)
        GPIO.add_event_detect(11,GPIO.BOTH,ButtonHandeler)
        self.blink_active = False
        self.on("Button",self.on_button_change)

        self.load_data_files(dirname(__file__))
        command_intent = IntentBuilder("GPIOIntent").\
            require("ItemKeyword").\
            optionally("ColorKeyword").\
            one_of("OnKeyword", "OffKeyword", "BlinkKeyword").build()

        self.register_intent(command_intent, self.handle_command_intent)

    def handle_command_intent(self, message):
        #str_limits = []
        #str_remainder = str(message.utterance_remainder())
        #if (str_remainder.find('for') != -1) or (str_remainder.find('four') != -1):
        #    str_limits = [4]
        #else:
        #    str_limits = re.findall('\d+', str_remainder)
        #
        #if str_limits:
        #    gpio_request = int(str_limits[0])
        #    if (gpio_request > 1) and (gpio_request < 28):
        #        pin_index = gpio_request - 2
        #        board_pin = self.io_pins[pin_index]
        #        LOG.info('The pin number requested was: ' + str(board_pin))
        #        if "OnKeyword" in message.data:
        #            self.gpio_on(board_pin, gpio_request)
        #        if "OffKeyword" in message.data:
        #            self.gpio_off(board_pin, gpio_request)
        #    else:
        #        self.speak_dialog("error", data={"result": str(gpio_request)})
        #else:
        #    self.speak('No GPIO Pin was specified')

        if message.data["ColorKeyword"].upper() == "RED":
            board_pin = 32
            gpio_request = 12
            LOG.info('The pin number requested was: ' + str(board_pin))
            if "OnKeyword" in message.data:
                self.gpio_on(board_pin, gpio_request)
            if "OffKeyword" in message.data:
                self.gpio_off(board_pin, gpio_request)
            if "BlinkKeyword" in message.data:
                if self.blink_active:
                    self.blink_active = False
                else:
                    self.blink_active = True                
                    self.gpio_blink(board_pin, gpio_request)
        elif message.data["ColorKeyword"].upper() == "GREEN":
            board_pin = 33
            gpio_request = 13
            LOG.info('The pin number requested was: ' + str(board_pin))
            if "OnKeyword" in message.data:
                self.gpio_on(board_pin, gpio_request)
            if "OffKeyword" in message.data:
                self.gpio_off(board_pin, gpio_request)
            if "BlinkKeyword" in message.data:
                if self.blink_active:
                    self.blink_active = False
                else:
                    self.blink_active = True
                    self.gpio_blink(board_pin, gpio_request)
        else:
            self.speak('No LED Color was specified')

    def ButtonHandeler(self, channel):
        button = GPIO.input(11)
        #if GPIO.input(channel) == GPIO.HIGH:
        if button:
            self.speak("Button is Released")
        else:
            self.speak("Button is Pressed")

    def gpio_on(self, board_number, gpio_request_number):
        self.blink_active = False
        GPIO.setup(board_number, GPIO.OUT, initial=0)
        GPIO.output(board_number, True)
        LOG.info('Turning On GPIO Number: ' + str(gpio_request_number))
        self.speak_dialog("on", data={"result": str(gpio_request_number)})

    def gpio_off(self, board_number, gpio_request_number):
        self.blink_active = False
        GPIO.setup(board_number, GPIO.OUT, initial=0)
        GPIO.output(board_number, False)
        LOG.info('Turning Off GPIO Number: ' + str(gpio_request_number))
        self.speak_dialog("off", data={"result": str(gpio_request_number)})

    def gpio_blink(self, board_number, gpio_request_number):
        GPIO.setup(board_number, GPIO.OUT, initial=0)
        if self.blink_active:
            threading.Timer(10, self.gpio_blink).start()
        if self.blink_active:
            GPIO.output(board_number, True)
            time.sleep(0.5)
            GPIO.output(board_number, False)
            time.sleep(0.5)
        LOG.info('Blinking GPIO Number: ' + str(gpio_request_number))
        self.speak_dialog("blink", data={"result": str(gpio_request_number)})

    def stop(self):
        self.blink_active = False
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    #return GPIOSkill()
    return Respeaker2MicGpioSkill()
