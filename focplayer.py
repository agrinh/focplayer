#!/usr/bin/env python
import RPi.GPIO as GPIO
import pygame
import time
import zerorpc


FILENAME = 'mariachi.wav'


class PlayerRPC(object):

    def __init__(self, filename, gpio_pin):
        # ZeroRPC state updating client
        self.__client = zerorpc.Client("tcp://127.0.0.1:4343")
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
        self.__disabled = GPIO.input(gpio_pin)

    def is_playing(self):
        return self.__playing

    def play(self):
        if not self.__disabled:
            pygame.mixer.music.play(-1)
            self.__playing = True
            return True

    def stop(self):
        pygame.mixer.music.stop()
        self.__playing = False

    def disable(self):
        self.stop()
        self.__disabled = True

    def enable(self):
        self.__disabled = False

    def update_state(self, pin):
        if pin == self.__gpio_pin:
            time.sleep(1)
            input = GPIO.input(self.__gpio_pin)
            if input:
                self.enable()
            elif not self.is_playing():
                self.enable()
                self.play()
	        self.__client.isPlaying(False)
            else:
                self.disable()
                self.__client.isPlaying(False)


if __name__ == '__main__':
    server = zerorpc.Server(PlayerRPC(FILENAME, 23))
    server.bind("tcp://127.0.0.1:4242")
    server.run()
