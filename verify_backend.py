from neuronet import PyGrafoDisperso
import os

def test_backend():
    print("Testing backend logic...")
    grafo = PyGrafoDisperso()
    
    # Create a temporary test file if not exists
    if not os.path.exists("test.txt"):
        with open("test.txt", "w") as f:
            f.write("0 1\n0 2\n1 2\n1 3\n2 4\n3 4\n3 5\n4 5\n4 6\n5 6\n")
            
    grafo.cargar_datos("test.txt")
    
    print(f"Nodos: {grafo.obtener_numero_nodos()}")
    print(f"Aristas: {grafo.obtener_numero_aristas()}")
    
    max_degree_node = grafo.obtener_nodo_mayor_grado()
    print(f"Nodo mayor grado: {max_degree_node}")
    
    # Expected max degree node in test.txt:
    # 0: 2
    # 1: 3
    # 2: 3
    # 3: 3
    # 4: 4 (neighbors: 2, 3, 5, 6) -> Wait, 4-6? 
    # Let's check test.txt content:
    # 0-1, 0-2
    # 1-2, 1-3
    # 2-4
    # 3-4, 3-5
    # 4-5, 4-6
    # 5-6
    # Degrees (undirected view, but our implementation is directed + sorted edges? No, I implemented directed in C++)
    # Wait, in C++ I did:
    # edges.push_back({u, v});
    # And then built CSR.
    # So it is a DIRECTED graph.
    # 0 -> 1, 2 (out-degree 2)
    # 1 -> 2, 3 (out-degree 2)
    # 2 -> 4 (out-degree 1)
    # 3 -> 4, 5 (out-degree 2)
    # 4 -> 5, 6 (out-degree 2)
    # 5 -> 6 (out-degree 1)
    # 6 -> (out-degree 0)
    
    # So max out-degree is 2 (nodes 0, 1, 3, 4).
    # My C++ implementation calculates degree as row_ptr[i+1] - row_ptr[i], which is out-degree.
    
    nodes, edges = grafo.bfs(0, 2)
    print(f"BFS from 0 depth 2 nodes: {nodes}")
    # BFS from 0 depth 2:
    # Depth 0: 0
    # Depth 1: 1, 2
    # Depth 2: (from 1: 2, 3), (from 2: 4) -> 2, 3, 4
    # Unique nodes: 0, 1, 2, 3, 4
    
    expected_nodes = {0, 1, 2, 3, 4}
    assert set(nodes) == expected_nodes, f"Expected {expected_nodes}, got {set(nodes)}"
    print("BFS verification passed!")

if __name__ == "__main__":
    test_backend()
