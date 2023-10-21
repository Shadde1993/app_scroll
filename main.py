from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.lang import Builder
import random

layout = GridLayout(cols=1, size_hint_y=None)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
for i in range(1000):
    btn = Button(size_hint_y=None, background_color = "%06x" % random.randint(0, 0xFFFFFF))
    layout.add_widget(btn)
    
root = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
root.add_widget(layout)

runTouchApp(root)


    
    