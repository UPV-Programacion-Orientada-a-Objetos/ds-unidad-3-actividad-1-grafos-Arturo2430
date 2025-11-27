#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <vector>
#include <string>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual int obtenerNodoMayorGrado() = 0;
    virtual std::vector<int> bfs(int inicio, int profundidad, std::vector<std::pair<int, int>>& aristas_visitadas) = 0;
    virtual int obtenerNumeroNodos() = 0;
    virtual int obtenerNumeroAristas() = 0;
};

#endif // GRAFOBASE_H
