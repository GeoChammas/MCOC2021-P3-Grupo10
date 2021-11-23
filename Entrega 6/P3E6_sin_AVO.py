import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
import matplotlib.patches as mpatches



def costo(n1, n2, att_arco):
   
    usar_arco_numero = 0
    arco = att_arco[usar_arco_numero]
    
    f = arco["flujo"]

    if "lanes" in arco:
        if str(type(arco["lanes"])) == "<class 'list'>":
            arco["lanes"] = [int(i) for i in arco["lanes"]]
            p = np.average(arco["lanes"])
        else:
            p = int(arco["lanes"]) 
    else:
        p = 1
    if p<=0:
        p=1
	
    q = f/5400
	
    if "length" in arco:
        length = float(arco["length"])
    else:
        length = 100

    if "highway" in arco:
        street_type = arco["highway"]
    else:
        street_type = "NO ROUTE"

    if street_type == "motorway":
        vel = 25
        u = 5
    elif street_type == "primary" or street_type == "secondary":
        vel = 15
        u = 3
    else:
        vel = 8
        u = 2
	
    costo = length/vel + (5-u)*12 + (900/(u*p))*(10*q - u*p +np.sqrt((10*q-u*p)**2 + q/9))

    return costo



G = nx.read_gpickle("Santiago_sin_AVO.gpickle")

zonas_gdf = gps.read_file("eod.json")

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


# Abrimos la matriz OD reducida
rows = []
with open("OD_reducida.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
        
OD_reducida = {}
for row in rows:
    OD_reducida[(int(row[0]), int(row[1]))] = float(row[2])
    

# Definimos las posiciones de los nodos
for i, node in enumerate(G.nodes):
    cx_nodo = G.nodes[node]["x"]
    cy_nodo = G.nodes[node]["y"]
    pos = [cx_nodo, cy_nodo]
    G.nodes[node]["pos"] =  pos
        
pos = nx.get_node_attributes(G, "pos")

nx.set_edge_attributes(G, 0, "flujo")
nx.set_edge_attributes(G, 0, "costo")

zonas_avo = []
for key in OD_reducida:
	zonas_avo.append(key[0])
	zonas_avo.append(key[1])

zonas_avo = sorted(set(zonas_avo))

zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_avo)]


incrementos = [0.1]*9 + [0.01]*9 + [0.001]*9 + [0.0001]*10

for incremento in incrementos:
	for key in OD_reducida:

		origen = key[0]
		destino = key[1]
		demanda_actual = OD_reducida[key]
		
		#ORIGEN
		nodos_origen = gps.sjoin(gdf_nodes, zonas_seleccionadas[zonas_seleccionadas.ID==origen], op="within")
		try:
			origen = nodos_origen.sample().index[0]
		except:
			try:
				p = zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].representative_point()
				cx_zona_origen, cy_zona_origen = float(p.x), float(p.y)
			except:
				try:
					cx_zona_origen, cy_zona_origen = float(zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].centroid.x), float(zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].centroid.y)
					
					distancia_minima = np.infty

					for i, node in enumerate(G.nodes):
						cx_nodo = G.nodes[node]["x"]
						cy_nodo = G.nodes[node]["y"]
				
						dist_nodo = np.sqrt((cx_nodo-cx_zona_origen)**2 + (cy_nodo-cy_zona_origen)**2)
				
						if dist_nodo < distancia_minima:
							distancia_minima = dist_nodo
							origen = node

				except:
					continue


		#DESTINO
		nodos_destino = gps.sjoin(gdf_nodes, zonas_seleccionadas[zonas_seleccionadas.ID==destino], op="within")
		try:
			destino = nodos_destino.sample().index[0]
		except:
			try:
				p = zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].representative_point()
				cx_zona_destino, cy_zona_destino = float(p.x), float(p.y)
			except:
				try:
					cx_zona_destino, cy_zona_destino = float(zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].centroid.x), float(zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].centroid.y)
				
					distancia_minima = np.infty

					for i, node in enumerate(G.nodes):
						cx_nodo = G.nodes[node]["x"]
						cy_nodo = G.nodes[node]["y"]
				
						dist_nodo = np.sqrt((cx_nodo-cx_zona_destino)**2 + (cy_nodo-cy_zona_destino)**2)
				
						if dist_nodo < distancia_minima:
							distancia_minima = dist_nodo
							destino = node
				except:
					continue

		if demanda_actual > 0.:
			#RUTA MÍNIMA
			try:
				path = list(nx.dijkstra_path(G, origen, destino, weight = costo))
				
				Nparadas = len(path)
				for parada in range(Nparadas-1):
					O = path[parada]
					D = path[parada + 1]
					G.edges[O, D, 0]["flujo"] += incremento*OD_reducida[key]

			except:
				continue


costo_total = 0
flujo_total = 0
costo_max = 0
flujo_max = 0

