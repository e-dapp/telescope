import serial
import sys
import pygame
from pygame.locals import *
import inputbox

port = ''
dec = ''
ra = ''
clock = pygame.time.Clock()


def open_port():
    port_name = '/dev/ttyUSB0'
    port_name = inputbox.ask(screen, 
                             "Set port to open [leave blank for '/dev/ttyUSB0']")
    if port_name == '':
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout = 0.1)
    else:
        ser = serial.Serial(port_name, 19200, timeout = 1)
    return ser

def check_align():
    port.write('!AGas;')

def set_target():
    dec = set_dec()
    ra = set_ra()
    assign_target(dec, ra)

def set_dec():
    dec = str(raw_input('Set target Declination [form: +00:00:00]: '))
    return dec

def set_ra():
    ra = str(raw_input('Set target Right Ascension [form: 00:00:00]: '))
    return ra

def assign_target(d, r):
    port.write('!CStd' + d + ';')
    port.write('!CStr' + r + ';')

def alignment_side(direction):
    port.write('!ASas' + direction + ';')

def align_from_target():
    port.write('!AFrn;')

def goto_target():
    port.write('!GTrd;')

def help_box():
    h_box_place = (screen.get_width() - 250, 10, 
                      240, 15 + len(help_list)*20)
    
    fontobject = pygame.font.SysFont("monospace", 14)
    pygame.draw.rect(screen, white,
                     h_box_place,
                     1)
    
    for i in range(len(help_list)):
        screen.blit(fontobject.render(help_list[i], 1, (255,255,255)),
                        (h_box_place[0] + 10,
                         h_box_place[1] + 5 + i*20))

def current_info_box():
    box_place = (10, 10, screen.get_width() - 270, 300)
    
    fontobject = pygame.font.SysFont("monospace", 14)
    
    pygame.draw.rect(screen, black,
                         box_place,
                         0)
    pygame.draw.rect(screen, white,
                             box_place,
                             1)
    new_c_i = []
    
    screen.blit(fontobject.render('Current Information, [press u to update]',
                                  1,(255,255,255)),
                (box_place[0] + 10,
                 box_place[1] + 5))    
    
    for i in range(len(current_info)):
        x = manage_string(current_info[i])
        new_c_i.append(x)
    
    for i in range(len(current_info_titles)):
        screen.blit(fontobject.render(current_info_titles[i], 1,(255,255,255)),
                    (box_place[0] + 10,
                     box_place[1] + 40 + i*20))
    
    for i in range(len(current_info)):
        screen.blit(fontobject.render(new_c_i[i], 1, (255,255,255)), 
                    (box_place[0] + 300,
                     box_place[1] + 40 + i*20))

def get_status():
    port.readline()
    port.write('!AGas;')
    a = port.readline()
    port.write('!AGai;')
    b = port.readline()
    port.write('!CGra;')
    c = port.readline()
    port.write('!CGde;')
    d = port.readline()
    port.write('!CGtr;')
    e = port.readline()
    port.write('!CGtd;')
    f = port.readline()
    
    #return str(port.readline())
    return [a, b, c, d, e, f]

def manage_string(string):
    new_string = ''
    for i in string:
        if i != ';':
            new_string += i
        else:
            break
    
    return new_string


pygame.init()
size = (width, height) = (800,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("testing")
myfont = pygame.font.SysFont("monospace", 16)
black = (0, 0, 0)
white = (255, 255, 255)

good = True
status_delay = 1000
time_tracker = 0

help_list = ['o - Open Port', 'e - Set Alignment Side', 
             'r - Target Right Ascension', 'd - Target Declination', 
             's - Set Target From RA/DE', 'a - Align from Target', 
             'g - GoTo Target', 'u - Update Current Info']

current_info_titles = ['Alignment State:', 'Side of the Sky:',
                       'Current Right Ascension:', 'Current Declination:',
                       'Target Right Ascension:', 'Target Declination:']

current_info = [';']

while good: 
    screen.fill(black)
    
    help_box()
    current_info_box()
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_ESCAPE:
                good = False
            if event.key == pygame.K_o:
                port = open_port()
            if event.key == pygame.K_d:
                dec = inputbox.ask(screen, 
                                   "Set target Declination [signed 6 digit]")
            if event.key == pygame.K_r:
                ra = inputbox.ask(screen, 
                                  "Set target Right Ascension [unsigned 6 digit]")
            if event.key == pygame.K_s:
                assign_target(dec, ra)
            if event.key == pygame.K_e:
                direction = inputbox.ask(screen, 
                                         "Set alignment side")
                alignment_side(direction)
            if event.key == pygame.K_a:
                align_from_target()
            if event.key == pygame.K_g:
                goto_target()
            if event.key == pygame.K_u:
                current_info = get_status()
    pygame.display.flip()

pygame.quit()