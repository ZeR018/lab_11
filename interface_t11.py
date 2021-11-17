import tkinter as tk
from ctypes import *
import ctypes
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, END
from tkinter import *
from PIL import Image, ImageTk


class Interface:
    def __init__(self, master):
        self.master = master  # инициализируем основное окно
        self.photo = tk.PhotoImage(file='logo.png')  # загрузка иконки приложения
        master.iconphoto(False, self.photo)  # установка иконки
        master.title('Задача Коши для ОДУ выполнил Варварин Евгений')  # заголовок
        master.configure(bg='#ececec')  # фон
        master.minsize(1200, 600)  # минимальный размер окна

        self.u0 = tk.DoubleVar(master, 2)  # u0
        self.u0_quote = tk.DoubleVar(master, 3)  # u0'
        self.x0 = tk.DoubleVar(master, 0)  # x0
        self.k = tk.DoubleVar(master, 10)  # k
        self.f = tk.DoubleVar(master, 20)  # f
        self.m = tk.DoubleVar(master, 10)  # m
        self.border = tk.DoubleVar(master, 100.0)  # правая граница
        self.accuracy = tk.DoubleVar(master, 0.0001)  # точность выхода на правую границу
        self.error = tk.DoubleVar(master, 0.00001)  # контроль лок. поргрешности
        self.max_step = tk.DoubleVar(master, 10000000)  # макс. число шагов
        self.step = tk.DoubleVar(master, 0.01)  # начальный шаг
        self.cb_var = tk.BooleanVar(master)  # хранит True или False (включен ли контроль погр-ти)
        self.cb_var.set(1)  # значение по умолчанию

        self.create_widgets()

    def make_menu(self):
        mainmenu = Menu(self.master)
        self.master.config(menu=mainmenu)

        params = Menu(mainmenu, tearoff=0)
        params.add_command(label="Начальные условия", command = self.set_begin_value)
        params.add_command(label="Параметры системы", command = self.set_system_params)
        params.add_command(label="Параметры метода", command = self.set_method_params)
        mainmenu.add_cascade(label="Параметры задачи", menu=params)

        info = Menu(mainmenu, tearoff=0)
        info.add_command(label="Описание задачи")
        info.add_command(label="Описание метода")
        mainmenu.add_cascade(label="Информация", menu=info)

    def make_frame(self):
        self.frame_top = LabelFrame(text="Параметры")
        self.frame_top.grid(row=0, column=1, padx = (10, 0), pady = (10, 0))
        begin_params = Label(self.frame_top, text = 'Начальные условия', font='Helvetica 10 bold').grid(row=1, column=1, sticky = 'w')
        u0 = Label(self.frame_top, text='U\u2092 = ' + str(self.u0.get())).grid(row=2, column=1, sticky = 'w')
        u0_quote = Label(self.frame_top, text="U\u2092' = " + str(self.u0_quote.get())).grid(row=3, column=1, sticky = 'w')
        x0 = Label(self.frame_top, text='X\u2092 = ' + str(self.x0.get())).grid(row=4, column=1, sticky = 'w')
        system_params = Label(self.frame_top, text = 'Параметры системы', font='Helvetica 10 bold').grid(row=5, column=1, sticky = 'w')
        k = Label(self.frame_top, text='k = ' + str(self.k.get())).grid(row=6, column=1, sticky = 'w')
        f = Label(self.frame_top, text='f = ' + str(self.f.get())).grid(row=7, column=1, sticky = 'w')
        m = Label(self.frame_top, text='m = ' + str(self.m.get())).grid(row=8, column=1, sticky = 'w')
        method_params = Label(self.frame_top, text='Параметры метода', font='Helvetica 10 bold').grid(row=9, column=1, sticky = 'w')
        border = Label(self.frame_top, text='Правая граница: ' + str(self.border.get())).grid(row=10, column=1, sticky = 'w')
        if self.cb_var.get():
            lp = Label(self.frame_top, text='Контроль локальной погрешности: ' + str(self.error.get())).grid(row=11, column=1, sticky = 'w')
        else:
            lp = Label(self.frame_top, text='Контроль локальной погрешности: отключен').grid(row=11, column=1, sticky = 'w')
        max_steps = Label(self.frame_top, text='Максимальное число шагов: ' + str(self.max_step.get())).grid(row=12, column=1, sticky = 'w')
        accuracy = Label(self.frame_top, text='Точность выхода на границу: ' + str(self.accuracy.get())).grid(row=13, column=1, sticky = 'w')
        step = Label(self.frame_top, text='Начальный шаг: ' + str(self.step.get())).grid(row=14, column=1, sticky = 'w')


    def set_begin_value(self):
        begin = tk.Toplevel()
        begin.title('Начальные условия')
        begin.minsize(300,100)
        u0l = tk.Label(begin, text='U\u2092', bg='#ececec').grid(row=1, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        u0e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.u0, width = 30).grid(row=1, column=2, pady = (10, 0))
        u0_quote_l = tk.Label(begin, text="U\u2092'", bg='#ececec').grid(row=2, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        u0_quote_e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.u0_quote, width = 30).grid(row=2, column=2, pady = (10, 0))
        x0l = tk.Label(begin, text='X\u2092', bg='#ececec').grid(row=3, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        x0e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.x0, width = 30).grid(row=3, column=2, pady = (10, 0))
        save = tk.Button(begin, text='Сохранить', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=4, column=1, columnspan = 2, pady = (10, 10))
        begin.mainloop()

    def set_system_params(self):
        system = tk.Toplevel()
        system.title('Начальные условия')
        system.minsize(300,100)
        kl = tk.Label(system, text='k', bg='#ececec').grid(row=1, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        ke = tk.Entry(system, highlightbackground='#cbcbcb', textvariable=self.k, width = 30).grid(row=1, column=2, pady = (10, 0))
        fl = tk.Label(system, text="f", bg='#ececec').grid(row=2, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        fe = tk.Entry(system, highlightbackground='#cbcbcb', textvariable=self.f, width = 30).grid(row=2, column=2, pady = (10, 0))
        ml = tk.Label(system, text='m', bg='#ececec').grid(row=3, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        me = tk.Entry(system, highlightbackground='#cbcbcb', textvariable=self.m, width = 30).grid(row=3, column=2, pady = (10, 0))
        save = tk.Button(system, text='Сохранить', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=4, column=1, columnspan = 2, pady = (10, 10))
        system.mainloop()

    def set_method_params(self):
        method = tk.Toplevel()
        method.title('Начальные условия')
        method.minsize(300,100)
        border_l = tk.Label(method, text='Правая граница', bg='#ececec').grid(row=1, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        border_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.border, width = 30).grid(row=1, column=2, pady = (10, 0), padx = (0, 10))
        error_l = tk.Label(method, text="Контроль ЛП", bg='#ececec').grid(row=2, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        error_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.error, width = 30).grid(row=2, column=2, pady = (10, 0), padx = (0, 10))
        error_cb = tk.Checkbutton(method, bg='#ececec', variable=self.cb_var).grid(row=2, column=3, pady = (10, 0), padx = (0, 10))
        max_steps_l = tk.Label(method, text='Макс. число шагов', bg='#ececec').grid(row=3, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        max_steps_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.max_step, width = 30).grid(row=3, column=2, pady = (10, 0), padx = (0, 10))
        accuracy_l = tk.Label(method, text='Точность выхода на границу', bg='#ececec').grid(row=4, column=1, padx=(10, 0), pady=(10, 0), sticky = 'w')
        accuracy_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.accuracy, width=30).grid(row=4,
                                                                                                          column=2,
                                                                                                          pady=(10, 0), padx = (0, 10))
        step_l = tk.Label(method, text='Начальный шаг', bg='#ececec').grid(row=5, column=1, padx=(10, 0), pady=(10, 0), sticky = 'w')
        step_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.step, width=30).grid(row=5,
                                                                                                         column=2,
                                                                                                         pady=(10, 0), padx = (0, 10))
        save = tk.Button(method, text='Сохранить', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=6, column=1, columnspan = 3, pady = (10, 10))
        method.mainloop()

    def save(self):
        self.frame_top.destroy()
        self.make_frame()

    def create_notebook(self):
        notebook = ttk.Notebook()
        notebook.grid(row=0, column=2, sticky = 'n', pady = (10, 0), padx = (10, 10))
        self.set_nb_frames(notebook)
        notebook.add(self.table_frame, text='Таблица')
        notebook.add(self.graph1_frame, text='График 1')
        notebook.add(self.graph2_frame, text='График 2')
        notebook.add(self.graph3_frame, text='График 3')
        notebook.add(self.info_frame, text='Справка')

    def set_nb_frames(self, notebook):
        self.table_frame = ttk.Frame(notebook, width=900, height=300)
        self.graph1_frame = ttk.Frame(notebook, width=400, height=300)
        self.graph2_frame = ttk.Frame(notebook, width=400, height=300)
        self.graph3_frame = ttk.Frame(notebook, width=400, height=300)
        self.info_frame = ttk.Frame(notebook, width=400, height=300)


    def create_widgets(self):
        self.make_menu()
        self.make_frame()
        self.create_notebook()
        execute = tk.Button(text='Вычислить', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=1, column=1, pady = (10, 10), padx = (10, 0), sticky = 'we')
        clear = tk.Button(text='Очистить график', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=2, column=1, pady = (10, 10), padx = (10, 0), sticky = 'we')


root = tk.Tk()
gui = Interface(root)
root.mainloop()