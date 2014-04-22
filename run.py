#!/usr'bin/python
import serial
import sys
import os
import time
import curses
from curses.textpad import Textbox, rectangle


port = None
dec = ''
ra = ''
current_info = [';']
print os.uname()[0]

def open_port():
    if os.uname()[0]=="Darwin":
         default_port_name = '/dev/tty.usbserial'
    else:
         default_port_name = '/dev/ttyUSB0'
    port_name = get_param("Set port to open [leave blank for '"+default_port_name+"']")
    try:
         if port_name == '':
              port_name = default_port_name
         ser = serial.Serial(port_name, 19200, timeout = 0.1)
         return ser
    except:
         return None

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
     if port is not None:
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
     else:
          nc = "Not connected."
          return [nc,nc,nc,nc,nc,nc]

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
	return win.getstr(3,2,55)

help_list = ['o - Open Port', 'e - Set Alignment Side', 
             'r - Target Right Ascension', 'd - Target Declination', 
             'a - Align from Target', 
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
	if port is not None:
		if current_time - start_time > 2:
			current_info = get_status()
	screen.refresh()
	key = screen.getch()
        if key == 27 or key == ord('q'): #27=ESC
            good = False
        if key == ord('o'):
            port = open_port()

        if key == ord('d'):
            dec = get_param("Set target Declination [+dd:mm:ss]")
	    if port is not None:
		 port.write('!CStd' + d + ';')

        if key == ord('r'):
            ra = get_param("Set target Right Ascension [hh:mm:dd]")
	    if port is not None:
                 port.write('!CStr' + r + ';')

        if key == ord('e'):
            direction = get_param("Set alignment side [West/East]")
            if port is not None:
                 port.write('!ASas' + direction + ';')

        if key == ord('a'):
            if port is not None:
                 port.write('!AFrn;')

        if key == ord('g'):
            if port is not None:
                 port.write('!GTrd;')

        if key == ord('u'):
            current_info = get_status()

curses.endwin()
