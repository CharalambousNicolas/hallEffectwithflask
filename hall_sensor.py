import RPi.GPIO as GPIO
import time
from lcd import LCD

mylcd = LCD(13, 26, 5, 0, 0, 0, 0, 16, 12, 19, 6)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pulse = 0
distance = 0.00
rpm = 0.00
speed = 0.00
wheel_c = 0.15708
multiplier = 0
hall = 21
elapse = 0.00

start = time.time()

GPIO.setup(hall, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_pulse(number):
    global elapse, distance, start, pulse, speed, rpm, multiplier
    cycle = 0
    pulse += 1
    cycle += 1
    if pulse > 0:
        elapse = time.time() - start
        pulse -= 1
    if cycle > 0:
        distance += wheel_c
        cycle -= 1

    multiplier = 3600 / elapse

    speed = (wheel_c * multiplier) / 1000
    rpm = 1 / elapse * 60
    # speed = 2 * 3.14 * 2.5 * rpm * (60 / 1000)
    start = time.time()


# ------------------------------------lcd-----------------------------------------------------#
# RS, RW, E, D0, D1, D2, D3, D4, D5, D6, D7):
mylcd.startDisplay()
mylcd.ShowText("Distance: ")
mylcd.ShowText("Speed: ")

# ----------------------------------------------------------------------------------------------------------------------#


try:
    print('Initializing Speedometer! Starting in 3 seconds!')
    time.sleep(1)
    print('3 seconds...')
    time.sleep(1)
    print('2 seconds...')
    time.sleep(1)
    print('1 seconds...')
    time.sleep(1)
    GPIO.add_event_detect(hall, GPIO.FALLING, callback=get_pulse, bouncetime=20)
    while True:
        speed = round(speed, 2)
        mylcd.ShowText(distance)
        mylcd.ShowText(speed)
        print('rpm:{0:.2f} speed:{1:.2f} distance:{2} elapse:{3:.4f} multiplier:{4:.4f}'.format(rpm, speed, distance,
                                                                                                elapse, multiplier))
        time.sleep(0.1)
except KeyboardInterrupt:
    print('You have pressed Ctrl+C! How dare you stopped this beautiful thing?!')
    GPIO.cleanup()
