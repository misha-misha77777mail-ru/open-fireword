import os
import traceback
from tkinter import *
from webbrowser import open_new
from tkinter import messagebox, ttk

import requests
from PIL import Image, ImageTk


__all__ = ('URLabel', 'URLButton', 'ToolTips', 'center_window', 'm_error', 'f_error', 'TipButton', 'add_image',
           'get_mas', 'showerror', 'showinfo', 'showwarning', 'listdir', 'open_site', 'add_icon_and_unmap',
           'show_error', 'fw_toplevel', 'conn_err', 'VERSION', 'get_list')

VERSION = '2.1.1'


def m_error(method):
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            try:
                requests.post('https://fireword.pythonanywhere.com/report', data={'report': traceback.format_exc()})
                messagebox.showerror('Fire Word Error', 'Произошла неопознанная ошибка. '
                                                        'Отчёт был отправлен разработчикам.')
            except requests.exceptions.ConnectionError:
                messagebox.showerror('Fire Word Error',
                                     f'Неопознанная ошибка программы!\n\n{traceback.format_exc()}\n'
                                     'Помогите улучшить работу программы, переслав скриншот этого '
                                     'сообщения по адресу: fireword@bk.ru')
            return e
    return wrapper


def f_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            try:
                requests.post('https://fireword.pythonanywhere.com/report', data={'report': traceback.format_exc()})
                messagebox.showerror('Fire Word Error', 'Произошла неопознанная ошибка. '
                                                        'Отчёт был отправлен разработчикам.')
            except requests.exceptions.ConnectionError:
                messagebox.showerror('Fire Word Error',
                                     f'Неопознанная ошибка программы!\n\n{traceback.format_exc()}\n'
                                     'Помогите улучшить работу программы, переслав скриншот этого '
                                     'сообщения по адресу: fireword@bk.ru')
            return e
    return wrapper


def get_mas():
    return {
        'а': '<1>',
        'б': '<2>',
        'в': '<3>',
        'г': '<4>',
        'д': '<5>',
        'е': '<6>',
        'ё': '<7>',
        'ж': '<8>',
        'з': '<9>',
        'и': '<10>',
        'й': '<11>',
        'к': '<12>',
        'л': '<13>',
        'м': '<14>',
        'н': '<15>',
        'о': '<16>',
        'п': '<17>',
        'р': '<18>',
        'с': '<19>',
        'т': '<20>',
        'у': '<21>',
        'ф': '<22>',
        'х': '<23>',
        'ц': '<24>',
        'ч': '<25>',
        'ш': '<26>',
        'щ': '<27>',
        'ъ': '<28>',
        'ы': '<29>',
        'ь': '<30>',
        'э': '<31>',
        'ю': '<32>',
        'я': '<33>',
        'А': '<-1>',
        'Б': '<-2>',
        'В': '<-3>',
        'Г': '<-4>',
        'Д': '<-5>',
        'Е': '<-6>',
        'Ё': '<-7>',
        'Ж': '<-8>',
        'З': '<-9>',
        'И': '<-10>',
        'Й': '<-11>',
        'К': '<-12>',
        'Л': '<-13>',
        'М': '<-14>',
        'Н': '<-15>',
        'О': '<-16>',
        'П': '<-17>',
        'Р': '<-18>',
        'С': '<-19>',
        'Т': '<-20>',
        'У': '<-21>',
        'Ф': '<-22>',
        'Х': '<-23>',
        'Ц': '<-24>',
        'Ч': '<-25>',
        'Ш': '<-26>',
        'Щ': '<-27>',
        'Ъ': '<-28>',
        'Ы': '<-29>',
        'Ь': '<-30>',
        'Э': '<-31>',
        'Ю': '<-32>',
        'Я': '<-33>',
        '№': '<X>'
    }


class Unmap:
    def __init__(self, root, level):
        self.root = root
        self.level = level
        self.root.bind('<Unmap>', self.unmap)
        self.level.protocol('WM_DELETE_WINDOW', self.unmap)
        self.level.bind('<Escape>', self.unmap)

    def unmap(self, par=None):
        self.level.destroy()
        self.root.unbind('<Unmap>')
        return par

    def abort(self):
        self.root.unbind('<Unmap>')


class URLabel:
    def __init__(self, master, text, font=('TkDefaultFont', None), url=None, fg='blue'):
        self.color = fg
        self.url = url
        self.label = Label(master=master, text=text, font=font[0], fg=fg, cursor='hand2')
        self.label.bind('<Enter>', self.enter)
        self.label.bind('<Leave>', self.leave)
        self.label.bind('<Button-1>', self.on)

    def enter(self, par=None):
        self.label.configure(fg='red')
        return par

    def leave(self, par=None):
        self.label.configure(fg=self.color)
        return par

    @m_error
    def on(self, par=None):
        os.startfile(self.url)
        return par

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def grid(self, **kwargs):
        self.label.grid(**kwargs)

    def place(self, **kwargs):
        self.label.place(**kwargs)

    def destroy(self):
        self.label.destroy()


