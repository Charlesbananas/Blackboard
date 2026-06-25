import pynput.mouse as mouse
import pynput.keyboard as keyboard

class Inputs():
    def __init__(self):
        self.m1_press = False
        self.m2_press = False
        self.handle_inputs()
        pass

    def handle_inputs(self):
        with mouse.Listener(
            on_move=self.on_move
        ) as listener:
            listener.join()
        pass

    def on_move(self,x,y):
        print("cursor at screen pos:{0}".format((x,y)))

    def on_click(self):
        pass

    def on_scroll(self):
        pass

    def set_states(self):
        pass

    def is_pressed(self,which):
        if which == "m1":
            return self.m1_press
        else:
            return self.m2_press
