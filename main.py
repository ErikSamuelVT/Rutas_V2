from tkinter import *
from tkinter import ttk
from typing_extensions import Self
import pymysql.cursors


class Window:
    def __init__(self, window):
        self.window = window
        self.window.title("Rutas_V2")
        window.geometry("800x500")

        # CONNECTION DB
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='municipios')

        self.cursor = self.connection.cursor()

        # TABS
        Tabs = ttk.Notebook(self.window)
        Tabs.pack(pady=0)

        routes = Frame(Tabs, width=800, height=500)
        municipalitys = Frame(Tabs, width=800, height=500)
        rate = Frame(Tabs, width=800, height=500)
        consultRoute = Frame(Tabs, width=800, height=500)

        routes.pack(fill="both", expand=1)
        municipalitys.pack(fill="both", expand=1)
        rate.pack(fill="both", expand=1)
        consultRoute.pack(fill="both", expand=1)

        Tabs.add(routes, text="Rutas")
        Tabs.add(municipalitys, text="Municipios")
        Tabs.add(rate, text="Tarifas")
        Tabs.add(consultRoute, text="Consultar Ruta")

        # FRAMES
        frameCreate = LabelFrame(routes, text="Agregar")
        frameCreate.grid(row=0, column=0, columnspan=3, ipadx=20, pady=20)

        frameRead = LabelFrame(routes, text="Rutas")
        frameRead.grid(row=2, column=0, columnspan=10, ipadx=20, pady=20)

        frameUpdate = LabelFrame(routes, text="Modificar")
        frameUpdate.grid(row=0, column=4, columnspan=3, ipadx=20, pady=20)

        frameDelete = LabelFrame(routes, text="Eliminar")
        frameDelete.grid(row=0, column=8, columnspan=3,
                         pady=20, ipadx=20, ipady=10)

        # GRAPHICS ELEMENTS CREATE
        Label(frameCreate, text="Ruta inicial:").grid(row=0, column=0)
        self.rI = Entry(frameCreate)
        self.rI.grid(row=0, column=1)

        Label(frameCreate, text="Ruta final:").grid(row=1, column=0)
        self.rF = Entry(frameCreate)
        self.rF.grid(row=1, column=1)

        ttk.Button(frameCreate, text="Agregar", command=self.create).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msg = Label(frameCreate, text="", fg="green")
        self.msg.grid(row=4, column=0, columnspan=3, sticky=W+E)
        # GRAPHICS ELEMENTS READ
        self.table = ttk.Treeview(
            frameRead,
            columns=('#1', '#2', '#3'),
            show="headings")
        self.table.grid(row=0, column=0)
        self.table.heading("#1", text="Id", anchor=CENTER)
        self.table.heading("#2", text="Ruta inicial", anchor=CENTER)
        self.table.heading("#3", text="Ruta final", anchor=CENTER)
        self.table.column("#1", width=250, anchor=CENTER)
        self.table.column("#2", width=250, anchor=CENTER)
        self.table.column("#3", width=250, anchor=CENTER)

        # GRAPHICS ELEMENTS UPDATE
        Label(frameUpdate, text="Ruta inicial:").grid(row=0, column=0)
        Entry(frameUpdate).grid(row=0, column=1)

        Label(frameUpdate, text="Ruta final:").grid(row=1, column=0)
        Entry(frameUpdate).grid(row=1, column=1)

        ttk.Button(frameUpdate, text="Modificar").grid(
            row=2, columnspan=3, sticky=W+E)

        # GRAPHICS ELEMENTS DELETE
        Label(frameDelete, text="Ruta:").grid(row=1, column=0)
        Entry(frameDelete).grid(row=1, column=1)

        ttk.Button(frameDelete, text="Eliminar").grid(
            row=2, columnspan=3, sticky=W+E)

    # SELECT INFO FROM DB
    def select(self):
        registers = self.table.get_children()
        for reg in registers:
            self.table.delete(reg)

        sql = "SELECT * FROM `tbl_rutas`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            i = len(rows)
            for row in reversed(rows):
                self.table.insert('', 0, values=(i, row[0], row[1]))
                i = i-1
        except Exception as e:
            print(f"Error al consultar las rutas: {e}")
    # CREATE REGISTERS

    def create(self):
        if len(self.rI.get()) != 0 and len(self.rF.get()) != 0:
            query = "INSERT INTO `tbl_rutas`(`ruta_origen`, `ruta_destino`) VALUES ('" + \
                    self.rI.get()+"','"+self.rF.get()+"')"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msg['text'] = "Ruta agregada!"
                self.select()
            except Exception as e:
                self.msg['text'] = "Los campos deben estar llenos!"


if __name__ == "__main__":
    window = Tk()
    aplication = Window(window)
    aplication.select()
    window.mainloop()
