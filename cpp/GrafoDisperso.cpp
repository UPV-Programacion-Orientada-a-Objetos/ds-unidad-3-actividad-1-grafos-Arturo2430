#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <map>
#include <queue>
#include <set>

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;

    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
        return;
    }

    // First pass: collect edges and find max node ID to determine size
    // Using an adjacency list temporarily to build CSR is easier, 
    // but for "massive" graphs we should try to be efficient.
    // However, sorting edges is necessary for CSR.
    // Let's read into a vector of pairs, sort, then build CSR.
    
    std::vector<std::pair<int, int>> edges;
    std::string line;
    int max_node_id = -1;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        int u, v;
        if (ss >> u >> v) {
            edges.push_back({u, v});
            if (u > max_node_id) max_node_id = u;
            if (v > max_node_id) max_node_id = v;
            
            // Assuming undirected graph for "robustness analysis" usually implies undirected,
            // but the prompt mentions "Diferencia entre grafos dirigidos y no dirigidos".
            // SNAP datasets like web-Google are directed.
            // Let's treat it as directed as per the input format usually implies.
            // If undirected is needed, we'd add {v, u} too.
            // The prompt says "web-Google.txt", which is a directed graph of web pages.
            // Let's stick to directed for now, or maybe add the reverse edge if we want undirected behavior.
            // "Recorridos de Grafos... BFS... para encontrar el camino más corto".
            // Let's assume directed as per the file format.
        }
    }
    file.close();

    num_nodos = max_node_id + 1;
    num_aristas = edges.size();

    // Sort edges by source node, then destination node
    std::sort(edges.begin(), edges.end());

    // Build CSR
    // row_ptr has size num_nodos + 1
    row_ptr.assign(num_nodos + 1, 0);
    col_indices.reserve(num_aristas);
    values.reserve(num_aristas); // All 1s

    int current_row = 0;
    for (const auto& edge : edges) {
        int u = edge.first;
        int v = edge.second;

        // Fill row_ptr for rows with no edges
        while (current_row < u) {
            current_row++;
            row_ptr[current_row] = col_indices.size();
        }

        col_indices.push_back(v);
        values.push_back(1);
    }
    
    // Fill remaining row_ptr
    while (current_row < num_nodos) {
        current_row++;
        row_ptr[current_row] = col_indices.size();
    }

    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos << " | Aristas: " << num_aristas << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida." << std::endl;
}

int GrafoDisperso::obtenerNodoMayorGrado() {
    int max_degree = -1;
    int max_node = -1;

    for (int i = 0; i < num_nodos; ++i) {
        int degree = row_ptr[i+1] - row_ptr[i];
        if (degree > max_degree) {
            max_degree = degree;
            max_node = i;
        }
    }
    return max_node;
}

std::vector<int> GrafoDisperso::bfs(int inicio, int profundidad, std::vector<std::pair<int, int>>& aristas_visitadas) {
    std::cout << "[C++ Core] Ejecutando BFS nativo desde " << inicio << " con profundidad " << profundidad << "..." << std::endl;
    
    std::vector<int> visitados;
    if (inicio < 0 || inicio >= num_nodos) return visitados;

    std::queue<std::pair<int, int>> q; // node, depth
    std::set<int> visited_set;

    q.push({inicio, 0});
    visited_set.insert(inicio);
    visitados.push_back(inicio);

    while (!q.empty()) {
        int u = q.front().first;
        int d = q.front().second;
        q.pop();

        if (d >= profundidad) continue;

        int start_idx = row_ptr[u];
        int end_idx = row_ptr[u+1];

        for (int i = start_idx; i < end_idx; ++i) {
            int v = col_indices[i];
            
            // Add edge to result
            aristas_visitadas.push_back({u, v});

            if (visited_set.find(v) == visited_set.end()) {
                visited_set.insert(v);
                visitados.push_back(v);
                q.push({v, d + 1});
            }
        }
    }
    
    std::cout << "[C++ Core] Nodos encontrados: " << visitados.size() << std::endl;
    return visitados;
}

int GrafoDisperso::obtenerNumeroNodos() {
    return num_nodos;
}

int GrafoDisperso::obtenerNumeroAristas() {
    return num_aristas;
}
