from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
import random


class FullScreenColor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = Window.height

        random_color = "#%06x" % random.randint(0, 0xFFFFFF)
        self.canvas.before.clear()
        with self.canvas.before:
            self.bg_color = Color(*get_color_from_hex(random_color))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Update label size and position dynamically
        font_size = max(10, int(Window.width * 0.05))  # Ensure the font size isn't too small
        self.text_label = Label(
            text="Nothing to see",
            color=(0, 0, 0, 1),
            font_size=f"{font_size}sp",
            size_hint=(None, None),
            size=(Window.width * 0.8, Window.height * 0.1),
            pos=(Window.width / 2 - Window.width * 0.8 / 2, Window.height / 2 - Window.height * 0.1 / 2)
        )
        self.add_widget(self.text_label)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        label_width = Window.width * 0.8
        label_height = Window.height * 0.1
        self.text_label.pos = (self.pos[0] + Window.width / 2 - label_width / 2,
                               self.pos[1] + Window.height / 2 - label_height / 2)
        # Dynamically adjust font size based on window size
        self.text_label.font_size = max(10, int(Window.width * 0.05))


class ScrollDetoxApp(App):
    def build(self):
        # Full screen setup
        Window.size = (Window.width, Window.height)
        Window.borderless = True
        Window.fullscreen = True

        root = FloatLayout()
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=Window.height * 1000)
        layout.bind(minimum_height=layout.setter('height'))

        # Add random color screens
        for _ in range(1000):
            layout.add_widget(FullScreenColor())

        scroll_view.add_widget(layout)
        root.add_widget(scroll_view)

        # Counter label in top-right corner
        counter_width = Window.width * 0.5
        counter_height = Window.height * 0.05
        self.counter_label = Label(
            text="Scrolls: 0",
            size_hint=(None, None),
            size=(counter_width, counter_height),
            pos=(Window.width - counter_width - 10, Window.height - counter_height - 10),
            color=(0, 0, 0, 1),
            font_size=f"{int(Window.width * 0.04)}sp"
        )
        root.add_widget(self.counter_label)

        # Bind scrolling to update counter
        scroll_view.bind(scroll_y=self.update_counter)
        self.last_swipe_position = 0
        self.swipe_count = 0

        return root

    def update_counter(self, scroll_view, scroll_y):
        current_position = int(scroll_view.scroll_y * 1000)
        if current_position != self.last_swipe_position:
            self.last_swipe_position = current_position
            self.swipe_count += 1
            self.counter_label.text = f"Scrolls: {self.swipe_count}"


if __name__ == '__main__':
    ScrollDetoxApp().run()
