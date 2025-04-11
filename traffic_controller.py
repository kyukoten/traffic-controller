import time
from pyfirmata import Arduino, util, STRING_DATA
import serial

PORT = 'COM5'
LCD_ARDUINO_PORT = 'COM4'  # Port for the second Arduino
board = Arduino(PORT)

lcd_arduino = serial.Serial(LCD_ARDUINO_PORT, 9600)  # Serial for LCD Arduino

class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green


# TL for each lane
TL_lane_1 = TrafficLight(13, 12, 11)
TL_lane_2 = TrafficLight(10, 9, 8)
TL_lane_3 = TrafficLight(7, 6, 5)
TL_lane_4 = TrafficLight(4, 3, 2)

TL = [TL_lane_1, TL_lane_2, TL_lane_3, TL_lane_4]


##### Functions #####

def ledCheck():
    """Sequentially turns LEDs on and off for testing."""
    for i in range(13, 1, -1):
        board.digital[i].write(1)
        time.sleep(0.025)
        board.digital[i].write(0)
    for i in range(2, 14):
        board.digital[i].write(1)
        time.sleep(0.025)
        board.digital[i].write(0)


def shutDownAll():
    """Turns off all LEDs."""
    for i in range(2, 14):
        board.digital[i].write(0)


def lcd(text):
    """Sends text to the LCD via the second Arduino."""
    lcd_arduino.write((text + '\n').encode())  # Send text followed by newline


def activateLane(laneIndex, gst, starvation):
    # Update LCD
    lcd(f"Lane: {laneIndex+1} ({gst}s)")
    lcd(f"S: {starvation[0]} {starvation[1]} {starvation[2]} {starvation[3]}")

    # Control the traffic lights
    for i in range(4):
        if i != laneIndex:
            board.digital[TL[i].yellow].write(0)
            board.digital[TL[i].green].write(0)
            board.digital[TL[i].red].write(1)
        else:
            if gst < 4:
                board.digital[TL[i].red].write(0)
                board.digital[TL[i].green].write(0)
                board.digital[TL[i].yellow].write(1)
            else:
                board.digital[TL[i].red].write(0)
                board.digital[TL[i].yellow].write(0)
                board.digital[TL[i].green].write(1)


##### Main Program #####

ledCheck()  # Test all LEDs at the beginning
