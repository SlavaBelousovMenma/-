from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from print_job import PrintJob
from matrix import MatrixPrinter
from inkjet import InkjetPrinter
from laser import LaserPrinter
from holder import EntryWithPlaceholder
from prqueue import PrintQueueManager
import time


class PrintManagerApp:
    def __init__(self, root):
        self.root = root
        self.manager = PrintQueueManager()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Принтер")
        self.root.geometry("800x550")

        types_printers = ["Струйный", "Лазерный", "Матричный"]
        types_color = ["Да", "Нет"]
        types_pod = ["Да", "Нет"]
        combobox = ttk.Combobox(values=types_printers)
        combobox.grid(row=1, column=0, columnspan=2, ipadx=70, ipady=6, padx=5, pady=5)

        self.btn1 = ttk.Button(text="Добавить принтер", command=self.add_printer)
        self.btn1.grid(row=1, column=2, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

        self.color_label = tk.Label(text="Цветная пчать")
        self.color_label.grid(row=2, column=2, ipadx=6, ipady=6, padx=5, pady=5)

        self.color_label2 = tk.Label(text="Бесконечная подача")
        self.color_label2.grid(row=2, column=3, ipadx=6, ipady=6, padx=5, pady=5)

        self.btn2 = ttk.Button(text="Показать принтеры", command=lambda: self.manager.report_text())
        self.btn2.grid(row=6, column=1, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)
    
        self.btn3 = ttk.Button(text="Выход", command=exit)
        self.btn3.grid(row=10, column=6, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

        self.btn4 = ttk.Button(text="Добавить задание", command=self.add_job)
        self.btn4.grid(row=3, column=6, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)
    
        self.btn5 = ttk.Button(text="Удалить задание", command=self.delete_job)
        self.btn5.grid(row=5, column=1, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)
    
        self.btn6 = ttk.Button(text="Удалить принтер", command=self.detele_printer)
        self.btn6.grid(row=4, column=1, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

        self.btn7 = ttk.Button(text="Список задач", command=self.show_job_list)
        self.btn7.grid(row=6, column=0, columnspan=1, ipadx=70, ipady=6, padx=5, pady=5)

        self.btn8 = ttk.Button(text="Печать", command=self.simulate_print)
        self.btn8.grid(row=9, column=3, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

        self.entry1 = ttk.Combobox(values=types_printers)
        self.entry1.grid(row=9, column=2, ipadx=6, ipady=6, padx=5, pady=5)

        self.entry7 = EntryWithPlaceholder(root, "Кол-во листов")
        self.entry7.grid(row=3, column=0, columnspan=2, ipadx=70, ipady=6, padx=5, pady=5)

        self.entry8 = EntryWithPlaceholder(root, "Введите номер задания")
        self.entry8.grid(row=9, column=0, ipadx=70, ipady=6, padx=5, pady=5)

        self.entry9 = ttk.Combobox(values=types_color, text="Цветная печать")
        self.entry9.grid(row=3, column=2, ipadx=6, ipady=6, padx=5, pady=5)

        self.entry10 = ttk.Combobox(values=types_pod, text="Бесконечная подача")
        self.entry10.grid(row=3, column=3, ipadx=6, ipady=6, padx=5, pady=5)
    
        self.entry13 = EntryWithPlaceholder(root, "Номер задания")
        self.entry13.grid(row=5, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        self.entry14 = ttk.Combobox(values=types_printers)
        self.entry14.grid(row=4, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        self.st = ScrolledText(root, width=60, height=10)
        self.st.grid(row=8, column=0, columnspan=6, ipadx=6, ipady=6, padx=5, pady=5)
        
        self.root.mainloop()

    def add_job(self):
        self.yes = True
        self.no = True
        if self.entry9.get() == "Нет":
            self.yes = False
        if self.entry10.get() == "Нет":
            self.no = False
        sheets, res, color, continuous_feed = (
            int(self.entry7.get()), 1200, self.yes, self.no
        )
        job = PrintJob(sheets, res, color, continuous_feed, None, None)
        self.manager.add_job(job)

    def show_report(self):
        self.st.delete(1.0, END)
        printers, queue, time = self.manager.report_text()
        output = []
        output.append("Принтеры:")
        for printer in printers:
            output.append(f"\n{printer.name}:")
            output.append(f"\n  Текущие задания: {printer.current_job}")
        output.append(f"\n  Незавершенные задания: {len(queue)}")
        print(output)
        self.st.insert(1.0, output)

    def show_job_list(self):
        self.st.delete(1.0, END)
        for i, job in enumerate(self.manager.get_queue()):
            self.st.insert(
                float(i + 1),
                f"\n Задание {i}: Листы: {job.sheets}, Разрешение: {job.resolution}, Цветное: {job.color}, Непрерывная подача: {job.continuous_feed} \n",
            )

    def delete_job(self):
        idx = int(self.entry13.get())
        if 0 <= idx < len(self.manager.queue):
            self.manager.remove_job(self.manager.queue[idx])
            print(f"Задание на печать удалено.")

    def simulate_print(self):
        self.st.delete(1.0, END)
        idx = int(self.entry8.get())
        if 0 <= idx < len(self.manager.queue):
            chosen_job = self.manager.queue[idx]
            printer = self.manager.find_printer(chosen_job)
            if printer:
                self.st.insert(END, f"\n Началась печать задания {idx} на принтере {self.entry1.get()}:")
                for page in range(1, chosen_job.sheets + 1):
                    self.st.insert(END, f"\nСтраница {page} распечатана")
                    time.sleep(0.2)
                self.st.insert(END, "\n Печать завершена.")
            else:
                self.st.insert(END,"Не найден подходящий принтер для этого задания.")
        else:
            self.st.insert(END,"Введен недопустимый индекс задания.")

    def detele_printer(self):
        name_to_remove = self.entry14.get()
        self.manager.remove_printer(name_to_remove)
        print(f"Принтер {name_to_remove} удален.")

    def add_printer(self):
        if self.combobox.get() == "Струйный":
            self.manager.add_printer(
                InkjetPrinter('Струйный', 210, 297, 1200, 1, 15, False)
            )
        elif self.combobox.get() == "Лазерный":
            self.manager.add_printer(
                LaserPrinter('Лазерный', 210, 297, 1200, 1, 15, True)
            )
        elif self.combobox.get() == "Матричный":
            self.manager.add_printer(
                MatrixPrinter('Матричный', 210, 297, 1200, 1, 15)
            )

    def exit(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PrintManagerApp(root)
