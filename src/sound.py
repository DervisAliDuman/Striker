import pygame

pygame.init()
pygame.mixer.init()

def SOUND_goal():
	pygame.mixer.music.load("Sounds/suuu.mp3")
	pygame.mixer.music.play()

def SOUND_prep1():
	pygame.mixer.music.load("Sounds/1.mp3")
	pygame.mixer.music.play()
	
def SOUND_prep2():
	pygame.mixer.music.load("Sounds/2.mp3")
	pygame.mixer.music.play()

def SOUND_prep3():
	pygame.mixer.music.load("Sounds/3.mp3")
	pygame.mixer.music.play()

def SOUND_prep4():
	pygame.mixer.music.load("Sounds/4.mp3")
	pygame.mixer.music.play()
