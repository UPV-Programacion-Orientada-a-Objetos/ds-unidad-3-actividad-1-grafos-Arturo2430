# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string
from neuronet cimport GrafoDisperso

cdef class PyGrafoDisperso:
    cdef GrafoDisperso* c_grafo

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, str archivo):
        self.c_grafo.cargarDatos(archivo.encode('utf-8'))

    def obtener_nodo_mayor_grado(self):
        return self.c_grafo.obtenerNodoMayorGrado()

    def bfs(self, int inicio, int profundidad):
        cdef vector[pair[int, int]] aristas_visitadas
        cdef vector[int] nodos = self.c_grafo.bfs(inicio, profundidad, aristas_visitadas)
        
        # Convert C++ vector of pairs to Python list of tuples
        py_aristas = []
        for i in range(aristas_visitadas.size()):
            py_aristas.append((aristas_visitadas[i].first, aristas_visitadas[i].second))
            
        return nodos, py_aristas

    def obtener_numero_nodos(self):
        return self.c_grafo.obtenerNumeroNodos()

    def obtener_numero_aristas(self):
        return self.c_grafo.obtenerNumeroAristas()
