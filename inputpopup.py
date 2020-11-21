from kivy.properties import StringProperty
from os.path import join, dirname
from kivy.lang import Builder
from kivy.uix.popup import Popup

class InputPopup(Popup):
    title =  StringProperty('Label Text')
    hint_text_secs = StringProperty('Hint Text')
    hint_text_sets = StringProperty('Hint Text Sets')
    info_sets = StringProperty()
    info_secs = StringProperty()
    ok_text = StringProperty('OK')
    cancel_text = StringProperty('Cancel')
	
    __events__ = ('on_ok', 'on_cancel')
    
    def __init__(self):
        super().__init__()
        #self.size_hint = [.9, .3]

    def open(self):
        super().open()

    def ok(self):
        self.dispatch('on_ok')
	
    def cancel(self):
        self.dispatch('on_cancel')
	
    def on_ok(self):
        print(self.ids.input_sets.text)
        self.info_sets = self.ids.input_sets.text
        self.info_secs = self.ids.input_secs.text
        self.dismiss()
	
    def on_cancel(self):
        self.dismiss()
