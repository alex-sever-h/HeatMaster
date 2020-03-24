import time
import RPi.GPIO as GPIO

from relay.initializer import Initialiser
from relay.controller import Controller

GPIO.setmode(GPIO.BOARD)


def main():
    li = Initialiser()
    lc = Controller(li.relays)

    #switch
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #RELAY
    GPIO.setup(29, GPIO.OUT)

    def handle_switch(pin):

        print ("Switch is ", GPIO.input(31))

        if GPIO.input(31):
            lc.turn_it_all_up()
            GPIO.output(29, 1)
        else:
            lc.turn_it_all_down()
            GPIO.output(29, 0)

    GPIO.add_event_detect(31, GPIO.BOTH, handle_switch)

    while(True):
        handle_switch(0);
        time.sleep(1)


if __name__ == "__main__":
    main()