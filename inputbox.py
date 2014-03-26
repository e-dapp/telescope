import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import sys

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return (event.key, event.unicode)
    else:
      pass

def display_box(screen, message):
  fontobject = pygame.font.SysFont("monospace",14)
  pygame.draw.rect(screen, (0,0,0),
                   (10,
                    (screen.get_height()) - 32,
                    (screen.get_width()) - 20, 24), 0)
  pygame.draw.rect(screen, (255,255,255),
                   (10,
                    (screen.get_height()) - 32,
                    (screen.get_width()) - 20, 24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                (20, (screen.get_height()) - 30))
  pygame.display.flip()

def ask(surface, question):
    "ask(question) -> answer"
    current_string = ""
    display_box(surface, question + ": " + current_string)
    while 1:
        (inkey, unichr) = get_key()

        if inkey == K_BACKSPACE:
            current_string = current_string[:-1]
        elif inkey == K_RETURN or inkey == K_KP_ENTER:
            break
        elif inkey == pygame.K_ESCAPE:
            terminate()
        else:
            current_string += unichr
 
        current_string = current_string[:50]
        display_box(surface, question + ": " + current_string)

    return current_string    

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name") + " was entered"
  pygame.quit()
  sys.exit()

if __name__ == '__main__':
  main()
