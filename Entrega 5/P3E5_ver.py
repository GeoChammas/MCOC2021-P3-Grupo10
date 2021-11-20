import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
import csv


G = nx.read_gpickle("Santiago_Grueso.gpickle")

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

# Eliminamos la zona que no tiene geometry, por lo que hace que el gps.clip no funcione
zonas_avo.remove(324)
zonas_avo.sort()


zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_avo)]


gdf_edges_seleccionados = gps.clip(gdf_edges, zonas_seleccionadas)


viajes=0
for key in OD_reducida:
    if key[0] == 324 or key[1] == 324:
        viajes+=0
    else:
        viajes+=OD_reducida[key]

print(f"Cantidad de viajes a asignar: {viajes}")

plt.figure()
ax = plt.subplot(111)
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)
gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth=3)
plt.suptitle("Avenida Américo Vespucio Oriente")
plt.savefig("AVO", bbox_inches = 'tight')
plt.show()
