#!/usr'bin/python
import serial
import sys
import time
import curses
from curses.textpad import Textbox, rectangle


port = ''
dec = ''
ra = ''
current_info = [';']

def open_port():
    port_name = '/dev/ttyUSB0'
    port_name = get_param("Set port to open [leave blank for '/dev/ttyUSB0']")
    if port_name == '':
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout = 0.1)
    else:
        ser = serial.Serial(port_name, 19200, timeout = 0.1)
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
	if current_info == [';']:
		pass
	else:
		new_c_i = []
		for i in range(len(current_info)):
			x = manage_string(current_info[i])
			new_c_i.append(x)
		for i in range(len(current_info)):
			screen.addstr(i + 15, 35, new_c_i[i])

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

def get_param(prompt):
	win = curses.newwin(5, 60, 5, 5)
	win.border(0)
	win.addstr(1,2,prompt)
	return win.getstr(3,2,55).decode(encoding="utf-8")

help_list = ['o - Open Port', 'e - Set Alignment Side', 
             'r - Target Right Ascension', 'd - Target Declination', 
             's - Set Target From RA/DE', 'a - Align from Target', 
             'g - GoTo Target', 'u - Update Current Info',
	     '------------','q - Exit']

current_info_titles = ['Alignment State:', 'Side of the Sky:',
                       'Current Right Ascension:', 'Current Declination:',
                       'Target Right Ascension:', 'Target Declination:']

screen = curses.initscr()
screen.timeout(50) #stops getch() from blocking
start_time = time.time()

good = True
while good: 
	screen.clear()
	screen.border(0)
	screen.addstr(2, 2, "UTSC Python Telescope control system")
	for i in range(len(help_list)):
		screen.addstr(i + 3, 4, help_list[i])
	for i in range(len(current_info_titles)):
		screen.addstr(i + 15, 4, current_info_titles[i])
	current_info_box()
	current_time = time.time()
	if port != '':
		if current_time - start_time > 2:
			current_info = get_status()
	screen.refresh()
	key = screen.getch()
        if key == 27 or key == ord('q'): #27=ESC
            good = False
        if key == ord('o'):
            port = open_port()
        if key == ord('d'):
            dec = get_param("Set target Declination [signed 6 digit]")
        if key == ord('r'):
            ra = get_param("Set target Right Ascension [unsigned 6 digit]")
        if key == ord('s'):
            assign_target(dec, ra)
        if key == ord('e'):
            direction = get_param("Set alignment side")
            alignment_side(direction)
        if key == ord('a'):
            align_from_target()
        if key == ord('g'):
            goto_target()
        if key == ord('u'):
            current_info = get_status()

curses.endwin()
