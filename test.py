import time
from pyfirmata import Arduino

# Initialize board
PORT = 'COM5'
board = Arduino(PORT)

# LCD pin mapping
RS = 8
E = 9
D4 = 4
D5 = 5
D6 = 6
D7 = 7

# Pin setup
lcd_pins = [RS, E, D4, D5, D6, D7]
for pin in lcd_pins:
    board.digital[pin].mode = 1  # Set pins to OUTPUT mode


# Function to send a nibble (4 bits) to the LCD
def send_nibble(data, is_command):
    board.digital[RS].write(0 if is_command else 1)  # Command or data mode
    board.digital[D4].write((data >> 0) & 1)
    board.digital[D5].write((data >> 1) & 1)
    board.digital[D6].write((data >> 2) & 1)
    board.digital[D7].write((data >> 3) & 1)
    board.digital[E].write(1)  # Pulse Enable pin
    time.sleep(0.001)
    board.digital[E].write(0)


# Function to send a byte (8 bits) to the LCD
def send_byte(data, is_command):
    send_nibble(data >> 4, is_command)  # Send higher nibble
    send_nibble(data & 0x0F, is_command)  # Send lower nibble
    time.sleep(0.002)


# Function to initialize the LCD
def lcd_init():
    send_nibble(0x03, True)  # Initialization sequence
    time.sleep(0.005)
    send_nibble(0x03, True)
    time.sleep(0.005)
    send_nibble(0x03, True)
    time.sleep(0.005)
    send_nibble(0x02, True)  # Set 4-bit mode

    send_byte(0x28, True)  # Function set: 4-bit, 2 lines, 5x8 dots
    send_byte(0x0C, True)  # Display ON, Cursor OFF, Blink OFF
    send_byte(0x06, True)  # Entry mode: Move cursor right
    send_byte(0x01, True)  # Clear display
    time.sleep(0.005)


# Function to print text on the LCD
def lcd_print(text):
    for char in text:
        send_byte(ord(char), False)


# Example usage
lcd_init()
lcd_print("text")
