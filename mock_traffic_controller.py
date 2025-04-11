# mock_traffic_controller.py

import time

class MockArduino:
    def __init__(self, port):
        print(f"Connected to mock Arduino on {port}")
        self.digital = [MockPin() for _ in range(14)]

    def send_sysex(self, string_data, two_byte_iter):
        print(f"Mock LCD: {''.join(chr(b) for b in two_byte_iter)}")

class MockPin:
    def write(self, value):
        if value == 1:
            print("LED ON")
        else:
            print("LED OFF")

def util_str_to_two_byte_iter(text):
    return [ord(c) for c in text]

board = MockArduino('COM5')  # Simulate the Arduino being connected

def activateLane(laneIndex, gst, starvation):
    print(f"Activating lane {laneIndex} with GST {gst}s and starvation levels {starvation}")
    time.sleep(0.1)  # Simulate a small delay

def shutDownAll():
    print("Shutting down all LEDs")

