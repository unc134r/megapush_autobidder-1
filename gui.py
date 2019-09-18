from tkinter import *
from tkinter import ttk
from platform import system
import threading


def createwidgets():
	frame = Frame(scroll_frame, borderwidth=2, relief="groove")
	frame.pack(side="top", fill="x")

	Label(frame, text=len(frames) + 1).pack(side="left", padx=1)

	Label(frame, text='ID').pack(side="left")
	id = StringVar()
	id.set('0')
	entry_id = Entry(frame, textvariable=id)
	entry_id.pack(side="left", padx=9)
	ttk.Separator(frame, orient='vertical').pack(side="left", padx=2)

	Label(frame, text='Интервал проверки (сек)').pack(side="left")
	interval = StringVar()
	interval.set('0')
	entry_interval = Entry(frame, textvariable=interval, width=7)
	entry_interval.pack(side="left", padx=9)
	ttk.Separator(frame, orient='vertical').pack(side="left", padx=2)

	Label(frame, text='Шаг ставки').pack(side="left")
	step = StringVar()
	step.set('0.1')
	entry_step = Entry(frame, textvariable=step, width=7)
	entry_step.pack(side="left", padx=9)
	ttk.Separator(frame, orient='vertical').pack(side="left", padx=2)

	Label(frame, text='Стандартные начальные ставки').pack(side="left")
	combovalue = StringVar()
	combo = ttk.Combobox(frame, textvariable=combovalue, width=14, state='readonly')
	combo['values'] = ('', 'Создание', 'Минимальная', 'Средняя', 'Максимальная')
	combo.pack(side="left", padx=9)
	ttk.Separator(frame, orient='vertical').pack(side="left", padx=2)


	Label(frame, text='Пользовательская ставка').pack(side="left")
	custom = StringVar()
	custom.set('0.1')
	entry_custom = Entry(frame, textvariable=custom, width=7)
	entry_custom.pack(side="left", padx=9)
	ttk.Separator(frame, orient='vertical').pack(side="left", padx=2)


	Label(frame, text='Предел ставки').pack(side="left")
	maxbid = StringVar()
	maxbid.set('0.5')
	entry_maxbid = Entry(frame, textvariable=maxbid, width=7)
	entry_maxbid.pack(side="left", padx=9)

	delbtn = Button(frame, text='X', width=1, command=lambda: rmv_frame(int(label_count.cget("text"))-1))
	delbtn.pack(side='right')

	frames.append({
		'frame': frame,
		'id': id,
		'interval': interval,
		'step': step,
		'custom': custom,
		'combovalue': combovalue,
		'maxbid': maxbid
	})

def rmv_frame(number):
	frames[number]['frame'].destroy()
	frames.remove(frames[number])

def config_canvas(event):
	canvas.configure(scrollregion=canvas.bbox("all"), width=1300, height=700)

def _on_mousewheel(event):
	if system() == 'Windows':
		canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
	elif system() == 'Darwin':
		canvas.yview_scroll(int(-1 * (event.delta)), "units")

def enabling():
	if active[0]:
		active[0] = False
		start_btn.config(text='Начать')
	else:
		active[0] = True
		start_btn.config(text='Остановить')


frames = []

active = [False]

root = Tk()
root.geometry("1250x800+100+100")
root.title('MegaPush Editor')

mainframe = Frame(root, borderwidth=2, relief="groove", width=500,height=1000,bd=1)
mainframe.pack(side="top", fill="x")

canvas = Canvas(mainframe)
scroll_frame = Frame(canvas)
scroll = Scrollbar(mainframe, command=canvas.yview)
scroll.pack(side='right', fill='y')
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side='top')
canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
scroll_frame.bind("<Configure>", config_canvas)
root.bind_all("<MouseWheel>", _on_mousewheel)

buttonframe = Frame(root, borderwidth=2, relief="groove")
buttonframe.pack(side='bottom', fill='x')

start_btn = Button(buttonframe, text="Начать", command=enabling, width=10)
start_btn.pack(side="bottom", pady=10)
create_btn = Button(buttonframe, text="Добавить", command=createwidgets, width=10)
create_btn.pack(side="bottom", pady=10)


if __name__ == '__main__':
	root.mainloop()


# Хранить все нужные виджеты в списке словарей
# Как выполнять другие функции во время mainloop()
# Поле с выбором начальной ставки или если оно пустое - поле с кастомной начальной ставкой. Если выбрал не кастомную - поле с кастомной неактивно
# BUGOFF Индексирование при удалении фреймов. Могут быть дубликаты
