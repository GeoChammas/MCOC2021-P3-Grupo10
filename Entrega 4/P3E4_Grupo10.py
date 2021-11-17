import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import dijkstra_path 
from tabulate import tabulate


G = nx.DiGraph() 


OD = {
      ("A", "C") : 1100,
      ("A", "D") : 1110,
      ("A", "E") : 1020,
      ("B", "C") : 1140,
      ("B", "D") : 1160,
      ("C", "E") : 1170,
      ("C", "G") : 1180,
      ("D", "C") : 350,
      ("D", "E") : 1190,
      ("D", "G") : 1200
      }


# Agregamos nodos (nodes)
G.add_node("A", pos=[0,2]) 
G.add_node("B", pos=[0,1])
G.add_node("C", pos=[1,1])
G.add_node("D", pos=[1,0])
G.add_node("E", pos=[2,2])
G.add_node("G", pos=[2,1])


fr = lambda f: 10 + f/120
fs = lambda f: 14 + 3*f/240
ft = lambda f: 10 + f/240
fu = lambda f: 14 + 3*f/240
fv = lambda f: 10 + f/120
fw = lambda f: 14 + 3*f/240
fx = lambda f: 10 + f/240
fy = lambda f: 14 + 3*f/240
fz = lambda f: 10 + f/120


# Agregamos arcos (edges)
G.add_edge("A","B", costo=fr, flujo=0, costo2=0, label = "r: 10 + f/120")
G.add_edge("A","C", costo=fs, flujo=0, costo2=0, label = "s: 14 + 3f/240")
G.add_edge("B","C", costo=ft, flujo=0, costo2=0, label = "t: 10 + f/240")
G.add_edge("B","D", costo=fu, flujo=0, costo2=0, label = "u: 14 + 3f/240")
G.add_edge("D","C", costo=fv, flujo=0, costo2=0, label = "v: 10 + f/120")
G.add_edge("C","E", costo=fw, flujo=0, costo2=0, label = "w: 14 + 3f/240")
G.add_edge("C","G", costo=fx, flujo=0, costo2=0, label = "x: 10 + f/240")
G.add_edge("D","G", costo=fy, flujo=0, costo2=0, label = "y: 14 + 3f/240")
G.add_edge("G","E", costo=fz, flujo=0, costo2=0, label = "z: 10 + f/120")



def costo(ni,nf,att):
    funcosto_arco = att["costo"]
    flujo_arco = att["flujo"]
    return funcosto_arco(flujo_arco)

incrementos = [0.05]*18 + [0.01]*9 + [0.001]*9 + [0.0001]*10


for i, incremento in enumerate(incrementos):
    
    for key in OD:
        origen = key[0]
        destino = key[1]
        demanda_actual = OD[key]
    
        if demanda_actual > 0:
        
            path = dijkstra_path(G, origen, destino, weight = costo)
        
            Nparadas = len(path)
            
            for i in range(Nparadas-1):
                O = path[i]
                D = path[i+1]
                G.edges[O,D]["flujo"] += incremento*OD[key]
                G.edges[O,D]["flujo"] = round(G.edges[O,D]["flujo"],2)
                G.edges[O, D]["costo2"] = G.edges[O, D]["costo"](G.edges[O, D]["flujo"])
                G.edges[O, D]["costo2"] = round(G.edges[O, D]["costo2"],2)
                

pos = nx.get_node_attributes(G, "pos")
labels = nx.get_edge_attributes(G, "label")
labels_f = nx.get_edge_attributes(G, "flujo")
labels_c = nx.get_edge_attributes(G, "costo2")

edgelist = []
colores = []

# Grafo con los labels indicando las funciones de costo
plt.figure(1)
nx.draw(G, pos = pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.suptitle("Funciones de Costos")
plt.savefig("Funciones de Costos", bbox_inches = 'tight')
nx.draw_networkx_edges(G, pos)


# Grafo con los flujos de cada arco
plt.figure(2)
nx.draw(G, pos = pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_f)
plt.suptitle("Flujos")
plt.savefig("Flujos", bbox_inches = 'tight')
nx.draw_networkx_edges(G, pos)


# Grafo con los costos de cada arco
plt.figure(3)
nx.draw(G, pos = pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_c)
plt.suptitle("Costos")
nx.draw_networkx_edges(G, pos)
plt.savefig("Costos", bbox_inches = 'tight')
plt.show()


parOD = []
rutas_minimas = []
costos = []
for key in OD:
    origen = key[0]
    destino = key[1]
    ruta = []
    parOD.append(key[0] + key[1])
    path = nx.dijkstra_path(G, origen, destino, weight="costo2")
    costo_min = 0
    Nparada_min = len(path)
    for j_parada in range(Nparada_min-1):
        o = path[j_parada]
        d = path[j_parada + 1]
        costo_min += G.edges[o, d]["costo2"]
    simple_paths = nx.all_simple_paths(G, key[0], key[1])
    for i in simple_paths:
        for j in i:
            costo_shortest_path = 0
            Nparada_min = len(i)
            for j_parada in range(Nparada_min-1):
                o = i[j_parada]
                d = i[j_parada + 1]
                costo_shortest_path += G.edges[o, d]["costo2"]
        if costo_shortest_path < 1.01*costo_min and costo_shortest_path > 0.99*costo_min:
                    ruta.append(i)
    rutas_minimas.append(ruta)
    costos.append(costo_min)
        

table = {
    "Par OD": parOD,
    "Rutas Mínimas": rutas_minimas,
    "Costos": costos}     
        
print("\n \n \n")
print(tabulate(table, headers='keys', tablefmt='fancy_grid'))
        
