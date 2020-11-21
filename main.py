#!/usr/bin/env python3

import sys
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

from inputpopup import InputPopup

class MainLayout(FloatLayout):

    timestring_w = StringProperty()
    timestring_s = StringProperty()
    timestring_r = StringProperty()
    pauzing = BooleanProperty(True)

    update_int = 0.05
    cutoff_time = 0.075

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.sets = 4
        self.secs_s = 450 #450 # 7.5 minutes
        self.init()

    def init(self):
        self.secs_w = self.secs_s * self.sets

        self.secs_sr = self.secs_s # remaining seconds
        self.secs_wr = self.secs_w

        self.direction = 1
        self.secs_rr = 0
        self.sound_bleep = SoundLoader.load('bleep.wav')
        self.sound_honk = SoundLoader.load('honk.wav')

        nowtime = datetime.datetime.now()
        self.delta_w = nowtime + datetime.timedelta(0, self.secs_w)
        self.delta_s = nowtime + datetime.timedelta(0, self.secs_s)
        self.delta_r = nowtime 
        self.button_l.background_color = (0,0,1,1)
        self.button_w.background_color = (1,1,1,1)
        self.button_s.background_color = (1,1,1,1)
        self.button_r.background_color = (0,1,0,1)  # start with green
        self.start()

    def start(self):
        Clock.schedule_interval(self.update, self.update_int)

    def stop(self):
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        nowtime = datetime.datetime.now()

        if self.pauzing:
            self.delta_w = nowtime + datetime.timedelta(0, self.secs_wr)
            self.delta_s = nowtime + datetime.timedelta(0, self.secs_sr)
            self.delta_r = nowtime + datetime.timedelta(0, self.secs_rr)
        else:
            self.secs_wr = round(self.delta_w.timestamp() - nowtime.timestamp(),12)
            self.secs_sr = round(self.delta_s.timestamp() - nowtime.timestamp(),12)
            if self.direction == 1:
                self.secs_rr = nowtime.timestamp() - self.delta_r.timestamp()
            else:
                self.secs_rr = self.delta_r.timestamp() - nowtime.timestamp()

        self.timestring_w = self.generate_timestring(self.secs_wr,0)
        self.timestring_s = self.generate_timestring(self.secs_sr,0)
        self.timestring_r = self.generate_timestring(self.secs_rr,1)

        if self.secs_wr < self.cutoff_time:
            self.timestring_r = self.generate_timestring(0,1)
            self.button_w.background_color = (1,0,0,1)
            self.button_s.background_color = (1,0,0,1)
            self.button_r.background_color = (1,0,0,1)
            self.sound_honk.play()
            self.sound_honk.play()
            self.stop()
            self.pauzing = True

        elif self.secs_sr < self.cutoff_time:
            self.timestring_r = self.generate_timestring(0,1)
            self.button_s.background_color = (1,0,0,1)
            self.button_r.background_color = (1,0,0,1)
            self.sound_honk.play()
            self.secs_sr = self.secs_sr + self.secs_s
            self.secs_rr = 0
            self.direction = 1
            self.delta_r = nowtime
            self.toggle_ws()

        elif self.secs_rr < 0:
            self.timestring_r = self.generate_timestring(0,1)
            self.button_r.background_color = (0,1,0,1)
            self.sound_bleep.play()
            self.secs_rr = 0
            self.direction = 1

    def toggle_r(self):
        if self.pauzing:
            self.toggle_ws()
        else:
            nowtime = datetime.datetime.now()
            if self.direction > 0:
                self.direction = -1
                self.delta_r = nowtime + datetime.timedelta(0, self.secs_rr)
                self.button_r.background_color = (0,0,1,1)

    def toggle_ws(self):
        nowtime = datetime.datetime.now()
        if self.pauzing and self.secs_wr < self.cutoff_time:
            self.init()
        elif self.pauzing:
            self.pauzing = False
            print("not pauzing")
            self.delta_w = nowtime + datetime.timedelta(0, self.secs_wr)
            self.delta_s = nowtime + datetime.timedelta(0, self.secs_sr)
            if self.direction > 0:
                self.delta_r = nowtime - datetime.timedelta(0, self.secs_rr)
            else:
                self.delta_r = nowtime + datetime.timedelta(0, self.secs_rr)
            self.button_s.background_color = (1,1,1,1)
            if self.direction > 0:
                self.button_r.background_color = (0,1,0,1)
            else:
                self.button_r.background_color = (0,0,1,1)
            self.start()
        else:
            self.pauzing = True
            print("pauzing now")
            #self.secs_wr = self.delta_w.timestamp() - nowtime.timestamp()
            if self.direction > 0:
                self.secs_rr = nowtime.timestamp() - self.delta_r.timestamp()
            else:
                self.secs_rr = self.delta_r.timestamp() - nowtime.timestamp()
            self.stop()

    def generate_timestring(self,seconds,digits):
        if digits == 0:
            minutes_str = "%02d" % (seconds // 60) 
            seconds_str = "%02d" % (round(seconds % 60) % 60)
        else:
            minutes_str = "%02d" % (seconds // 60)
            seconds_str = '{:04.1f}'.format(seconds % 60)
        timestring = "%s:%s" % (minutes_str, seconds_str)
        return timestring

    def configpopup(self):
        menu = InputPopup()
        menu.title = 'Set sets and seconds per set'
        menu.ids.input_sets.text = str(self.sets)
        menu.ids.input_secs.text = str(self.secs_s)
        menu.bind(on_ok=self.back_from_configpopup)
        menu.ids.input_secs.focus = True
        menu.open()

    def back_from_configpopup(self, ins):
        self.sets   = int(ins.ids.input_sets.text)
        self.secs_s = int(ins.ids.input_secs.text)
        self.init()


if __name__ == '__main__':

    class MainApp(App):
        def build(self):
            return MainLayout()

    MainApp().run()
