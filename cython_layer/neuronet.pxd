from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

cdef extern from "../cpp/GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        int obtenerNodoMayorGrado()
        vector[int] bfs(int inicio, int profundidad, vector[pair[int, int]]& aristas_visitadas)
        int obtenerNumeroNodos()
        int obtenerNumeroAristas()