class URLButton:
    def __init__(self, w, url='', *args, **kwargs):
        self.button = w(*args, **kwargs, command=self.ok)
        self.url = url

    def ok(self):
        open_new(self.url)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def grid(self, **kwargs):
        self.button.grid(**kwargs)

    def place(self, **kwargs):
        self.button.place(**kwargs)

    def destroy(self):
        self.button.destroy()


class ToolTipBase:
    def __init__(self, button, text):
        self.button = button
        self.text = text
        self.wind = None
        self.id = None
        self.x = self.y = 0
        self._id1 = self.button.bind('<Enter>', self.enter)
        self._id2 = self.button.bind('<Leave>', self.leave)
        self._id3 = self.button.bind('<ButtonPress>', self.leave)

    def enter(self, event=None):
        self.schedule()
        return event

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
        return event

    def schedule(self):
        self.unschedule()
        self.id = self.button.after(1000, self.showtip)

    def unschedule(self):
        ad = self.id
        self.id = None
        if ad:
            self.button.after_cancel(ad)

    def showtip(self):
        if self.wind:
            return
        xx = self.button.winfo_rootx() + 20
        yy = self.button.winfo_rooty() + self.button.winfo_height() + 1
        self.wind = tw = Toplevel(self.button)
        tw.wm_overrideredirect(True)
        tw.wm_geometry('+%d+%d' % (xx, yy))
        self.showcontents()

    def showcontents(self):
        label = Label(self.wind, text=str(self.text), justify=LEFT, background='white')
        label.pack(padx=10, pady=10)

    def hidetip(self):
        tw = self.wind
        self.wind = None
        if tw:
            tw.destroy()


class ToolTips(ToolTipBase):
    def __init__(self, button, text, flag=True):
        ToolTipBase.__init__(self, button, text) if flag else None

    def showcontents(self):
        ToolTipBase.showcontents(self)


@f_error
def _place(widget, x, y):
    widget.place(x=x, y=y)
    return widget


@f_error
def listdir(path):
    mas = []
    for i in os.listdir(path):
        if os.path.splitext(i)[1] == '.fw':
            mas.append(i)
    return mas


@f_error
def open_site():
    open_new('https://fireword.glitch.me')


@f_error
def add_image(widget, path):
    widget.img = ImageTk.PhotoImage(Image.open(path))
    widget.configure(image=widget.img)


@f_error
def showinfo(message):
    messagebox.showinfo('Fire Word Info', message)


@f_error
def showwarning(message):
    messagebox.showwarning('Fire Word Info', message)


@f_error
def showerror(message):
    messagebox.showerror('Fire Word Error', message)


@f_error
def conn_err():
    showerror('Нет доступа к сети!')


@f_error
def fw_toplevel(title, width, height, master):
    toplevel = Toplevel()
    toplevel.title(title)
    center_window(master, toplevel, width, height)
    toplevel.resizable(False, False)
    toplevel.transient(master)
    toplevel.grab_set()
    toplevel.focus_set()
    return toplevel


@f_error
def show_error():
    with open('error.hta', 'w') as f:
        f.write('''<head><title>Ошибка</title><hta:application showInTaskBar=yes icon=icon.ico caption=no
innerBorder=no selection=no scroll=no contextmenu=yes /><script language=javascript>var winWidth=310; var winHeight=110;
window.resizeTo(winWidth, winHeight); var winPosX=screen.width/2-winWidth/2; var winPosY=screen.height/2-winHeight/2;
window.moveTo(winPosX, winPosY);</script></head><body><center><font color=red>Ошибка! 
Отсутствует файл blue.json, необходимый для запуска программы.<br>Нажмите Alt+F4 для выхода.</font></center></body>''')
    os.startfile('error.hta')


@f_error
def add_icon_and_unmap(path: str, master, toplevel: Toplevel):
    toplevel.iconbitmap(path + 'images/ico.ico')
    return Unmap(master, toplevel)


@f_error
def get_list(lst):
    mas = ''
    for item in range(4):
        try:
            mas += f'{lst[item]}\n'
        except IndexError:
            break

    if len(lst) > 4:
        mas += '...'
    elif len(lst) <= 4:
        mas = mas[:-1]
    return mas


class TipButton:
    def __init__(self, flag, master, text, tip, command, x, y, width=11, widget=ttk.Button):
        ToolTips(_place(widget(master, text=text, command=command, width=width), x, y), tip, flag)


@f_error
def center_window(parent, root, width, height):
    root.geometry(f'{width}x{height}+{parent.winfo_x() + int((parent.winfo_width() / 2) - (width / 2))}+'
                  f'{parent.winfo_y() + int((parent.winfo_height() / 2) - (height / 2))}')
