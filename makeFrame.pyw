"""
Create a window bar with buttons that launch apps, folders and files,
using a button press. The items can be preselected and added
to the bar.

Drag the startUpLauncher.bat file to the start up
folder (C:\Windows\System32\GroupPolicy\Machine\Scripts\Startup).

"""

import os
import tkinter.simpledialog
import tkinter.messagebox
import tkinter.filedialog
from tkinter import *


my_directory = os.curdir


class MakeFrame(Frame):

    def __init__(self):
        self.root = Tk()
        self.root.title("Quick Launch")
        self.root.iconbitmap('small.ico')
        self.buttons = []
        self.frame = Frame(self.root)
        self.get_rid = []

        self.frame.pack(side=BOTTOM, expand=YES, fill=BOTH)

        count = self.structure()
        self.structure_count = count.__iter__()

        if 'files_and_folders.txt' in os.listdir('{}'.format(my_directory)):
            with open('{}\\files_and_folders.txt'.format(my_directory), 'r') as file:
                self.button_info = file.readlines()
            self.create_saved_buttons()

    def make_window(self):
        """
        Top-level window containing all buttons.
        """
        add_directory = Button(self.root, text='Add Folder', command=self.save_button_file)
        add_app = Button(self.root, text='Add App', command=self.save_button_app)
        delete_button = Button(self.root, text='Remove Button', command=self.remove_button)

        add_directory.pack(side=LEFT, expand=YES, fill=BOTH)
        add_app.pack(side=LEFT, expand=YES, fill=BOTH)
        delete_button.pack(side=LEFT, expand=YES, fill=BOTH)

    def run(self):
        self.make_window()
        self.root.mainloop()

    def save_button_file(self):
        """
        Save folder to be opened with button press.
        """

        folder_path = tkinter.filedialog.askdirectory(initialdir=r'C:\Users\user\Documents')
        if folder_path:
            button_name = tkinter.simpledialog.askstring(title='Button Name', prompt='Please Enter Name')
            self.save_items(folder_path, button_name)
            position = self.structure_count.__next__()

            press = Button(self.frame, text=button_name, command=lambda: self.button_action(folder_path))
            self.buttons.append(press)
            press.grid(row=position[0], column=position[1])

    def save_button_app(self):
        """
        Save application tobe opened with button press.
        """
        folder_path = tkinter.filedialog.askopenfilename(initialdir=r'C:\Users\user\Documents')
        if folder_path:
            button_name = tkinter.simpledialog.askstring(title='Button Name', prompt='Please Enter Name')
            if not button_name:
                return
            self.save_items(folder_path, button_name)
            position = self.structure_count.__next__()

            press = Button(self.frame, text=button_name, command=lambda: self.button_action(folder_path))
            self.buttons.append(press)
            press.grid(row=position[0], column=position[1])

    def save_items(self, item, button_name):
        """
        Save folders and files
        :param item: folder to be saved
        :param button_name: name of button
        """

        if 'files_and_folders.txt' not in os.listdir('{}'.format(my_directory)):
            with open('{}\\files_and_folders.txt'.format(my_directory), 'w') as file:
                file.writelines(f'{item}---{button_name}\n')
        else:
            with open('{}\\files_and_folders.txt'.format(my_directory), 'a+') as file:
                file.writelines(f'{item}---{button_name}\n')

            with open('{}\\files_and_folders.txt'.format(my_directory), 'r') as file:
                self.button_info = file.readlines()

    def remove_button(self):
        """
        Removes buttons and links from window.
        """
        top_level = Toplevel(self.root)

        if not self.button_info:
            Label(top_level, text='NO buttons added')
            return

        frame = Frame(top_level)
        top_buttons = []
        count = self.structure()
        shape = count.__iter__()
        top_level.bind('<Destroy>', self.frame_bind)
        top_level.grab_set()

        for button_location, x in enumerate(self.button_info):

            names = x.split('---')
            name = names[1].replace('\n', '')
            press = Button(frame, text=name,
                           command=lambda button_location=button_location: self.remove(button_location, top_buttons))
            press.config(bg='black', fg='red')
            place = shape.__next__()
            press.grid(row=place[0], column=place[1])
            top_buttons.append(press)
        frame.pack()

    def frame_bind(self, fra):
        # rewrite all the main folder buttons
        # Rewrite the save text with all buttons

        with open('{}\\files_and_folders.txt'.format(my_directory), 'w') as file:
            for (num, x) in enumerate(self.button_info):
                if num not in self.get_rid:
                    file.writelines(x)

        with open('{}\\files_and_folders.txt'.format(my_directory), 'r') as file:
            self.button_info = file.readlines()

        for x in self.buttons:
            x.grid_forget()
        self.buttons = []
        self.get_rid = []

        count = self.structure()
        self.structure_count = count.__iter__()
        self.create_saved_buttons()

    def remove(self, position, top_buttons):
        decision = tkinter.messagebox.askyesno('Remove Button', 'Do You Want To Remove Button?')
        if not decision:
            return
        self.get_rid.append(position)
        top_buttons[position].grid_forget()

    def create_saved_buttons(self):
        """
        Read from list from text file the names of buttons to be created.
        """

        for x in self.button_info:
            names = x.split('---')
            name = names[1].replace('\n', '')
            address = names[0]

            press = self.button_ref(name, address)
            placement = self.structure_count.__next__()
            press.grid(row=placement[0], column=placement[1], sticky=NSEW)

            self.frame.rowconfigure(placement[0], weight=1)
            self.frame.columnconfigure(placement[1], weight=1)

    def button_ref(self, text, location):
        """
        This creates buttons from given inputs
        :param text: button name
        :param location: folder or app to be run
        :return: reference to button
        """

        press = Button(self.frame, text=text,
                       command=lambda: self.button_action(location))
        self.buttons.append(press)
        return press

    def button_action(self, location):
        """
        run the folder or app
        :param location: directory.
        """
        os.popen(f'start "" "{location}"')

    def structure(self):
        """generator that shapes frame with buttons"""
        for x in range(100000):
            for y in range(10):
                yield (x,y)


if __name__ == "__main__":
    done = MakeFrame()
    done.run()
    print(sys.exc_info())
else:
    done = MakeFrame()
    done.run()










