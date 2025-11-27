import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from neuronet import PyGrafoDisperso
import time
import os

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Redes Masivas")
        self.root.geometry("900x700")
        
        # Dark Theme Colors (IDE Style)
        self.bg_color = "#1e1f22"
        self.fg_color = "#bcbec4"
        self.comp_bg = "#2b2d30"
        self.accent_color = "#3574f0"
        self.button_bg = "#4e5157" # Slightly lighter for buttons
        
        self.root.configure(bg=self.bg_color)

        self.grafo = None
        self.filename = None

        self.create_widgets()

    def create_widgets(self):
        # Styles
        label_style = {"bg": self.bg_color, "fg": self.fg_color, "font": ("Segoe UI", 10)}
        button_style = {"bg": self.button_bg, "fg": self.fg_color, "activebackground": self.accent_color, "activeforeground": "white", "relief": tk.FLAT, "padx": 10, "pady": 5}
        entry_style = {"bg": self.comp_bg, "fg": self.fg_color, "insertbackground": self.fg_color, "relief": tk.FLAT}
        frame_style = {"bg": self.bg_color}

        # Frame for controls
        control_frame = tk.Frame(self.root, **frame_style)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

        # Load Button
        self.btn_load = tk.Button(control_frame, text="Cargar Dataset", command=self.load_dataset, **button_style)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        # Info Label
        self.lbl_info = tk.Label(control_frame, text="No se ha cargado ningún dataset.", **label_style)
        self.lbl_info.pack(side=tk.LEFT, padx=15)

        # Analysis Frame
        analysis_frame = tk.LabelFrame(self.root, text="Análisis y Simulación", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11, "bold"))
        analysis_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Max Degree Button
        self.btn_max_degree = tk.Button(analysis_frame, text="Nodo Mayor Grado", command=self.find_max_degree, state=tk.DISABLED, **button_style)
        self.btn_max_degree.pack(side=tk.LEFT, padx=10, pady=15)

        # BFS Controls
        tk.Label(analysis_frame, text="Nodo Inicio:", **label_style).pack(side=tk.LEFT, padx=5)
        self.entry_start_node = tk.Entry(analysis_frame, width=10, **entry_style)
        self.entry_start_node.pack(side=tk.LEFT, padx=5)

        tk.Label(analysis_frame, text="Profundidad:", **label_style).pack(side=tk.LEFT, padx=5)
        self.entry_depth = tk.Entry(analysis_frame, width=5, **entry_style)
        self.entry_depth.pack(side=tk.LEFT, padx=5)

        self.btn_bfs = tk.Button(analysis_frame, text="Ejecutar BFS", command=self.run_bfs, state=tk.DISABLED, **button_style)
        self.btn_bfs.pack(side=tk.LEFT, padx=15)

        # Results Area
        self.txt_results = tk.Text(self.root, height=15, bg=self.comp_bg, fg=self.fg_color, insertbackground=self.fg_color, relief=tk.FLAT, font=("Consolas", 10))
        self.txt_results.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def load_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return

        self.filename = file_path
        
        # Get file size
        size_bytes = os.path.getsize(self.filename)
        size_mb = size_bytes / (1024 * 1024)
        
        self.grafo = PyGrafoDisperso()
        
        self.log(f"Cargando dataset: {os.path.basename(self.filename)} ({size_mb:.2f} MB)...")
        self.root.update()
        
        start_time = time.time()
        self.grafo.cargar_datos(self.filename)
        end_time = time.time()
        
        num_nodos = self.grafo.obtener_numero_nodos()
        num_aristas = self.grafo.obtener_numero_aristas()
        
        self.lbl_info.config(text=f"Nodos: {num_nodos:,} | Aristas: {num_aristas:,} | Tamaño: {size_mb:.2f} MB")
        self.log(f"Carga completa en {end_time - start_time:.4f}s.")
        self.log(f"Grafo cargado: {num_nodos:,} nodos, {num_aristas:,} aristas.")
        
        self.btn_max_degree.config(state=tk.NORMAL)
        self.btn_bfs.config(state=tk.NORMAL)

    def find_max_degree(self):
        if not self.grafo:
            return
        
        node = self.grafo.obtener_nodo_mayor_grado()
        self.log(f"Nodo con mayor grado: {node}")
        messagebox.showinfo("Resultado", f"El nodo con mayor grado es: {node}")

    def run_bfs(self):
        if not self.grafo:
            return
            
        try:
            start_node = int(self.entry_start_node.get())
            depth = int(self.entry_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
            return

        self.log(f"Ejecutando BFS desde {start_node} con profundidad {depth}...")
        self.root.update()
        
        start_time = time.time()
        nodes, edges = self.grafo.bfs(start_node, depth)
        end_time = time.time()
        
        self.log(f"BFS completado en {end_time - start_time:.4f}s.")
        self.log(f"Subgrafo resultante: {len(nodes)} nodos, {len(edges)} aristas.")
        
        self.visualize_subgraph(nodes, edges, start_node)

    def visualize_subgraph(self, nodes, edges, start_node):
        if len(nodes) > 5000:
            messagebox.showwarning("Subgrafo demasiado grande", 
                                   f"El subgrafo tiene {len(nodes)} nodos. La visualización está limitada a 5000 nodos para evitar congelar la aplicación.\n\n"
                                   "Intente reducir la profundidad de búsqueda.")
            return

        if len(nodes) > 1000:
            if not messagebox.askyesno("Advertencia", "El subgrafo es grande (>1000 nodos). ¿Desea visualizarlo? Puede ser lento."):
                return

        try:
            import scipy
        except ImportError:
            messagebox.showerror("Error", "La librería 'scipy' es necesaria para visualizar grafos complejos. Por favor instálela.")
            return

        G = nx.Graph() # Or DiGraph if we want directed
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        plt.figure(figsize=(10, 8), facecolor=self.bg_color)
        ax = plt.gca()
        ax.set_facecolor(self.bg_color)
        
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=50, node_color=self.accent_color, edgecolors='white')
        # Highlight start node
        nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_size=150, node_color='#e05555', edgecolors='white')
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color=self.fg_color)
        
        # Draw labels if small enough
        if len(nodes) < 50:
            nx.draw_networkx_labels(G, pos, font_color='white', font_size=8)
            
        plt.title(f"BFS desde Nodo {start_node} (Nodos: {len(nodes)}, Aristas: {len(edges)})", color=self.fg_color)
        plt.show()

    def log(self, message):
        self.txt_results.insert(tk.END, message + "\n")
        self.txt_results.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
