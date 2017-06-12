import RPi.GPIO as GPIO
import time


class LCD():
    __teller = 0
    def __init__(self, RS, RW, E, D0, D1, D2, D3, D4, D5, D6, D7):
        self.__RS = RS
        self.__RW = RW
        self.__E = E
        self.__D0 = D0
        self.__D1 = D1
        self.__D2 = D2
        self.__D3 = D3
        self.__D4 = D4
        self.__D5 = D5
        self.__D6 = D6
        self.__D7 = D7
        GPIO.setmode(GPIO.BCM)
        listGPIO = [RS, RW, E, D0, D1, D2, D3, D4, D5, D6, D7]
        for index in range(0, len(listGPIO)):
            GPIO.setup(listGPIO[index], GPIO.OUT)

    def __eHoogInstructie(self):
        GPIO.output(self.__E, GPIO.HIGH)
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)

    # E van hoog naar laag zetten bepaalt wanneer de LCD data verwerkt
    # lage RS is instructie hoge RS zijn characters doorsturen
    # RW is altijd op laag om data door te sturen als je wilt aflezen van de LCD dan plaats je dit op hoog
    def __eLaagInstructie(self):
        GPIO.output(self.__E, GPIO.LOW)
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)

    def __eHoogData(self):
        GPIO.output(self.__E, GPIO.HIGH)
        GPIO.output(self.__RS, GPIO.HIGH)
        GPIO.output(self.__RW, GPIO.LOW)

    def __eLaagData(self):  # E=0, RS=1, RW=0
        GPIO.output(self.__E, GPIO.LOW)
        GPIO.output(self.__RS, GPIO.HIGH)
        GPIO.output(self.__RW, GPIO.LOW)

    def __clearDisplay(self):
        self.__setGPIODataBits_instruction(0x01)
        # setGPIODataBits_instruction(0b000000001)
        time.sleep(0.005)

    def __displayOn(self):
        self.__setGPIODataBits_instruction(0x0F)
        # setGPIODataBits_instruction(0b000001111)
        time.sleep(0.005)

    def __setGPIODataBits_instruction(self, data):
        self.__eHoogInstructie()
        listGPIO = [self.__D7, self.__D6, self.__D5, self.__D4, self.__D3, self.__D2, self.__D1, self.__D0]
        filter = 0x80
        for bit in range(0, 4, 1):
            result = data & filter  # result is 0 of 128
            if result == 0:
                GPIO.output(listGPIO[bit], GPIO.LOW)
                filter = filter >> 1
            else:
                GPIO.output(listGPIO[bit], GPIO.HIGH)
                filter = filter >> 1
        self.__eLaagInstructie()
        time.sleep(0.005)

        filter = 0x08
        self.__eHoogInstructie()
        for bit in range(0, 4, 1):
            result = data & filter  # result is 0 of 128
            if result == 0:
                GPIO.output(listGPIO[bit], GPIO.LOW)
                filter = filter >> 1
            else:
                GPIO.output(listGPIO[bit], GPIO.HIGH)
                filter = filter >> 1
        self.__eLaagInstructie()
        time.sleep(0.005)

    def __setGPIODataBits_data(self, data):
        self.__eHoogData()
        listGPIO = [self.__D7, self.__D6, self.__D5, self.__D4, self.__D3, self.__D2, self.__D1, self.__D0]
        filter = 0x80
        for bit in range(0, 4, 1):
            result = data & filter  # result is 0 of 128
            if result == 0:
                GPIO.output(listGPIO[bit], GPIO.LOW)
                filter = filter >> 1
            else:
                GPIO.output(listGPIO[bit], GPIO.HIGH)
                filter = filter >> 1
        self.__eLaagData()
        time.sleep(0.005)

        filter = 0x08
        self.__eHoogData()
        for bit in range(0, 4, 1):
            result = data & filter  # result is 0 of 128
            if result == 0:
                GPIO.output(listGPIO[bit], GPIO.LOW)
                filter = filter >> 1
            else:
                GPIO.output(listGPIO[bit], GPIO.HIGH)
                filter = filter >> 1
        self.__eLaagData()
        time.sleep(0.005)

    def ShowText(self, text):
        # from 0 until 15 or from 64 until 79 (0x00 until 0x0f or from 0x40 until 0x4f)
        # db7: must be high
        # db6 - db0: ddram adres
        text = str(text)
        # text=text.decode()
        # print (text)
        # print(LCD.__teller)
        if text == "Speed: ":
            self.__setGPIODataBits_instruction(0xA8)

        if LCD.__teller == 2:
            # self.__setGPIODataBits_instruction(0b0000001101)
            self.__setGPIODataBits_instruction(0b10001010)

        elif LCD.__teller == 3:
            self.__setGPIODataBits_instruction(0b11000111)
            LCD.__teller=1

        for character in text:
            self.__setGPIODataBits_data(ord(character))
        LCD.__teller += 1

    def __function_set(self):
        self.__setGPIODataBits_instruction(0x28)
        # setGPIODataBits_instruction(0b000101000)
        time.sleep(0.005)
        print("function set executed")

    def __reset(self):
        time.sleep(0.005)
        # setGPIODataBits_instruction(0b00011)
        self.__setGPIODataBits_instruction(0x33)
        time.sleep(0.0015)

        self.__setGPIODataBits_instruction(0x32)
        # setGPIODataBits_instruction(0b00011)
        time.sleep(0.005)

        # self.__setGPIODataBits_instruction(0x30)
        # # self.__setGPIODataBits_instruction(0b00011)
        # time.sleep(0.005)
        # # -----------------------------#
        # self.__setGPIODataBits_instruction(0x20)
        # # self.__setGPIODataBits_instruction(0b00010)
        # time.sleep(0.00015)

        # setGPIODataBits_instruction(0b000101000)
        self.__setGPIODataBits_instruction(0x28)
        time.sleep(0.00015)
        self.__setGPIODataBits_instruction(0x08)
        # setGPIODataBits_instruction(0b000001000)
        time.sleep(0.00015)
        self.__setGPIODataBits_instruction(0x01)
        # setGPIODataBits_instruction(0b000000001)
        time.sleep(0.00015)

        self.__setGPIODataBits_instruction(0x06)
        # setGPIODataBits_instruction(0b000000110)
        time.sleep(0.00015)
        print("reset executed")

    def startDisplay(self):
        self.__reset()
        self.__function_set()
        self.__displayOn()
        self.__clearDisplay()
        self.__setGPIODataBits_instruction(0b00001100)




        # RS, RW, E, D0,D1,D2,D3, D4, D5, D6, D7

# lcd = LCD(17, 27, 22, 0, 0, 0, 0, 5, 6, 13, 19)
# lcd=LCD(26, 0, 19, 0,0,0,0, 22, 27, 17, 4)
# lcd.startDisplay()
# ip = lcd.getRaspberryIP()
# lcd.ShowText(ip)
# filenames=lcd.getFileName()
# lcd.ShowText(filenames[1])