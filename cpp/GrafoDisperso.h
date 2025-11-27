#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    // CSR format
    // Since it's an unweighted graph for this assignment (or weights are 1), we might not strictly need 'values' if we just care about connectivity.
    // However, standard CSR has values. The prompt says "3 vectors: values, column_indices, row_ptr".
    // If the input is just "NodeA NodeB", we can assume weight 1.
    std::vector<int> values; 
    std::vector<int> col_indices;
    std::vector<int> row_ptr;
    
    int num_nodos;
    int num_aristas;

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    int obtenerNodoMayorGrado() override;
    std::vector<int> bfs(int inicio, int profundidad, std::vector<std::pair<int, int>>& aristas_visitadas) override;
    int obtenerNumeroNodos() override;
    int obtenerNumeroAristas() override;
};

#endif // GRAFODISPERSO_H
