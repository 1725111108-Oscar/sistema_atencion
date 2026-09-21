class Nodo:
    """Un elemento de la fila: guarda un estudiante y apunta al siguiente."""
 
    def __init__(self, estudiante):
        self.estudiante = estudiante  # diccionario con los datos
        self.siguiente = None
 
 
class Fila:
    def __init__(self):
        self._frente = None   # primer nodo (el que se atiende primero)
        self._final = None    # último nodo (el que llegó más tarde)
        self._tamano = 0
 
    # a) Agregar un estudiante al final de la fila
    def agregar(self, estudiante):
        nodo = Nodo(estudiante)
        if self.esta_vacia():
            self._frente = nodo
        else:
            self._final.siguiente = nodo
        self._final = nodo
        self._tamano += 1
 
    # b) Atender al estudiante que está al frente (lo saca de la fila)
    def atender(self):
        if self.esta_vacia():
            return None
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:      # ya no quedó nadie
            self._final = None
        self._tamano -= 1
        return nodo.estudiante
 
    # c) Consultar quién es el siguiente (sin sacarlo)
    def consultar_siguiente(self):
        if self.esta_vacia():
            return None
        return self._frente.estudiante
 
    # d) Mostrar todos los estudiantes que esperan
    def mostrar(self):
        lista = []
        actual = self._frente
        while actual is not None:
            lista.append(actual.estudiante)
            actual = actual.siguiente
        return lista
 
    # e) Cuántos estudiantes están esperando
    def contar(self):
        return self._tamano
 
    # f) ¿La fila está vacía?
    def esta_vacia(self):
        return self._tamano == 0
 
    def existe_matricula(self, matricula):
        return any(e["matricula"] == matricula for e in self.mostrar())
 