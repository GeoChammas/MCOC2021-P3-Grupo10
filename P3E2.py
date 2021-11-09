import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph() #Graph asume bidireccionalidad en todos los arcos

# Agregamos nodos (nodes) con sus coordenadas
G.add_node("0", pos = [1,2] )
G.add_node("1", pos = [4,3] )
G.add_node("2", pos = [1,6] )
G.add_node("3", pos = [7,3] )
G.add_node("4", pos = [10,1] )
G.add_node("5", pos = [0,10] )
G.add_node("6", pos = [4,0] )
G.add_node("7", pos = [5,8] )
G.add_node("8", pos = [9,7] )
G.add_node("9", pos = [8,10] )

# Agregamos arcos (edges) con el atributo de tiempo = distancia/velocidad
G.add_edge("0","1", tiempo = np.sqrt((1-4)**2 + (2-3)**2)/40)
G.add_edge("0","2", tiempo = np.sqrt((1-1)**2 + (2-6)**2)/120)
G.add_edge("0","6", tiempo = np.sqrt((1-4)**2 + (2-0)**2)/120)
G.add_edge("1","2", tiempo = np.sqrt((4-1)**2 + (3-6)**2)/40)
G.add_edge("1","3", tiempo = np.sqrt((4-7)**2 + (3-3)**2)/60)
G.add_edge("1","7", tiempo = np.sqrt((4-5)**2 + (3-8)**2)/40)
G.add_edge("2","5", tiempo = np.sqrt((1-0)**2 + (6-10)**2)/40)
G.add_edge("3","4", tiempo = np.sqrt((7-10)**2 + (3-1)**2)/60)
G.add_edge("3","6", tiempo = np.sqrt((7-4)**2 + (3-0)**2)/40)
G.add_edge("3","7", tiempo = np.sqrt((7-5)**2 + (3-8)**2)/60)
G.add_edge("3","8", tiempo = np.sqrt((7-9)**2 + (3-7)**2)/40)
G.add_edge("4","6", tiempo = np.sqrt((10-4)**2 + (1-0)**2)/120)
G.add_edge("4","8", tiempo = np.sqrt((10-9)**2 + (1-7)**2)/120)
G.add_edge("5","7", tiempo = np.sqrt((0-5)**2 + (10-8)**2)/120)
G.add_edge("7","9", tiempo = np.sqrt((5-8)**2 + (8-10)**2)/60)
G.add_edge("8","9", tiempo = np.sqrt((9-8)**2 + (7-10)**2)/60)

# Coordenadas de los nodos
pos = nx.get_node_attributes(G, "pos")

colores = []
edgelist = []
rgb = lambda h: tuple(int(h[i:i+2], 16)/256 for i in (0, 2, 4))

#Definimos los colores de los arcos
for ni, nf in G.edges:
    if (ni=="0" and nf=="2") or (ni=="0" and nf=="6") or (ni=="4" and nf=="6") or (ni=="4" and nf=="8") or (ni=="5" and nf=="7"):
        colores.append(rgb("7C7C7C")) #gris
    elif (ni=="1" and nf=="3") or (ni=="3" and nf=="4") or (ni=="3" and nf=="7") or (ni=="7" and nf=="9") or (ni=="8" and nf=="9"):
        colores.append(rgb("00701A")) #verde
    else:
        colores.append(rgb("6C4E09"))
    edgelist.append((ni,nf)) #café


x = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]
y = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]


# Se grafica la red
fig, ax = plt.subplots()
nx.draw(G, pos = pos, with_labels=True)
nx.draw_networkx_edges(G, pos, edgelist=edgelist, edge_color=colores, width = 2, ax=ax)
ax.grid()
ax.set_axisbelow(True)
limits=plt.axis('on')
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
ax.set_xlabel("X [km]")
ax.set_ylabel("Y [km]")
plt.xticks(x, x)
plt.yticks(y, y)
plt.savefig("fig1", bbox_inches = 'tight')
plt.show()








