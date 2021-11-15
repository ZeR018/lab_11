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
        master.minsize(1530, 670)  # минимальный размер окна

        self.x0 = tk.DoubleVar(master, 0)  # x0
        self.u0 = tk.DoubleVar(master, 2)  # u0
        self.a1 = tk.DoubleVar(master, 10)  # a1
        self.a3 = tk.DoubleVar(master, 20)  # a3
        self.m = tk.DoubleVar(master, 10)  # m
        self.border = tk.DoubleVar(master, 100.0)  # правая граница
        self.accuracy = tk.DoubleVar(master, 0.0001)  # точность выхода на правую границу
        self.error = tk.DoubleVar(master, 0.00001)  # контроль лок. поргрешности
        self.max_step = tk.DoubleVar(master, 10000000)  # макс. число шагов
        self.step = tk.DoubleVar(master, 0.01)  # начальный шаг
        self.rb_var = tk.IntVar(master)  # хранит 0 или 1 (выход на границу x или u)
        self.rb_var.set(0)  # значение по умолчанию
        self.cb_var = tk.BooleanVar(master)  # хранит True или False (включен ли контроль погр-ти)
        self.cb_var.set(1)  # значение по умолчанию

        self.create_widgets()  # создание виджетов

    def create_widgets(self):
        # место для задачи (открытие по кнопке)
        exec_b = tk.Button(text='Задача', bg='#ececec', highlightbackground='#ececec', command=self.task_window).grid(
            row=5, column=5, padx=10, pady=(10, 10), sticky='we')

        # начальные условия
        cond_l = tk.Label(text='Начальные условия', bg='#ececec', font='Helvetica 10 bold').grid(row=0, column=0,
                                                                                                 columnspan=2, padx=10,
                                                                                                 pady=(10, 0))
        cond_xl = tk.Label(text='x0', bg='#ececec').grid(row=1, column=0, padx=(10, 0), sticky='w')
        cond_xe = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.x0).grid(row=1, column=1, padx=(0, 10))
        cond_ul = tk.Label(text='u0', bg='#ececec').grid(row=2, column=0, padx=(10, 0), sticky='w')
        cond_ue = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.u0).grid(row=2, column=1, padx=(0, 10))
        cond_p = tk.Label(text='Параметры системы', bg='#ececec').grid(row=3, column=0, columnspan=2)
        cond_a1l = tk.Label(text='a1', bg='#ececec').grid(row=4, column=0, padx=(10, 0), sticky='w')
        cond_a1e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.a1).grid(row=4, column=1, padx=(0, 10))
        cond_a3l = tk.Label(text='a3', bg='#ececec').grid(row=5, column=0, padx=(10, 0), sticky='w')
        cond_a3e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.a3).grid(row=5, column=1, padx=(0, 10))
        cond_ml = tk.Label(text='m', bg='#ececec').grid(row=6, column=0, padx=(10, 0), sticky='nw')
        cond_me = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.m).grid(row=6, column=1, padx=(0, 10),
                                                                                    sticky='n')

        # график
        self.canvas = tk.Canvas()

        # кнопка Вычислить
        exec_b = tk.Button(text='Вычислить', bg='#ececec', highlightbackground='#ececec', command=self.execute).grid(
            row=6, column=5, padx=10, pady=(0, 10), sticky='we')

        # параметры програмы
        param_l = tk.Label(text='Параметры программы', bg='#ececec', font='Helvetica 10 bold').grid(row=0, column=2,
                                                                                                    padx=10,
                                                                                                    columnspan=4,
                                                                                                    pady=(10, 0),
                                                                                                    sticky='we')
        border_l = tk.Label(text='Правая граница', bg='#ececec').grid(row=1, column=2, padx=10,
                                                                      pady=(10, 0), sticky='w')
        rb1 = tk.Radiobutton(text='x', variable=self.rb_var, value=0, bg='#ececec').grid(row=1, column=3, pady=(10, 0),
                                                                                         sticky='e')
        rb2 = tk.Radiobutton(text='u', variable=self.rb_var, value=1, bg='#ececec').grid(row=1, column=4, pady=(10, 0),
                                                                                         sticky='e')
        border_e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.border).grid(row=2, column=2,
                                                                                          columnspan=3,
                                                                                          padx=(10, 0), sticky='we')
        error_cb = tk.Checkbutton(bg='#ececec', variable=self.cb_var).grid(row=3, column=3, columnspan=2)
        error_l = tk.Label(text='Контроль лок. погрешности', bg='#ececec').grid(row=3, column=2, padx=10, sticky='w')
        error_e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.error).grid(row=4, column=2, columnspan=3,
                                                                                        padx=(10, 0), sticky='we')
        max_steps_l = tk.Label(text='Максимальное число шагов', bg='#ececec').grid(row=5, column=2, padx=10, sticky='w')
        max_steps_e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.max_step).grid(row=6, column=2,
                                                                                               columnspan=3,
                                                                                               padx=(10, 0),
                                                                                               sticky='nwe')
        accuracy_l = tk.Label(text='Точность выхода на границу', bg='#ececec').grid(row=1, column=5, padx=10,
                                                                                    sticky='w')
        accuracy_e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.accuracy).grid(row=2, column=5,
                                                                                              padx=(10, 0), sticky='we')
        step_l = tk.Label(text='Начальный шаг', bg='#ececec').grid(row=3, column=5, padx=10, sticky='w')
        step_e = tk.Entry(highlightbackground='#cbcbcb', textvariable=self.step).grid(row=4, column=5, columnspan=3,
                                                                                      padx=(10, 0), sticky='we')

        # справка
        reference_l = tk.Label(text='Справка', bg='#ececec', font='Helvetica 10 bold').grid(row=0, column=8, pady=10,
                                                                                            padx=10, sticky='we')
        self.reference_t = tk.Text(height=10, width=110, highlightbackground='#cbcbcb')
        self.reference_t.grid(row=1, column=8, rowspan=6, padx=(10, 10),
                              sticky='we')

        # таблица

    def tables(self, p, _i, d):
        heads = ['k', 'x', 'V', 'ОЛП', 'h', 'U', 'E', 'C1', 'C2']
        self.table = ttk.Treeview(self.master, show='headings')
        self.table['columns'] = heads
        self.table.grid(row=9, column=5, columnspan=4, rowspan=10, padx=(10, 0), sticky=tk.NSEW)
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')
            self.table.column(header, width=8)
        self.table.column('ОЛП', width=100)
        self.table.column('V', width=100)
        self.table.column('E', width=100)

        for z in range(int(_i.value / p['k'])):
            if d[p['e'] + z * p['k']] == 0:
                _s = "<1e-16"
            else :
                _s = d[p['e'] + z * p['k']]
            self.table.insert('', tk.END, values=(
            z, round((d[p['x'] + z * p['k']]), 4), (d[p['V'] + z * p['k']]),  _s,
            d[p['h'] + z * p['k']], d[p['U'] + z * p['k']], d[p['E'] + z * p['k']], int(d[p['c1'] + z * p['k']]),
            int(d[p['c2'] + z * p['k']])))
        scroll_bar1 = Scrollbar(self.master, orient=VERTICAL, command=self.table.yview)
        scroll_bar1.grid(row=9, column=9, padx=10, sticky=tk.NSEW)
        self.table.configure(yscroll=scroll_bar1.set)

        # график

    def plotOnPlane(self, X, Y):
        plt.close()
        f = plt.figure(num=2, figsize=(7, 5), dpi=80, facecolor='#ececec')
        fig = plt.subplot(1, 1, 1)
        fig.set_title('График зависимости скорости U от времени x')
        fig.set_xlabel('x, сек.')
        fig.set_ylabel('U(x), м/сек.')
        fig.plot(X, Y, '-k')
        return f

    def create_form_graph(self, figure):
        self.canvas = FigureCanvasTkAgg(figure, self.master)
        self.canvas.get_tk_widget().grid(row=9, column=1, columnspan=4, rowspan=1)
        self.canvas.draw()

    # справка
    def reference(self, p, _i, d):
        self.reference_t.delete(1.0, END)
        mul_counter = 0
        div_counter = 0
        max_step = self.step.get()
        min_step = self.step.get()
        max_error = 0
        max_error_point = self.x0.get()
        for z in range(1, int(_i.value / p['k'])):
            if d[p['E'] + z * p['k']] > max_error:
                max_error = d[p['E'] + z * p['k']]
                max_error_point = d[p['x'] + z * p['k']]
            div_counter += d[p['c1'] + z * p['k']]
            #if d[p['c1'] + z * p['k']] > div_counter:
            #    div_counter = d[p['c1'] + z * p['k']]
            mul_counter += d[p['c2'] + z * p['k']]
            #if d[p['c2'] + z * p['k']] > mul_counter:
            #    mul_counter = d[p['c2'] + z * p['k']]
            if d[p['h'] + z * p['k']] > max_step:
                max_step = d[p['h'] + z * p['k']]
            if d[p['h'] + z * p['k']] < min_step:
                min_step = d[p['h'] + z * p['k']]
        self.reference_t.insert(1.0, 'Метод РК3\n\n')
        self.reference_t.insert(3.0, 'Число шагов: ' + str(int(_i.value / p['k'])) + '\n')
        self.reference_t.insert(4.0, 'Число удвоений: ' + str(int(mul_counter)) + '\n')
        self.reference_t.insert(5.0, 'Число делений: ' + str(int(div_counter)) + '\n')
        self.reference_t.insert(6.0, 'Максимальный шаг: ' + str(max_step) + '\n')
        self.reference_t.insert(7.0, 'Минимальный шаг: ' + str(min_step) + '\n')
        self.reference_t.insert(8.0, 'Максимальная ошибка: ' + str(max_error) + ', в точке x = ' + str(max_error_point))

    # окно задачи
    def task_window(self):
        task = tk.Toplevel()
        task.title('Задача')
        img = ImageTk.PhotoImage(Image.open("./task.jpg"))
        panel = tk.Label(task, image=img)
        panel.pack(side='bottom', fill='both', expand='yes')
        task.mainloop()

    #  выполняется при нажатии кнопки "Вычислить"
    def execute(self):
        # записываем начальные условия задачи
        init_params = (c_double * 11)()
        init_params[0] = self.x0.get()
        init_params[1] = self.u0.get()
        init_params[2] = 1
        init_params[3] = self.step.get()
        init_params[4] = 1
        init_params[5] = 1
        init_params[6] = 1
        init_params[7] = self.error.get()
        init_params[8] = self.max_step.get()
        init_params[9] = self.border.get()  # точность выхода на границу
        init_params[10] = self.accuracy.get()
        # записываем параметры чм
        # method_params = (c_double*2)()
        # method_params[0] = self.accuracy.get()  # точность выхода на границу
        # method_params[1] = self.error.get()  # контроль погрешности
        # записываем данные с кнопок (выбор границы / контроль лп)
        button_data = (c_int * 2)()
        button_data[0] = self.rb_var.get()  # выбор границы 0 - x, 1 - u
        button_data[1] = self.cb_var.get()  # контроль ЛП True/False

        # подрубаем dll
        dll = cdll.LoadLibrary("dll_for_py2//x64//Release//dll_for_py2.dll")
        # вроде нужно чтобы работало
        dll.work_RK31R.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None
        # ---------------------------------------------------------
        dll.del_mem.argtypes = [POINTER(POINTER(c_double))]
        dll.work_RK31R.restype = None

        # для ракрытия массива
        p = {'k': 8, 'x': 0, 'V': 1, 'e': 2, 'h': 3, 'U': 4, 'E': 5, 'c1': 6, 'c2': 7}

        # главный массив
        d = POINTER(c_double)()

        # количество эл в массиве
        _i = (c_int)()

        # работа
        dll.work_RK31R(byref(d), byref(init_params), byref(button_data), byref(_i))

        # -------------------------------------------------ИНСТРУКЦИЯ---------------------------------------------------------------------------#
        # --------------------------------------------------------------------------------------------------------------------------------------#
        # #из массива берем переменную x      далее берем строку          и умножаем ее на кратность массива
        #           d[p['x']                           +z                          *p['k']]

        # for z in range(int(_i.value/p['k'])):
        # use_it.append(d[p['x']+z*p['k']])
        # use_it.append(d[p['v1']+z*p['k']])

        # print(use_it) # проверка

        # for z in range(int(_i.value/p['k'])):
        #    print("i: ",z,"\tx: ",d[p['x']+z*p['k']],"\tv: ",d[p['v1']+z*p['k']],"\te: ",d[p['e']+z*p['k']],"\th: ",d[p['h']+z*p['k']],"\tu: ",d[p['u']+z*p['k']],"\tE: ",d[p['E']+z*p['k']],"\tC1: ",d[p['c1']+z*p['k']],"\tC2: ",d[p['c2']+z*p['k']],"\n")

        X = []
        for z in range(int(_i.value / p['k'])):
            X.append(d[p['x'] + z * p['k']])
        Y = []
        for z in range(int(_i.value / p['k'])):
            Y.append(d[p['V'] + z * p['k']])

        self.figure = self.plotOnPlane(X, Y)
        self.create_form_graph(self.figure)  # график

        self.tables(p, _i, d)  # таблица
        self.reference(p, _i, d)

        # удаляем память
        dll.del_mem(byref(d))


root = tk.Tk()
gui = Interface(root)
root.mainloop()
