class Hallsensor():


    def __init__(self):
        import RPi.GPIO as GPIO
        import time
        from lcd import LCD
        GPIO.setmode(GPIO.BCM)
        self.__pulse = 0
        self.__distance = 0.00
        self.__rpm = 0.00
        self.__speed = 0.00
        self.__wheel_c = 0.15708
        self.__multiplier = 0
        self.__hall = 21
        self.__elapse = 0.00
        self.__start = time.time()
        GPIO.setup(self.__hall, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.__hall, GPIO.FALLING, callback=self.get_pulse, bouncetime=20)

    def get_pulse(self):
        # global elapse, distance, start, pulse, speed, rpm, multiplier
        import time
        cycle = 0
        self.__pulse += 1
        cycle += 1
        if self.__pulse > 0:
            self.__elapse = time.time() - self.__start
            self.__pulse -= 1
        if cycle > 0:
            self.__distance += self.__wheel_c
            cycle -= 1

        self.__multiplier = 3600 / self.__elapse
        self.__speed = (self.__wheel_c * self.__multiplier) / 1000
        self.__rpm = 1 / self.__elapse * 60
        # speed = 2 * 3.14 * 2.5 * rpm * (60 / 1000)
        self.__start = time.time()
        return self.__speed,self.__distance
