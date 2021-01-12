import tkinter as tki

class BoggleGUI:

    def __init__(self, boggle_model):
        self._boggle_model = boggle_model
        self._root = tki.Tk()

        self._boggle_display = tki.Frame(width=300, height=300)
        self.pack()

        # self._clock_display = tki.Label(font=("Courier", 30), width=11)
        # self._clock_display.pack()
        # self._clock_display.bind("<Button-1>", self._label_clicked)
        # self._button = tki.Button(text="mode", font=("Courier", 30))
        # self._button.pack()

    def pack(self):
        self._boggle_display.pack()
    # def _label_clicked(self, event):
    #     print(event.x, event.y)
    #     print(dir(event))
    #
    # def _animate(self):
    #     self._clock_display["text"] = self._boggle_model.get_time_str()
    #     self._root.after(10, self._animate)

    def run(self):
        # self._animate()
        # self._button["command"] = self._boggle_model.switch_mode
        self._root.mainloop()
