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
        master.title('Задача Коши для ОДУ №11 выполнил Дыряев Всеволод 381903-2')  # заголовок
        master.configure(bg='#ececec')  # фон
        master.minsize(1200, 500)  # минимальный размер окна

        self.u0 = tk.DoubleVar(master, 7.5)  # u0
        self.u0_quote = tk.DoubleVar(master, 0)  # u0'
        self.x0 = tk.DoubleVar(master, 0)  # x0
        self.k = tk.DoubleVar(master, 175)  # k
        self.f = tk.DoubleVar(master, 0.3)  # f
        self.m = tk.DoubleVar(master, 4.5)  # m
        self.border = tk.DoubleVar(master, 100.0)  # правая граница
        self.accuracy = tk.DoubleVar(master, 0.0001)  # точность выхода на правую границу
        self.error = tk.DoubleVar(master, 0.00001)  # контроль лок. поргрешности
        self.max_step = tk.DoubleVar(master, 10000)  # макс. число шагов
        self.step = tk.DoubleVar(master, 0.01)  # начальный шаг
        self.cb_var = tk.BooleanVar(master)  # хранит True или False (включен ли контроль погр-ти)
        self.cb_var.set(1)  # значение по умолчанию

        self.i = 0

        self.label_1 = ['График зависимости смещения груза U от времени x', 'x, сек.', 'U(x), м.']
        self.label_2 = ["График зависимости скорости груза U' от времени x", 'x, сек.', "U'(x), м/сек."]
        self.label_3 = ["График зависимости скорости U' от смещения груза U ", "U(x), м.", "U', м/сек."]

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
        info.add_command(label="Описание задачи", command = self.task_window)
        info.add_command(label="Описание метода", command = self.method_window)
        mainmenu.add_cascade(label="Информация", menu=info)

    def task_window(self):
        task = tk.Toplevel()
        task.title('Описание задачи')
        img = ImageTk.PhotoImage(Image.open("./task.jpg"))
        panel = tk.Label(task, image=img)
        panel.pack(side='bottom', fill='both', expand='yes')
        task.mainloop()

    def method_window(self):
        task = tk.Toplevel()
        task.title('Описание метода')
        img = ImageTk.PhotoImage(Image.open("./method.jpg"))
        panel = tk.Label(task, image=img)
        panel.pack(side='bottom', fill='both', expand='yes')
        task.mainloop()

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
        u0l = tk.Label(begin, text='U\u2092', bg='#ececec').grid(row=2, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        u0e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.u0, width = 30).grid(row=2, column=2, pady = (10, 0))
        u0_quote_l = tk.Label(begin, text="U\u2092'", bg='#ececec').grid(row=3, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        u0_quote_e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.u0_quote, width = 30).grid(row=3, column=2, pady = (10, 0))
        x0l = tk.Label(begin, text='X\u2092', bg='#ececec').grid(row=1, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        x0e = tk.Entry(begin, highlightbackground='#cbcbcb', textvariable=self.x0, width = 30).grid(row=1, column=2, pady = (10, 0))
        save = tk.Button(begin, text='Сохранить', bg='#ececec', highlightbackground='#ececec', command=self.save).grid(
            row=4, column=1, columnspan = 2, pady = (10, 10))
        begin.mainloop()

    def set_system_params(self):
        system = tk.Toplevel()
        system.title('Параметры сисетмы')
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
        method.title('Параметры метода')
        method.minsize(300,100)
        border_l = tk.Label(method, text='Правая граница', bg='#ececec').grid(row=1, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        border_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.border, width = 30).grid(row=1, column=2, pady = (10, 0), padx = (0, 10))
        error_l = tk.Label(method, text="Контроль ЛП", bg='#ececec').grid(row=4, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        error_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.error, width = 30).grid(row=4, column=2, pady = (10, 0), padx = (0, 10))
        error_cb = tk.Checkbutton(method, bg='#ececec', variable=self.cb_var).grid(row=4, column=3, pady = (10, 0), padx = (0, 10))
        max_steps_l = tk.Label(method, text='Макс. число шагов', bg='#ececec').grid(row=5, column=1, padx = (10, 0), pady = (10, 0), sticky = 'w')
        max_steps_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.max_step, width = 30).grid(row=5, column=2, pady = (10, 0), padx = (0, 10))
        accuracy_l = tk.Label(method, text='Точность выхода на границу', bg='#ececec').grid(row=3, column=1, padx=(10, 0), pady=(10, 0), sticky = 'w')
        accuracy_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.accuracy, width=30).grid(row=3,
                                                                                                          column=2,
                                                                                                          pady=(10, 0), padx = (0, 10))
        step_l = tk.Label(method, text='Начальный шаг', bg='#ececec').grid(row=2, column=1, padx=(10, 0), pady=(10, 0), sticky = 'w')
        step_e = tk.Entry(method, highlightbackground='#cbcbcb', textvariable=self.step, width=30).grid(row=2,
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
        notebook.grid(row=0, column=2, sticky = 'n', rowspan = 4, pady = (10, 0), padx = (10, 10))
        self.set_nb_frames(notebook)
        notebook.add(self.table_frame, text='Таблица')
        notebook.add(self.graph1_frame, text='График 1')
        notebook.add(self.graph2_frame, text='График 2')
        notebook.add(self.graph3_frame, text='График 3')
        notebook.add(self.info_frame, text='Справка')

    def set_nb_frames(self, notebook):
        self.table_frame = ttk.Frame(notebook, width=900, height=400)
        self.graph1_frame = ttk.Frame(notebook, width=400, height=300)
        self.graph2_frame = ttk.Frame(notebook, width=400, height=300)
        self.graph3_frame = ttk.Frame(notebook, width=400, height=300)
        self.info_frame = ttk.Frame(notebook, width=400, height=300)

    def create_widgets(self):
        self.make_menu()
        self.make_frame()
        self.create_notebook()
        execute = tk.Button(text='Вычислить', bg='#ececec', highlightbackground='#ececec', command=self.execute).grid(
            row=1, column=1, pady = (10, 10), padx = (10, 0), sticky = 'nwe')
        self.create_table()
        self.plotOnPlane(self.label_1, self.graph1_frame)
        self.plotOnPlane(self.label_2, self.graph2_frame)
        self.plotOnPlane(self.label_3, self.graph3_frame)

    def dll_work(self):
        init_params = (c_double * 11)()
        init_params[0] = self.x0.get()
        init_params[1] = self.u0.get()
        init_params[2] = self.u0_quote.get()
        init_params[3] = self.step.get()
        init_params[4] = self.k.get()
        init_params[5] = self.f.get()
        init_params[6] = self.m.get()
        init_params[7] = self.error.get()
        init_params[8] = self.max_step.get()
        init_params[9] = self.border.get()
        init_params[10] = self.accuracy.get()

        button_data = (c_int * 2)()
        button_data[1] = self.cb_var.get()  # контроль ЛП True/False

        dll = cdll.LoadLibrary("dll_for_py2//x64//Release//dll_for_py2.dll")
        dll.work_RK31R.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None
        dll.del_mem.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None

        p = {'x': 0, 'V1': 1, 'V2': 2, 'V11': 3, 'V22': 4, 'e': 5, 'h': 6, 'U1': 7, 'U2': 8, 'E': 9, 'c1': 10,
             'c2': 11, 'k': 12}
        d = POINTER(c_double)()
        _i = (c_int)()

        dll.work_RK31R(byref(d), byref(init_params), byref(button_data), byref(_i))
        return p, d, _i

    def create_table(self):
        heads = ['k', 'x', 'V1', 'V2', 'V11', 'V22', 'ОЛП', 'h', 'C1', 'C2']
        self.table = ttk.Treeview(self.table_frame, show='headings', height=20)
        self.table['columns'] = heads
        self.table.grid(row=0, column=0, sticky=tk.NSEW)
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')
            self.table.column(header, width=90)

    def destroy_table(self):
        self.table.destroy()

    def fill_table(self, p, d, _i):
        _s = 0
        for z in range(int(_i.value / p['k'])):

            if d[p['e'] + z * p['k']] == 0:
                if z != 0:
                    _s = "<1e-16"
            else:
                _s = d[p['e'] + z * p['k']]
            self.table.insert('', tk.END, values=(
                z,
                round((d[p['x'] + z * p['k']]), 4),
                (d[p['V1'] + z * p['k']]),
                (d[p['V2'] + z * p['k']]),
                (d[p['V11'] + z * p['k']]),
                (d[p['V22'] + z * p['k']]),
                _s,
                d[p['h'] + z * p['k']],
                #d[p['U1'] + z * p['k']],
                #d[p['U2'] + z * p['k']],
                #d[p['E'] + z * p['k']],
                int(d[p['c1'] + z * p['k']]),
                int(d[p['c2'] + z * p['k']])))
        scroll_bar1 = Scrollbar(self.table_frame, orient=VERTICAL, command=self.table.yview)
        scroll_bar1.grid(row=0, column=1, sticky=tk.NSEW)
        self.table.configure(yscroll=scroll_bar1.set)

    def plotOnPlane(self, label, place, X = [0], Y = [0]):
        f = plt.figure(figsize=(11, 5), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title(label[0])
        fig.set_xlabel(label[1])
        fig.set_ylabel(label[2])
        fig.plot(X, Y, '-k')
        self.create_form_graph(f, place)

    def create_form_graph(self, figure, place):
        canvas = FigureCanvasTkAgg(figure, place)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw()

    def fill_graph_1(self, p, d, _i):
        X = []
        for z in range(int(_i.value / p['k'])):
            X.append(d[p['x'] + z * p['k']])
        Y = []
        for z in range(int(_i.value / p['k'])):
            Y.append(d[p['V1'] + z * p['k']])
        self.plotOnPlane(self.label_1, self.graph1_frame, X, Y)

    def fill_graph_2(self, p, d, _i):
        X = []
        for z in range(int(_i.value / p['k'])):
            X.append(d[p['x'] + z * p['k']])
        Y = []
        for z in range(int(_i.value / p['k'])):
            Y.append(d[p['V2'] + z * p['k']])
        self.plotOnPlane(self.label_2, self.graph2_frame, X, Y)

    def fill_graph_3(self, p, d, _i):
        X = []
        for z in range(int(_i.value / p['k'])):
            X.append(d[p['V1'] + z * p['k']])
        Y = []
        for z in range(int(_i.value / p['k'])):
            Y.append(d[p['V2'] + z * p['k']])
        self.plotOnPlane(self.label_3, self.graph3_frame, X, Y)

    def reference(self, p, d, _i):
        mul_counter = 0
        div_counter = 0
        max_step = self.step.get()
        max_step_x = 0
        min_step = self.step.get()
        min_step_x = 0
        max_olp = 0
        max_olp_x = 0
        for z in range(1, int(_i.value / p['k'])):
            if d[p['e'] + z * p['k']] > max_olp:
                max_olp = d[p['e'] + z * p['k']]
                max_olp_x = d[p['x'] + z * p['k']]
            div_counter += d[p['c1'] + z * p['k']]
            mul_counter += d[p['c2'] + z * p['k']]
            if d[p['h'] + z * p['k']] > max_step:
                max_step = d[p['h'] + z * p['k']]
                max_step_x = d[p['x'] + z * p['k']]
            if d[p['h'] + z * p['k']] < min_step:
                min_step = d[p['h'] + z * p['k']]
                min_step_x = d[p['x'] + z * p['k']]
        self.s1 = tk.Label(self.info_frame, text='Метод РК4', bg='#ececec')
        self.s1.grid(row=0, column=0, sticky='w')
        self.s2 = tk.Label(self.info_frame, text=f"Число шагов: {int(_i.value / p['k'])-1}", bg='#ececec')
        self.s2.grid(row=1, column=0, sticky='w')
        self.s3 = tk.Label(self.info_frame, text=f"Число удвоений: {mul_counter}", bg='#ececec')
        self.s3.grid(row=2, column=0, sticky='w')
        self.s4 = tk.Label(self.info_frame, text=f"Число делений: {div_counter}", bg='#ececec')
        self.s4.grid(row=3, column=0, sticky='w')
        self.s5 = tk.Label(self.info_frame, text=f"Максимальный шаг: {max_step}, в точке x = {round(max_step_x, 4)}", bg='#ececec')
        self.s5.grid(row=4, column=0, sticky='w')
        self.s6 = tk.Label(self.info_frame, text=f"Минимальный шаг: {min_step}, в точке x = {round(min_step_x, 4)}", bg='#ececec')
        self.s6.grid(row=5, column=0,sticky='w')
        self.s7 = tk.Label(self.info_frame, text=f"Максимальная ОЛП: {max_olp}, в точке x = {round(max_olp_x, 4)}", bg='#ececec')
        self.s7.grid(row=6, column=0, sticky='w')

    def destroy_reference(self):
        self.s1.destroy()
        self.s2.destroy()
        self.s3.destroy()
        self.s4.destroy()
        self.s5.destroy()
        self.s6.destroy()
        self.s7.destroy()

    def execute(self):
        p, d, i = self.dll_work()
        self.destroy_table()
        self.create_table()
        self.fill_table(p, d, i)
        self.fill_graph_1(p, d, i)
        self.fill_graph_2(p, d, i)
        self.fill_graph_3(p, d, i)
        if self.i > 0:
            self.destroy_reference()
        self.reference(p, d, i)
        self.i += 1






root = tk.Tk()
gui = Interface(root)
root.mainloop()