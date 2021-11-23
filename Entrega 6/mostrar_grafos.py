import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
import matplotlib.patches as mpatches




G = nx.read_gpickle("Wardrop_con_AVO.gpickle")

zonas_gdf = gps.read_file("eod.json")

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


rows = []
with open("OD_reducida.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
        
OD_reducida = {}
for row in rows:
    OD_reducida[(int(row[0]), int(row[1]))] = float(row[2])

zonas_avo = []
for key in OD_reducida:
 	zonas_avo.append(key[0])
 	zonas_avo.append(key[1])

zonas_avo = sorted(set(zonas_avo))

zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_avo)]

pos = nx.get_node_attributes(G, "pos")

# flujo_total = 0
# costo_total = 0
# costos = []
# flujos = []
# for i, edge in enumerate(G.edges):
#     flujo_total += G.edges[edge]["flujo"]
#     costo_total += G.edges[edge]["costo"]
#     costos.append(G.edges[edge]["costo"])
#     flujos.append(G.edges[edge]["flujo"])

# flujo_max = max(flujos)
# costo_max = max(costos)

# print(f"Flujo Total = {flujo_total}")
# print(f"Costo Total = {costo_total}")
# print(f"Flujo Máximo = {flujo_max}")
# print(f"Costo Máximo = {costo_max}")
# colors_flujo = []
# colors_costo = []
# flujo_max = 10367.73
# costo_max = 3054

# for i, edge in enumerate(G.edges):
# 	if G.edges[edge]["flujo"] < flujo_max/5:
# 		colors_flujo.append("blue")
# 	elif G.edges[edge]["flujo"] < 2*flujo_max/5:
# 		colors_flujo.append("green")
# 	elif G.edges[edge]["flujo"] < 3*flujo_max/5:
# 		colors_flujo.append("yellow")
# 	elif G.edges[edge]["flujo"] < 4*flujo_max/5:
# 		colors_flujo.append("orange")
# 	else:
# 		colors_flujo.append("red")

# 	if G.edges[edge]["costo"] < costo_max/5:
# 		colors_costo.append("blue")
# 	elif G.edges[edge]["costo"] < 2*costo_max/5:
# 		colors_costo.append("green")
# 	elif G.edges[edge]["costo"] < 3*costo_max/5:
# 		colors_costo.append("yellow")
# 	elif G.edges[edge]["costo"] < 4*costo_max/5:
# 		colors_costo.append("orange")
# 	else:
# 		colors_costo.append("red")

# fig, ax = plt.subplots()
# zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
# pos = nx.get_node_attributes(G, "pos")
# plt.suptitle("Flujo sin AVO")
# nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=5, arrowsize=6, edge_color=colors_flujo)
# intervalo1 = mpatches.Patch(color = "blue", label=f"[{0}, {round(flujo_max/5, 2)}]")
# intervalo2 = mpatches.Patch(color = "green", label=f"[{round(flujo_max/5, 2)}, {round(2*flujo_max/5, 2)}]")
# intervalo3 = mpatches.Patch(color = "yellow", label=f"[{round(2*flujo_max/5, 2)}, {round(3*flujo_max/5, 2)}]")
# intervalo4 = mpatches.Patch(color = "orange", label=f"[{round(3*flujo_max/5, 2)}, {round(4*flujo_max/5, 2)}]")
# intervalo5 = mpatches.Patch(color = "red", label=f"[{round(4*flujo_max/5, 2)}, {round(flujo_max, 2)}]")
# plt.legend(handles = [intervalo1, intervalo2, intervalo3, intervalo4, intervalo5], loc='upper right')
# # plt.savefig("Flujo sin AVO", dpi = 300, bbox_inches = 'tight')


# # Graficamos el grafo con los costos
# fig, ax = plt.subplots()
# zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
# pos = nx.get_node_attributes(G, "pos")
# plt.suptitle("Costo sin AVO")
# nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=5, arrowsize=6, edge_color=colors_costo)
# intervalo1 = mpatches.Patch(color = "blue", label=f"[{0}, {round(costo_max/5, 2)}]")
# intervalo2 = mpatches.Patch(color = "green", label=f"[{round(costo_max/5, 2)}, {round(2*costo_max/5, 2)}]")
# intervalo3 = mpatches.Patch(color = "yellow", label=f"[{round(2*costo_max/5, 2)}, {round(3*costo_max/5, 2)}]")
# intervalo4 = mpatches.Patch(color = "orange", label=f"[{round(3*costo_max/5, 2)}, {round(4*costo_max/5, 2)}]")
# intervalo5 = mpatches.Patch(color = "red", label=f"[{round(4*costo_max/5, 2)}, {round(costo_max, 2)}]")
# plt.legend(handles = [intervalo1, intervalo2, intervalo3, intervalo4, intervalo5], loc='upper right')
# # plt.savefig("Costo sin AVO", dpi = 300, bbox_inches = 'tight')




fig, ax = plt.subplots()
zonas_seleccionadas.plot(ax=ax, color = "#CDCDCD")
# zonas_gdf.plot(ax=ax, color = "#CDCDCD")
nx.draw(G, pos = pos, node_size = 5)
# gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth=3)
plt.suptitle("Santiago con AVO")
# plt.savefig("Zonas de Santiago", bbox_inches = 'tight') 

plt.show()




