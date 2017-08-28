import time

import RPi.GPIO as GPIO

# Define GPIO to LCD mapping
__LCD_RS = 21
__LCD_E = 20
__LCD_D4 = 26
__LCD_D5 = 16
__LCD_D6 = 19
__LCD_D7 = 13

# Define some device constants
__LCD_WIDTH = 20  # Maximum characters per line
__LCD_CHR = True
__LCD_CMD = False

__LCD_LINE_ADDRESSES_LIST = [0x80, 0xC0, 0x94, 0xD4]

# Timing constants
__E_PULSE = 0.0005
__E_DELAY = 0.0005

LINE_1 = 0
LINE_2 = 1
LINE_3 = 2
LINE_4 = 3

STYLE_ALIGN_LEFT = 1
STYLE_ALIGN_CENTER = 2
STYLE_ALIGN_RIGHT = 3


def display(text, line, style):
    __lcd_string(text, __LCD_LINE_ADDRESSES_LIST[line], style)


def __lcd_init():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setup(__LCD_E, GPIO.OUT)  # E
    GPIO.setup(__LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(__LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(__LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(__LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(__LCD_D7, GPIO.OUT)  # DB7

    __lcd_byte(0x33, __LCD_CMD)  # 110011 Initialise
    __lcd_byte(0x32, __LCD_CMD)  # 110010 Initialise
    __lcd_byte(0x06, __LCD_CMD)  # 000110 Cursor move direction
    __lcd_byte(0x0C, __LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    __lcd_byte(0x28, __LCD_CMD)  # 101000 Data length, number of lines, font size
    __lcd_byte(0x01, __LCD_CMD)  # 000001 Clear display
    time.sleep(__E_DELAY)


def __lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(__LCD_RS, mode)  # RS

    # High bits
    GPIO.output(__LCD_D4, False)
    GPIO.output(__LCD_D5, False)
    GPIO.output(__LCD_D6, False)
    GPIO.output(__LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(__LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(__LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(__LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(__LCD_D7, True)

    __lcd_toggle_enable()

    # Low bits
    GPIO.output(__LCD_D4, False)
    GPIO.output(__LCD_D5, False)
    GPIO.output(__LCD_D6, False)
    GPIO.output(__LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(__LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(__LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(__LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(__LCD_D7, True)

    __lcd_toggle_enable()


def __lcd_toggle_enable():
    # Toggle enable
    time.sleep(__E_DELAY)
    GPIO.output(__LCD_E, True)
    time.sleep(__E_PULSE)
    GPIO.output(__LCD_E, False)
    time.sleep(__E_DELAY)


def __lcd_string(message, line, style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified

    if style == 1:
        message = message.ljust(__LCD_WIDTH, " ")
    elif style == 2:
        message = message.center(__LCD_WIDTH, " ")
    elif style == 3:
        message = message.rjust(__LCD_WIDTH, " ")

    __lcd_byte(line, __LCD_CMD)

    for i in range(__LCD_WIDTH):
        __lcd_byte(ord(message[i]), __LCD_CHR)

        # def lcd_backlight(flag):
        # Toggle backlight on-off-on
        # GPIO.output(LED_ON, flag)


# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         __lcd_byte(0x01, LCD_CMD)
#         __lcd_string("Goodbye!", LCD_LINE_1_ADDRESS, 2)
#         GPIO.cleanup()

__lcd_init()
