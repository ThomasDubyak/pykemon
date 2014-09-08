import pygame

file = "intro.ogg"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
  
while pygame.mixer.music.get_busy():
  pygame.time.Clock().tick(10)
  
