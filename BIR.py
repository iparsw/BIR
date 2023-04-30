import os
import re
from PIL import Image
import argparse
import customtkinter as ctk
import tkinter as tk


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def calc_new_height(width, height, new_width):
    return round(new_width * height / width)


def resize(root, file, new_width, new_img_name, keep_aspect_ratio, new_height):
    original_img_path = os.path.join(root, file)
    new_img_path = os.path.join(root, new_img_name)

    try:
        new_width = int(new_width)
    except:
        raise TypeError(
            f'-w, --new-width or NEW_WIDTH must be a number. Sent "{NEW_WIDTH}".')

    pillow_img = Image.open(original_img_path)
    width, height = pillow_img.size

    if keep_aspect_ratio:
        new_height = calc_new_height(width, height, new_width)
    else:
        new_height = new_height

    new_img = pillow_img.resize((new_width, new_height), Image.LANCZOS)

    try:
        new_img.save(
            new_img_path,
            optimize=True,
            quality=100,
            subsampling=0,
            exif=pillow_img.info.get('exif')
        )
    except:
        try:
            new_img.save(
                new_img_path,
                optimize=True,
                subsampling=0,
                quality=100,
            )
        except:
            raise RuntimeError(f'Could not convert "{original_img_path}".')

    print(f'Saved at {new_img_path}')


def is_image(extension):
    extension_lowercase = extension.lower()
    return bool(re.search(r"^\.(jpe?g|png)$", extension_lowercase))


def files_checks(root, file, height, width, keep_aspect_ratio):
    filename, extension = os.path.splitext(file)

    if not is_image(extension):
        return

    flag = '_CONVERTED'

    if flag in file:
        return

    new_img_name = filename + flag + extension

    resize(root=root, file=file, new_width=width, new_img_name=new_img_name, new_height=height,
           keep_aspect_ratio=keep_aspect_ratio)


def files_loop(root, files, height, width, keep_aspect_ratio):
    for file in files:
        files_checks(root, file, height=height, width=width, keep_aspect_ratio=keep_aspect_ratio)


def main_function(root_folder, height, width, keep_aspect_ratio):
    for root, dirs, files in os.walk(root_folder):
        files_loop(root, files, height=height, width=width, keep_aspect_ratio=keep_aspect_ratio)


def main_gui():
    base = ctk.CTk()
    base.title("BIM")
    base.geometry("400x550")
    base.resizable(False, False)

    mode_var = ctk.StringVar(value="Change aspect ratio")
    height_entry_visibility = ctk.StringVar(value="normal")

    def option_menu_callback(choice):
        if choice == "keep aspect ratio":
            width_entry.configure(state="disable")
        if choice == "Change aspect ratio":
            width_entry.configure(state="normal")

    def start_bim():
        mode = mode_var.get()
        keep_aspect_ratio = True
        height = 0
        width = int(width_entry.get())
        path = path_entry.get()
        if mode == "Change aspect ratio":
            keep_aspect_ratio = False
            height = int(height_entry.get())
        main_function(root_folder=path,
                      height=height,
                      width=width,
                      keep_aspect_ratio=keep_aspect_ratio)
        return

    label_font = ctk.CTkFont(family="sans", size=80)
    entry_font = ctk.CTkFont(family="sans", size=20)
    entry_font2 = ctk.CTkFont(family="sans", size=14)

    frame = ctk.CTkFrame(master=base)
    frame.pack(padx=45, pady=45)
    """Label"""
    label = ctk.CTkLabel(master=frame,
                         text="BIR",
                         fg_color=("black", "gray75"),
                         text_color=("white", "black"),
                         corner_radius=8,
                         font=label_font)

    label.pack(padx=20, pady=50)
    """Path entry"""
    path_entry = ctk.CTkEntry(master=frame,
                              placeholder_text="Base directory",
                              width=250,
                              height=40,
                              border_width=2,
                              corner_radius=10,
                              font=entry_font)

    path_entry.pack(padx=20, pady=20)
    """Option menu"""
    mode_option_box = ctk.CTkOptionMenu(master=frame,
                                        values=["Keep aspect ratio",
                                                "Change aspect ratio"],
                                        variable=mode_var,
                                        command=option_menu_callback)

    mode_option_box.pack(padx=10, pady=10)
    """Width entry"""
    width_entry = ctk.CTkEntry(master=frame,
                               placeholder_text="Width",
                               width=150,
                               height=20,
                               border_width=2,
                               corner_radius=10,
                               font=entry_font2,
                               )

    width_entry.pack(padx=10, pady=10)
    """Height entry"""
    height_entry = ctk.CTkEntry(master=frame,
                                placeholder_text="Height",
                                width=150,
                                height=20,
                                border_width=2,
                                corner_radius=10,
                                font=entry_font2,
                                state=height_entry_visibility.get())

    height_entry.pack(padx=10, pady=10)
    """Start Button"""
    start_button = ctk.CTkButton(master=frame,
                                 text="Start",
                                 command=start_bim,
                                 corner_radius=10,
                                 height=40,
                                 width=100,
                                 font=entry_font)
    start_button.pack(padx=10, pady=10)

    base.mainloop()


if __name__ == '__main__':
    main_gui()