for i, edge in enumerate(G.edges):
    arco = G.edges[edge]

    f = arco["flujo"]

    if "lanes" in arco:
        if str(type(arco["lanes"])) == "<class 'list'>":
            arco["lanes"] = [int(i) for i in arco["lanes"]]
            p = np.average(arco["lanes"])
        else:
            p = int(arco["lanes"]) 
    else:
        p = 1
    if p<=0:
        p=1
	
    q = f/5400
	
    if "length" in arco:
        length = float(arco["length"])
    else:
        length = 100

    if "highway" in arco:
        street_type = arco["highway"]
    else:
        street_type = "NO ROUTE"

    if street_type == "motorway":
        vel = 25
        u = 5
    elif street_type == "primary" or street_type == "secondary":
        vel = 15
        u = 3
    else:
        vel = 8
        u = 2

    costo = length/vel + (5-u)*12 + (900/(u*p))*(10*q - u*p +np.sqrt((10*q-u*p)**2 + q/9))
    
    G.edges[edge]["costo"] = costo
    
    costo_total += costo
    flujo_total += f
    
    if costo_max<costo:
        costo_max = costo
    if flujo_max<f:
        flujo_max = f


print(f"Costo Total = {costo_total}")
print(f"Flujo Total Asignado = {flujo_total}")


nx.write_gpickle(G, "Wardrop_sin_AVO.gpickle")


colors_flujo = []
colors_costo = []

for i, edge in enumerate(G.edges):
	if G.edges[edge]["flujo"] < flujo_max/5:
		colors_flujo.append("blue")
	elif G.edges[edge]["flujo"] < 2*flujo_max/5:
		colors_flujo.append("green")
	elif G.edges[edge]["flujo"] < 3*flujo_max/5:
		colors_flujo.append("yellow")
	elif G.edges[edge]["flujo"] < 4*flujo_max/5:
		colors_flujo.append("orange")
	else:
		colors_flujo.append("red")

	if G.edges[edge]["costo"] < costo_max/5:
		colors_costo.append("blue")
	elif G.edges[edge]["costo"] < 2*costo_max/5:
		colors_costo.append("green")
	elif G.edges[edge]["costo"] < 3*costo_max/5:
		colors_costo.append("yellow")
	elif G.edges[edge]["costo"] < 4*costo_max/5:
		colors_costo.append("orange")
	else:
		colors_costo.append("red")
        
        
        

# Graficamos el grafo completo de Santiago sin AVO
fig, ax = plt.subplots()
zonas_gdf.plot(ax=ax, color = "#CDCDCD")
nx.draw(G, pos = pos, node_size = 5)
plt.suptitle("Santiago sin AVO")
plt.savefig("Santiago sin AVO", bbox_inches = 'tight')


# Graficamos el grafo con los flujos
fig, ax = plt.subplots()
zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Flujo sin AVO")
nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=5, arrowsize=6, edge_color=colors_flujo)
intervalo1 = mpatches.Patch(color = "blue", label=f"[{0}, {round(flujo_max/5, 2)}]")
intervalo2 = mpatches.Patch(color = "green", label=f"[{round(flujo_max/5, 2)}, {round(2*flujo_max/5, 2)}]")
intervalo3 = mpatches.Patch(color = "yellow", label=f"[{round(2*flujo_max/5, 2)}, {round(3*flujo_max/5, 2)}]")
intervalo4 = mpatches.Patch(color = "orange", label=f"[{round(3*flujo_max/5, 2)}, {round(4*flujo_max/5, 2)}]")
intervalo5 = mpatches.Patch(color = "red", label=f"[{round(4*flujo_max/5, 2)}, {round(flujo_max, 2)}]")
plt.legend(handles = [intervalo1, intervalo2, intervalo3, intervalo4, intervalo5], loc='upper right')
plt.savefig("Flujo sin AVO", dpi = 300, bbox_inches = 'tight')


# Graficamos el grafo con los costos
fig, ax = plt.subplots()
zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Costo sin AVO")
nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=5, arrowsize=6, edge_color=colors_costo)
intervalo1 = mpatches.Patch(color = "blue", label=f"[{0}, {round(costo_max/5, 2)}]")
intervalo2 = mpatches.Patch(color = "green", label=f"[{round(costo_max/5, 2)}, {round(2*costo_max/5, 2)}]")
intervalo3 = mpatches.Patch(color = "yellow", label=f"[{round(2*costo_max/5, 2)}, {round(3*costo_max/5, 2)}]")
intervalo4 = mpatches.Patch(color = "orange", label=f"[{round(3*costo_max/5, 2)}, {round(4*costo_max/5, 2)}]")
intervalo5 = mpatches.Patch(color = "red", label=f"[{round(4*costo_max/5, 2)}, {round(costo_max, 2)}]")
plt.legend(handles = [intervalo1, intervalo2, intervalo3, intervalo4, intervalo5], loc='upper right')
plt.savefig("Costo sin AVO", dpi = 300, bbox_inches = 'tight')

plt.show()

