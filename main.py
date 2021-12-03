from tkinter import *
from tkinter import ttk
import random
from typing_extensions import Self
from tkinter import messagebox as MessageBox
import pymysql.cursors


class Vertice:
    """Clase que define los vértices de los gráficas"""

    def __init__(self, i):
        """Método que inicializa el vértice con sus atributos
        id = identificador
        vecinos = lista de los vértices con los que está conectado por una arista
        visitado = flag para saber si fue visitado o no
        padre = vértice visitado un paso antes
        costo = valor que tiene recorrerlo"""
        self.id = i
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.costo = float('inf')

    def agregarVecino(self, v, p):
        """Método que agrega los vertices que se encuentre conectados por una arista a la lista de vecinos 
        de un vertice, revisando si éste aún no se encuentra en la lista de vecinos"""
        if v not in self.vecinos:
            self.vecinos.append([v, p])


class Grafica:
    """Clase que define los vértices de las gráficas"""

    def __init__(self):
        """vertices = diccionario con los vertices de la grafica"""
        self.vertices = {}

    def agregarVertice(self, id):
        """Método que agrega vértices, recibiendo el índice revisando si éste no existe en el diccionario de vértices"""
        if id not in self.vertices:
            self.vertices[id] = Vertice(id)

    def agregarArista(self, a, b, p):
        """Método que agrega aristas, recibiendo el índice de dos vertices y revisando si existen estos en la lista
        de vertices, además de recibir el peso de la arista , el cual se asigna a ambos vértices por medio del método
        agregar vecino"""
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecino(b, p)
            self.vertices[b].agregarVecino(a, p)

    def imprimirGrafica(self):
        """Método que imprime el gráfo completo arista por arista con todas sus características(incluye heurística)"""
        for v in self.vertices:
            print("El costo del vértice "+str(self.vertices[v].id)+" es " + str(
                self.vertices[v].costo)+" llegando desde "+str(self.vertices[v].padre))

    def camino(self, a, b):
        """Método que va guardando en la lista llamada 'camino' los nodos en el orden que sean visitados y actualizando dicha
        lista con los vértices con el menor costo"""
        camino = []
        actual = b
        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre

        return [camino, self.vertices[b].costo]

    def minimo(self, l):
        """Método que recibe la lista de los vertices no visitados, revisa si su longitud es mayor a cero(indica que 
        aún hay vértices sin visitar), y realiza comparaciones de los costos de cada vértice en ésta lista para encontrar
        el de menor costo"""
        if len(l) > 0:
            m = self.vertices[l[0]].costo
            v = l[0]
            for e in l:
                if m > self.vertices[e].costo:
                    m = self.vertices[e].costo
                    v = e
            return v
        return None

    def dijkstra(self, a):
        """Método que sigue el algortimo de Dijkstra
        1. Asignar a cada nodo una distancia tentativa: 0 para el nodo inicial e infinito para todos los nodos restantes. Predecesor nulo para todos.
        2. Establecer al nodo inicial como nodo actual y crear un conjunto de nodos no visitados.
        3. Para el nodo actual, considerar a todos sus vecinos no visitados con peso w.
                a) Si la distancia del nodo actual sumada al peso w es menor que la distancia tentativa actual de ese vecino,
                sobreescribir la distancia con la suma obtenida y guardar al nodo actual como predecesor del vecino
        4. Cuando se termina de revisar a todos los vecino del nodo actual, se marca como visitado y se elimina del conjunto no  visitado
        5. Continúa la ejecución hasta vaciar al conjunto no visitado
        6. Seleccionar el nodo no visitado con menor distancia tentativa y marcarlo como el nuevo nodo actual. Regresar al punto 3
        """
        if a in self.vertices:
            # 1 y 2
            self.vertices[a].costo = 0
            actual = a
            noVisitados = []

            for v in self.vertices:
                if v != a:
                    self.vertices[v].costo = float('inf')
                self.vertices[v].padre = None
                noVisitados.append(v)

            while len(noVisitados) > 0:
                # 3
                for vec in self.vertices[actual].vecinos:
                    if self.vertices[vec[0]].visitado == False:
                        # 3.a
                        if self.vertices[actual].costo + vec[1] < self.vertices[vec[0]].costo:
                            self.vertices[vec[0]
                                          ].costo = self.vertices[actual].costo + vec[1]
                            self.vertices[vec[0]].padre = actual

                # 4
                self.vertices[actual].visitado = True
                noVisitados.remove(actual)

                # 5 y 6
                actual = self.minimo(noVisitados)
        else:
            return False


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

        # FRAMES ROUTES
        frameCreate = LabelFrame(routes, text="Agregar")
        frameCreate.grid(row=0, column=0, columnspan=3)

        frameRead = LabelFrame(routes, text="Rutas")
        frameRead.grid(row=2, column=0, columnspan=10, padx=15)

        frameUpdate = LabelFrame(routes, text="Modificar")
        frameUpdate.grid(row=0, column=3, columnspan=3)

        frameDelete = LabelFrame(routes, text="Eliminar")
        frameDelete.grid(row=0, column=6, columnspan=3)

        # FRAMES MUNICIPIOS
        frameCreateM = LabelFrame(municipalitys, text="Agregar")
        frameCreateM.grid(row=0, column=0, columnspan=3, padx=20)

        frameReadM = LabelFrame(municipalitys, text="Municipios")
        frameReadM.grid(row=2, column=0, columnspan=10, padx=20)

        frameUpdateM = LabelFrame(municipalitys, text="Modificar")
        frameUpdateM.grid(row=0, column=3, columnspan=3, padx=20)

        frameDeleteM = LabelFrame(municipalitys, text="Eliminar")
        frameDeleteM.grid(row=0, column=6, columnspan=3, padx=20)

        # FRAMES RATE
        frameCreateR = LabelFrame(rate, text="Agregar")
        frameCreateR.grid(row=0, column=0, columnspan=3, padx=20)

        frameReadR = LabelFrame(rate, text="Tarifas")
        frameReadR.grid(row=2, column=0, columnspan=10, padx=20)

        frameUpdateR = LabelFrame(rate, text="Modificar")
        frameUpdateR.grid(row=0, column=3, columnspan=3, padx=20)

        frameDeleteR = LabelFrame(rate, text="Eliminar")
        frameDeleteR.grid(row=0, column=6, columnspan=3, padx=20)

        # FRAMES CONSULT ROUTE
        frameCreateCR = LabelFrame(consultRoute, text="Consultar")
        frameCreateCR.grid(row=0, column=0, columnspan=3)

        # GRAPHICS ELEMENTS FRAME RUTAS
        # CREATE
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

        # READ
        self.table = ttk.Treeview(
            frameRead,
            columns=('#1', '#2', '#3', '#4'),
            show="headings")
        self.table.grid(row=0, column=0)
        self.table.heading("#1", text="Id", anchor=CENTER)
        self.table.heading("#2", text="Ruta inicial", anchor=CENTER)
        self.table.heading("#3", text="Ruta final", anchor=CENTER)
        self.table.heading("#4", text="Km", anchor=CENTER)
        self.table.column("#1", width=200, anchor=CENTER)
        self.table.column("#2", width=200, anchor=CENTER)
        self.table.column("#3", width=200, anchor=CENTER)
        self.table.column("#4", width=200, anchor=CENTER)

        # UPDATE
        Label(frameUpdate, text="Ruta actual:").grid(row=0, column=0)
        self.oM = Entry(frameUpdate)
        self.oM.grid(row=0, column=1)

        Label(frameUpdate, text="Ruta nueva:").grid(row=1, column=0)
        self.nM = Entry(frameUpdate)
        self.nM.grid(row=1, column=1)

        ttk.Button(frameUpdate, text="Modificar", command=self.update).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgU = Label(frameUpdate, text="", fg="green")
        self.msgU.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # DELETE
        Label(frameDelete, text="Ruta origen:").grid(row=0, column=0)
        self.rO = Entry(frameDelete)
        self.rO.grid(row=0, column=1)

        Label(frameDelete, text="Ruta destino:").grid(row=1, column=0)
        self.rD = Entry(frameDelete)
        self.rD.grid(row=1, column=1)

        ttk.Button(frameDelete, text="Eliminar", command=self.delete).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgD = Label(frameDelete, text="", fg="green")
        self.msgD.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # GRAPHICS ELEMENTS FRAME MUNICIPIOS
        # CREATE
        Label(frameCreateM, text="Municipio:").grid(row=0, column=0)
        self.mun = Entry(frameCreateM)
        self.mun.grid(row=0, column=1)

        ttk.Button(frameCreateM, text="Agregar", command=self.createM).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgMC = Label(frameCreateM, text="", fg="green")
        self.msgMC.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # READ
        self.tableM = ttk.Treeview(
            frameReadM,
            columns=('#1', '#2'),
            show="headings")
        self.tableM.grid(row=0, column=0)
        self.tableM.heading("#1", text="Id", anchor=CENTER)
        self.tableM.heading("#2", text="Municipios", anchor=CENTER)
        self.tableM.column("#1", width=250, anchor=CENTER)
        self.tableM.column("#2", width=250, anchor=CENTER)

        # UPDATE
        Label(frameUpdateM, text="Municipio actual:").grid(row=0, column=0)
        self.munA = Entry(frameUpdateM)
        self.munA.grid(row=0, column=1)

        Label(frameUpdateM, text="Munucipio nuevo:").grid(row=1, column=0)
        self.munN = Entry(frameUpdateM)
        self.munN.grid(row=1, column=1)

        ttk.Button(frameUpdateM, text="Modificar", command=self.updateM).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgUM = Label(frameUpdateM, text="", fg="green")
        self.msgUM.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # DELETE
        Label(frameDeleteM, text="Municipio:").grid(row=0, column=0)
        self.munD = Entry(frameDeleteM)
        self.munD.grid(row=0, column=1)

        ttk.Button(frameDeleteM, text="Eliminar", command=self.deleteM).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgDM = Label(frameDeleteM, text="", fg="green")
        self.msgDM.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # GRAPHICS ELEMENTS FRAME RATE
        # CREATE
        Label(frameCreateR, text="Tarifa:").grid(row=0, column=0)
        self.tar = Entry(frameCreateR)
        self.tar.grid(row=0, column=1)

        ttk.Button(frameCreateR, text="Agregar", command=self.createR).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgCR = Label(frameCreateR, text="", fg="green")
        self.msgCR.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # READ
        self.tableR = ttk.Treeview(
            frameReadR,
            columns=('#1', '#2'),
            show="headings")
        self.tableR.grid(row=0, column=0)
        self.tableR.heading("#1", text="Id", anchor=CENTER)
        self.tableR.heading("#2", text="Tarifas", anchor=CENTER)
        self.tableR.column("#1", width=250, anchor=CENTER)
        self.tableR.column("#2", width=250, anchor=CENTER)

        # UPDATE
        Label(frameUpdateR, text="Tarifa actual:").grid(row=0, column=0)
        self.tarA = Entry(frameUpdateR)
        self.tarA.grid(row=0, column=1)

        Label(frameUpdateR, text="Tarifa nueva:").grid(row=1, column=0)
        self.tarN = Entry(frameUpdateR)
        self.tarN.grid(row=1, column=1)

        ttk.Button(frameUpdateR, text="Modificar", command=self.updateR).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgUR = Label(frameUpdateR, text="", fg="green")
        self.msgUR.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # DELETE
        Label(frameDeleteR, text="Tarifa:").grid(row=0, column=0)
        self.tarD = Entry(frameDeleteR)
        self.tarD.grid(row=0, column=1)

        ttk.Button(frameDeleteR, text="Eliminar", command=self.deleteR).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgDR = Label(frameDeleteR, text="", fg="green")
        self.msgDR.grid(row=4, column=0, columnspan=3, sticky=W+E)

        # GRAPHICS ELEMENTS CONSULT ROUTE
        Label(frameCreateCR, text="Municipio origen:").grid(row=0, column=0)
        self.munOrigen = Entry(frameCreateCR)
        self.munOrigen.grid(row=0, column=1)

        Label(frameCreateCR, text="Municipio destino:").grid(row=1, column=0)
        self.munDestino = Entry(frameCreateCR)
        self.munDestino.grid(row=1, column=1)

        ttk.Button(frameCreateCR, text="Consultar", command=self.consult).grid(
            row=2, columnspan=3, sticky=W+E)
        self.msgCLTR = Label(frameCreateCR, text="", fg="green")
        self.msgCLTR.grid(row=4, column=0, columnspan=3, sticky=W+E)

    # BD ROUTES
    def selectRoutes(self):
        sql = "SELECT * FROM `tbl_rutas`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error al consultar las rutas: {e}")

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
                self.table.insert('', 0, values=(i, row[0], row[1], row[2]))
                i = i-1
        except Exception as e:
            print(f"Error al consultar las rutas: {e}")

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

    def update(self):
        if len(self.oM.get()) != 0 and len(self.nM.get()) != 0:
            query = "UPDATE tbl_rutas SET ruta_origen = '"+self.nM.get() + \
                "' WHERE ruta_origen = '"+self.oM.get()+"'"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msgU['text'] = "Ruta actualizada!"
                self.select()
            except Exception as e:
                self.msgU['text'] = "Los campos deben estar llenos!"

    def delete(self):
        if len(self.rO.get()) != 0 and len(self.rD.get()) != 0:
            sql = "DELETE FROM `tbl_rutas` WHERE ruta_origen = '" + \
                self.rO.get()+"' and ruta_destino = '"+self.rD.get()+"'"
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                self.msgD['text'] = "Ruta eliminada!"
                self.select()
            except Exception as e:
                self.msgD['text'] = "Los campos deben estar llenos!"

    # BD MUNICIPIOS
    def selectMunicipalitys(self):
        sql = "SELECT * FROM `tbl_municipios`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error al consultar los municipios: {e}")

    def selectM(self):
        registers = self.tableM.get_children()
        for reg in registers:
            self.tableM.delete(reg)

        sql = "SELECT * FROM `tbl_municipios`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            i = len(rows)
            for row in reversed(rows):
                self.tableM.insert('', 0, values=(i, row[0]))
                i = i-1
        except Exception as e:
            print(f"Error al consultar los municipios: {e}")

    def createM(self):
        if len(self.mun.get()) != 0:
            query = "INSERT INTO `tbl_municipios`(`nombre_municipio`) VALUES ('" + \
                self.mun.get()+"')"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msgMC['text'] = "Municipio agregado!"
                self.selectM()
            except Exception as e:
                self.msgMC['text'] = "Los campos deben estar llenos!"

    def updateM(self):
        if len(self.munA.get()) != 0 and len(self.munN.get()) != 0:
            query = "UPDATE tbl_municipios SET nombre_municipio = '"+self.munN.get() + \
                "' WHERE nombre_municipio = '"+self.munA.get()+"'"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msgUM['text'] = "Municipio actualizado!"
                self.selectM()
            except Exception as e:
                self.msgUM['text'] = "Los campos deben estar llenos!"

    def deleteM(self):
        if len(self.munD.get()) != 0:
            sql = "DELETE FROM `tbl_municipios` WHERE nombre_municipio = '" + self.munD.get() + \
                "'"
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                self.msgDM['text'] = "Muncipio eliminado!"
                self.selectM()
            except Exception as e:
                self.msgDM['text'] = "Los campos deben estar llenos!"

    # BD TARIFAS
    def selectRates(self):
        sql = "SELECT * FROM `tbl_tarifas`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error al consultar las tarifas: {e}")

    def selectR(self):
        registers = self.tableR.get_children()
        for reg in registers:
            self.tableR.delete(reg)

        sql = "SELECT * FROM `tbl_tarifas`"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            i = len(rows)
            for row in reversed(rows):
                self.tableR.insert('', 0, values=(i, row[0]))
                i = i-1
        except Exception as e:
            print(f"Error al consultar las tarifas: {e}")

    def createR(self):
        if len(self.tar.get()) != 0:
            query = "INSERT INTO `tbl_tarifas`(`tarifa`) VALUES ('" + \
                self.tar.get()+"')"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msgCR['text'] = "Tarifa agregada!"
                self.selectR()
            except Exception as e:
                self.msgCR['text'] = "Los campos deben estar llenos!"

    def updateR(self):
        if len(self.tarA.get()) != 0 and len(self.tarN.get()) != 0:
            query = "UPDATE tbl_tarifas SET tarifa = '"+self.tarN.get() + \
                "' WHERE tarifa = '"+self.tarA.get()+"'"
            try:
                self.cursor.execute(query)
                self.connection.commit()
                self.msgUR['text'] = "Tarifa actualizada!"
                self.selectR()
            except Exception as e:
                self.msgUR['text'] = "Los campos deben estar llenos!"

    def deleteR(self):
        if len(self.tarD.get()) != 0:
            sql = "DELETE FROM `tbl_tarifas` WHERE tarifa = '" + self.tarD.get() + "'"
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                self.msgDR['text'] = "Tarifa eliminada!"
                self.selectR()
            except Exception as e:
                self.msgDR['text'] = "Los campos deben estar llenos!"

    # CONSULT
    def consult(self):
        g = Grafica()
        routesDB = list(self.selectRoutes())
        munDB = list(self.selectMunicipalitys())

        # Pasamos de tuplas a listas
        mun_list = []
        routes_list = []

        for mun in munDB:
            mun_list.append(list(mun))
        for rut in routesDB:
            routes_list.append(list(rut))

         # Pasamos las listsa a una sola de cada info
        municipalitys = []
        route_origin = []  # ✅
        route_destination = []  # ✅
        kilometers = []  # ✅

        for mun, rutas in zip(mun_list, routes_list):
            municipalitys.append(mun[0])
            route_origin.append(rutas[0])
            route_destination.append(rutas[1])
            kilometers.append(int(rutas[2]))

        # Pasamos los valores de las listas para obtener el camino más corto
        for mun in municipalitys:
            g.agregarVertice(mun)

        for ro, rd, km in zip(route_origin, route_destination, kilometers):
            g.agregarArista(ro, rd, km)

        # Imprimimos el resultado final
        costo = random.randint(12, 30)
        g.dijkstra(self.munOrigen.get())
        result = g.camino(self.munOrigen.get(), self.munDestino.get())
        print(result)
        MessageBox.showinfo("Ruta mas corta!",
                            f'Ruta: {result[0]}  Costo: {costo} Km recorridos {result[1]}')


if __name__ == "__main__":
    window = Tk()
    aplication = Window(window)
    aplication.select()
    aplication.selectM()
    aplication.selectR()
    window.mainloop()
