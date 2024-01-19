# импортируем tkinter
from tkinter import *

# размеры сетки
N_X = 50
N_Y = 40
# сторона квадрата в сетке
step = 25
# начальная формула
graphs = []
intersection_points = []
intersection_points_poses = []


# функция прекращения работы которую будем использовать в кнопке
def stop_the_program():
    window.destroy()

# функция для удаления всех графиков
def del_all_graphs():
    global graphs, intersection_points, intersection_points_poses
    for graph in graphs:
        canvas.delete(graph[0])
    graphs = []
    text_graphs.set('Графики:'.ljust(30, ' '))
    text_types_graphs.set('Типы графиков:')
    for point in intersection_points:
        canvas.delete(point)
    intersection_points, intersection_points_poses = [], []
    text1.set('Точки пересечения:')


# поиск точек пересечения
def draw_show_intersection_points():
    # проверяем больше ли 2 кол-во графиков
    if len(graphs) > 1:
        global intersection_points_poses
        intersection_points_poses = []
        text1.set('Точки пересечения:')
        # цикл для взятия графика
        for i in range(len(graphs) - 1):
            # цикл для взятия другого графика и поиска точек пересечения с первым
            for j in range(i + 1, len(graphs)):
                new_formula = [0, 0, 0]
                # цикл для приравнивания графиков
                for coefficient in range(len(new_formula)):
                    new_formula[coefficient] = graphs[i][1][coefficient] - graphs[j][1][coefficient]
                poses = []
                if new_formula[0] and new_formula[1]:
                    d = (new_formula[1] ** 2) - (4 * new_formula[0] * new_formula[2])
                    if d < 0:
                        continue
                    else:
                        for a in range(-1, 2, 2):
                            poses.append([])
                            poses[-1].append(((-new_formula[1]) + a * (d ** 0.5)) / (2 * new_formula[0]))
                            poses[-1].append(
                                poses[a][0] ** 2 * graphs[i][1][0] +
                                + poses[a][0] * graphs[i][1][1] + graphs[i][1][2])
                elif new_formula[0]:
                    if -new_formula[2] / new_formula[0] >= 0:
                        for a in range(-1, 2, 2):
                            poses.append([])
                            poses[-1].append(a * (-new_formula[2] / new_formula[0]) ** 0.5)
                            poses[-1].append(poses[a][0] ** 2 * graphs[i][1][0] + graphs[i][1][2])
                    else:
                        continue
                elif new_formula[1]:
                    poses.append([])
                    poses[-1].append(-new_formula[2] / new_formula[1])
                    poses[-1].append(graphs[i][1][1] * poses[-1][0] + graphs[i][1][2])
                for a in range(len(poses)):
                    if (poses[a][0], poses[a][1]) not in intersection_points_poses:
                        intersection_points.append(canvas.create_oval(
                            (N_X * step // 2 - -(poses[a][0] * step) - 3, (N_Y * step) // 2 - (poses[a][1] * step) - 3),
                            (N_X * step // 2 - -(poses[a][0] * step) + 3, (N_Y * step) // 2 - (poses[a][1] * step) + 3),
                            fill='green'))
                        new_text = text1.get() + '\n'
                        text1.set(new_text + f'{(poses[a][0], poses[a][1])}')
                        intersection_points_poses.append((poses[a][0], poses[a][1]))


# функция для рисования графика
def draw_graph():
    a, b, c = ent_a.get(), ent_b.get(), ent_c.get()
    if not a or a.isalpha():
        a = 0
    if not b or b.isalpha():
        b = 0
    if not c or c.isalpha():
        c = 0
    a, b, c = int(a), int(b), int(c)
    if a != 0:
        type_f = 'квадратичный'
    elif a == 0:
        type_f = 'линейный'
    formula = [a, b, c]
    # список точек по которым мы будем рисовать график
    points = []
    # цикл для определения точек
    for x in range(-N_X * 4, N_X * 4):
        x /= 4
        y = 0
        y += x ** 2 * a
        y += x * b
        y += c
        # добавление позиции точки
        points.append((N_X * step // 2 - -(x * step), N_Y * step // 2 - y * step))
    # отрисовываем график и добовляем его в список с графиками
    graphs.append([canvas.create_line(*points, fill='red', width=2), formula])
    new_text = text_graphs.get() + '\n'
    coefficients = ('x^2', 'x', '')
    formula_text = []
    for m in range(len(formula)):
        if not formula[m] - int(formula[m]):
            formula[m] = int(formula[m])
        if formula[m] != 0:
            if formula[m] < 0:
                formula_text.append(f'({str(formula[m]) + coefficients[m]})')
            elif formula[m]:
                formula_text.append(f'{str(formula[m]) + coefficients[m]}')
    text_graphs.set(new_text + ' + '.join(formula_text))
    text_types_graphs.set(text_types_graphs.get() + '\n' + type_f)


# создаём окно
window = Tk()
# меняем цвет заднего фона окна
window['bg'] = '#101010'

text1 = StringVar()
text1.set('Точки пересечения:')
text_graphs = StringVar()
text_graphs.set('Графики:'.ljust(30, ' '))
text_types_graphs = StringVar()
text_types_graphs.set('Типы графиков:')

# создём холст в котором мы и будем отрисовывать график
canvas = Canvas(window, bg='#fff', height=N_Y * step, width=N_X * step)
# основные кнопки
# создаём кнопку для закрытия окна
Button(window, text='Прекратить работу', command=stop_the_program).place(x=0, y=200)
# кнопка для рисования графика
Button(window, text='Нарисовать график', command=draw_graph).place(x=0, y=250)
# кнопка для удаления всех графиков
Button(window, text='Удалить все графики', command=del_all_graphs).place(x=0, y=300)
# кнопка для рисования и показа точек пересечения
Button(window, text='Нарисовать и показать пересечения', command=draw_show_intersection_points).place(x=0, y=350)

# создаём окно ввода
name = Label(text="Подставьте коэфициенты", width=20)
name.place(x=0, y=550)

# отрисовываем линии
for i in range(1, N_X):
    if i == N_X // 2:
        canvas.create_line(
            (i * step, 0), (i * step, N_Y * step), fill='#C71585')
    else:
        canvas.create_line(
            (i * step, 0), (i * step, N_Y * step), fill='black')
    # метка для оси Ox
    canvas.create_text(
        i * step, N_Y // 2 * step + 10, text=str(i - N_X // 2), fill='#101010')
# отрисовываем линии
for i in range(1, N_Y):
    if i == N_Y // 2:
        canvas.create_line(
            (0, i * step), (N_X * step, i * step), fill='#C71585')
    else:
        canvas.create_line(
            (0, i * step), (N_X * step, i * step), fill='black')
    # метка для оси Oy
    canvas.create_text(
        N_X // 2 * step + 10, i * step, text=str(N_Y // 2 - i), fill='#101010')

# дбавляем холст в окно
canvas.pack()

# Создание фрейма
frame = Frame(bd=3, relief=SUNKEN)
frame.place(x=5, y=580)

# Создание трех полей для ввода
ent_a = Entry(frame, width=5)
ent_a.grid(row=0, column=0)

ent_b = Entry(frame, width=5)
ent_b.grid(row=0, column=1)

ent_c = Entry(frame, width=5)
ent_c.grid(row=0, column=2)

# Создание букв для каждого из полей
lab_a = Label(frame, text="A")
lab_a.grid(row=1, column=0)

lab_b = Label(frame, text="B")
lab_b.grid(row=1, column=1)

lab_c = Label(frame, text="C")
lab_c.grid(row=1, column=2)

# текст
label1 = Label(window, textvariable=text1)
label2 = Label(window, textvariable=text_graphs)
label3 = Label(window, textvariable=text_types_graphs)
# отображаем текст
label1.place(x=1300, y=10)
label2.place(x=1300, y=700)
label3.place(x=1500, y=700)

# следующая строчка отвечает за полноэкранный режим окна
window.attributes('-fullscreen', True)
# основной цикл
window.mainloop()
