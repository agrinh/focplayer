#!/usr/bin/env python
import pygame
import zerorpc


FILENAME = 'mariachi.wav'


class PlayerRPC(object):

    def __init__(self, filename):
        self.__playing = False
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

    def is_playing(self):
        return self.__playing

    def play(self):
        pygame.mixer.music.play(loops=-1)
        self.__playing = True
        return True

    def stop(self):
        pygame.mixer.music.stop()
        self.__playing = False


if __name__ == '__main__':
    server = zerorpc.Server(PlayerRPC(FILENAME))
    server.bind("tcp://127.0.0.1:4242")
    server.run()
