#!/usr/bin/env python
import RPi.GPIO as GPIO
import pygame
import time


FILENAME = 'mariachi.wav'


class TriggerPlayer(object):

    def __init__(self, filename, gpio_pin):
        # Setup player
        self.__gpio_pin = gpio_pin
        self.__playing = False
        # start mixer and load music
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN)
        GPIO.add_event_detect(gpio_pin, GPIO.BOTH)
        GPIO.add_event_callback(gpio_pin, self.update_state)
        self.update_state(gpio_pin)

    def is_playing(self):
        return self.__playing

    def play(self):
        self.__playing = True
        return pygame.mixer.music.play(-1)

    def stop(self):
        self.__playing = False
        return pygame.mixer.music.stop()

    def update_state(self, pin):
        if pin == self.__gpio_pin:
            time.sleep(1)
            input_ = GPIO.input(self.__gpio_pin)
            if not input_ and not self.is_playing():
                self.play()
            elif input_ and self.is_playing():
                self.stop()


if __name__ == '__main__':
    player = TriggerPlayer(FILENAME, 23)
    try:
        while True:
            GPIO.event_detected(23)
    except KeyboardInterrupt:
        GPIO.cleanup()
