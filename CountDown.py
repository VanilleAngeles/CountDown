#!/usr/bin/env python3
# coding: utf-8
# References:
#------ CountDown --> https://www.darkartistry.com/2019/12/simple-python-3-threaded-timer-in-gtk3/
#------ Sound     --> https://stackoverflow.com/questions/260738/play-audio-with-python
import gi, time, threading, os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango
from playsound import playsound

class MyApplication(Gtk.Window):
	def __init__(self):
#------	acces to CSS file
		style_provider = Gtk.CssProvider()
		style_provider.load_from_path('CountDown.css')
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
#------ Init Buttons state
		self.CountDownStatus = "Stopped"
#------ Window created
		Gtk.Window.__init__(self, title="Timer")
#------ VBOX
		self.vbox = Gtk.VBox()
#------ GRID
		self.grid = Gtk.Grid()
		self.grid.set_hexpand(True)
		self.grid.set_column_spacing(10)
#------ SpinButtons
		self.labelStart = Gtk.Label()
		self.labelStart.set_text('Start in')
		self.grid.attach(self.labelStart, 0, 0, 1, 1)
		adjuststart = Gtk.Adjustment(value=0, lower=0, upper=10, step_increment=1, page_increment=1, page_size=0)
		self.Start = Gtk.SpinButton(adjustment=adjuststart)
		self.grid.attach(self.Start, 0, 1, 1, 1)

		self.labelFrequency = Gtk.Label()
		self.labelFrequency.set_text('Frequency')
		self.grid.attach(self.labelFrequency, 1, 0, 1, 1)
		adjustFrequency = Gtk.Adjustment(value=1, lower=1, upper=10, step_increment=1, page_increment=1, page_size=0)
		self.Frequency = Gtk.SpinButton(adjustment=adjustFrequency)
		self.grid.attach(self.Frequency, 1, 1, 1, 1)

		self.labelNumber = Gtk.Label()
		self.labelNumber.set_text('Number')
		self.grid.attach(self.labelNumber, 2, 0, 1, 1)
		adjustNumber = Gtk.Adjustment(value=5, lower=1, upper=60, step_increment=1, page_increment=5, page_size=0)
		self.Number = Gtk.SpinButton(adjustment=adjustNumber)
		self.grid.attach(self.Number, 2, 1, 1, 1)

		self.labelIteration = Gtk.Label()
		self.labelIteration.set_text('Iteration')
		self.grid.attach(self.labelIteration, 3, 0, 1, 1)
		adjustIteration = Gtk.Adjustment(value=1, lower=1, upper=5, step_increment=1, page_increment=1, page_size=0)
		self.Iteration = Gtk.SpinButton(adjustment=adjustIteration)
		self.grid.attach(self.Iteration, 3, 1, 1, 1)
#------ CountDown		
		self.label=Gtk.Label()
		self.label.set_name('CountDown')
		self.label.set_text('00')
		self.grid.attach(self.label, 0, 2, 4, 1)
#------ Start Button
		self.startbutton=Gtk.Button.new_with_label("⏯")
		self.startbutton.set_name('Stopped')
		self.startbutton.connect("clicked",self.start_clicked)
		self.grid.attach(self.startbutton, 1, 3, 1, 1)
#------ Stop Button
		self.stopbutton=Gtk.Button.new_with_label("⏹")
		self.stopbutton.set_name('Stopped')
		self.stopbutton.connect("clicked",self.stop_clicked)
		self.grid.attach(self.stopbutton, 2, 3, 1, 1)
#------ Generate Grid
		self.vbox.pack_end(self.grid,True,True,5)
		self.add(self.vbox)
		
#------ Start
	def start_clicked(self, niet):
		if self.CountDownStatus == 'Stopped':
				self.CountDownStatus = 'Started'
				self.startbutton.set_name(self.CountDownStatus)
				self.timer = threading.Thread(target=self.CountDown)
				self.event = threading.Event()
				self.timer.daemon=True
				self.timer.start()
		elif self.CountDownStatus == 'Started':
				self.CountDownStatus = 'Paused'
				self.startbutton.set_name(self.CountDownStatus)
		elif self.CountDownStatus == 'Paused':
				self.CountDownStatus = 'Started'
				self.startbutton.set_name(self.CountDownStatus)
#------ Only frome Python version 3.10
#		match self.CountDownStatus:
#			case 'Stopped':
#				self.CountDownStatus = 'Started'
#				self.startbutton.set_name(self.CountDownStatus)
#				self.timer = threading.Thread(target=self.CountDown)
#				self.event = threading.Event()
#				self.timer.daemon=True
#				self.timer.start()
#			case 'Started':
#				self.CountDownStatus = 'Paused'
#				self.startbutton.set_name(self.CountDownStatus)
#			case 'Paused':
#				self.CountDownStatus = 'Started'
#				self.startbutton.set_name(self.CountDownStatus)
		
#------ Stop
	def stop_clicked(self, niet):
		self.CountDownStatus = "Stopped"
		self.startbutton.set_name(self.CountDownStatus)
		self.label.set_text('0')

#------	Loop
	def CountDown(self):
		I = self.Iteration.get_value_as_int()
		S = self.Start.get_value_as_int()
		while S:
			if self.CountDownStatus == 'Stopped': break
			timer=str(f'{S*-1:0>2d}')
			self.label.set_text(timer)
			time.sleep(0.75)
			self.label.set_text('')
			time.sleep(0.25)
			S -= 1
		time.sleep(S)
		while I:
			if self.CountDownStatus == 'Stopped': break
			N = self.Number.get_value_as_int()
			F=self.Frequency.get_value_as_int()
			while N+1:
				if self.CountDownStatus == 'Stopped': break
				if self.CountDownStatus == 'Started':
					timer=str(f'{N:0>2d}')
					self.label.set_text(timer)
					playsound('CountDown200m.mp3')
					if N == 0:
						self.startbutton.set_name(self.CountDownStatus)
#						os.system('paplay CountDown.wav')
						playsound('CountDown1s.mp3')
					else:
						time.sleep(F-0.3)
					N -= 1
			if F > 1:
				time.sleep(F-1)
			I -= 1
		self.CountDownStatus = 'Stopped'
		self.startbutton.set_name(self.CountDownStatus)

	def main(self):
		Gtk.main()


#----- Init
win = MyApplication()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
