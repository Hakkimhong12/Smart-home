import speech_recognition as sr
from pyfirmata import Arduino, SERVO, OUTPUT
from time import sleep

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

port = 'COM5'
pin = 10
led1_pin = 7
led2_pin = 6
fan_pin1 = 2
fan_pin2 = 3
fan_pin3 = 4

board = Arduino(port)

board.digital[pin].mode = SERVO
board.digital[led2_pin].mode = OUTPUT
board.digital[led1_pin].mode = OUTPUT
board.digital[fan_pin1].mode = OUTPUT
board.digital[fan_pin2].mode = OUTPUT
board.digital[fan_pin3].mode = OUTPUT

def rotate(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

def control_led(pin, state):
    board.digital[pin].write(state)
    sleep(0.015)

def control_fan(pin,state):
    board.digital[pin].write(state)
    sleep(0.015)
with mic as source:
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print("Heard command:", command)

            if command == 'Open Door':
                control_led(led2_pin, 0)
                control_led(led1_pin,0)
                print('door is  on')
                for i in range(0,180,5):
                    rotate(pin, i)
            elif command == 'close door':
                control_led(led2_pin, 0)
                control_led(led1_pin, 0)
                for i in range(180, 0, -5):
                    rotate(pin, i)

            elif command == 'LED on':
                print("LEDs are on")
                control_led(led1_pin, 1)
                control_led(led2_pin, 1)

            elif command == 'LED off':
                print("LEDs are off")
                control_led(led1_pin, 0)
                control_led(led2_pin, 0)

            elif command == 'fan on':
                control_fan(fan_pin2,1)
                control_fan(fan_pin3,0)
                control_fan(fan_pin1,1)
            elif command == 'fan off':

                control_fan(fan_pin3,0)
                control_fan(fan_pin2,0)
                control_fan(fan_pin1,0)
            elif command == 'stop':
                break

            # elif command == 'all one':
            #     for i in range(0,180,5):
            #         rotate(pin, i)
            #         sleep(1)
            #
            #     control_led(led1_pin,1)
            #     control_fan(fan_pin2,1)
            #     control_fan(fan_pin3,1)
            #
            #     control_led(led1_pin,0)
            #     control_fan(fan_pin1,0)

            else:
                print("Unknown command:", command)
                
        except sr.UnknownValueError:
            print("Unknown command:")
        except sr.RequestError as e:
            print("Error occurred during speech recognition:", str(e))