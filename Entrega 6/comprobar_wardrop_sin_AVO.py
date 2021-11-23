import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
from tabulate import tabulate

def costo_arriba(n1, n2, att_arco):
    
    usar_arco_numero = 0
    arco = att_arco[usar_arco_numero]

    f = 1.15*arco["flujo"]

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


def costo_abajo(n1, n2, att_arco):
    usar_arco_numero = 0
    arco = att_arco[usar_arco_numero]

    f = 0.75*arco["flujo"]

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

    return 0.95*costo


def costo_normal(n1, n2, att_arco):
    
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



G = nx.read_gpickle("Wardrop_sin_AVO.gpickle")


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

zonas_avo = []
for key in OD_reducida:
	zonas_avo.append(key[0])
	zonas_avo.append(key[1])

zonas_avo = sorted(set(zonas_avo))

zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_avo)]


par_OD = []
rutas_minimas = []
costos = []
errores = []

for key in OD_reducida:
    origen = key[0]
    destino = key[1]

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


    try:
        rutas_arriba = list(nx.all_shortest_paths(G, origen, destino, weight=costo_arriba))
        rutas_abajo = list(nx.all_shortest_paths(G, origen, destino, weight=costo_abajo))
        rutas = list(nx.all_shortest_paths(G, origen, destino, weight=costo_normal))
        ruta_minima = list(nx.dijkstra_path(G, origen, destino, weight="costo"))

        rutas_totales = rutas_arriba + rutas_abajo + rutas
        new_k = []
        for i in rutas_totales:
            if i not in new_k:
                new_k.append(i)
        rutas_totales = new_k

        par_OD.append(f"{key[0]} - {key[1]}")

        costo_minimo = 0
        Nparada_min = len(ruta_minima)
        for parada in range(Nparada_min-1):
            O = ruta_minima[parada]
            D = ruta_minima[parada + 1]
            costo_minimo += G.edges[O, D, 0]["costo"]
    
        costos_seleccionados = []
        rutas_seleccionadas = 0
        errores_seleccionados = []
        
        for i in rutas_totales:
            costo = 0
            Nparadas = len(i)

            for parada in range(Nparadas-1):
                O = i[parada]
                D = i[parada + 1]
                costo += G.edges[O, D, 0]["costo"]

            if (0.95*costo_minimo) <= costo and costo <= (1.05*costo_minimo):
                costos_seleccionados.append(costo)
                rutas_seleccionadas += 1
                
                if costo_minimo != costo:
                    error = (abs(costo-costo_minimo)/costo_minimo)*100
                    errores_seleccionados.append(error)
                    
                else:
                    errores_seleccionados.append(0)
                    
        rutas_minimas.append(rutas_seleccionadas)
        costos.append(np.average(costos_seleccionados))
        
        if len(errores_seleccionados)<=1:
            errores.append(f"{errores_seleccionados[0]}%")
            
        else:
            errores.append(f"{sum(errores_seleccionados)/(len(errores_seleccionados)-1)}%")
            
    except:
        continue


table = {
    "Par OD (Zonas)": par_OD,
    "Número de Rutas Mínimas": rutas_minimas,
    "Costos": costos,
    "Error de Costos": errores}

print(tabulate(table, headers='keys', tablefmt='fancy_grid'))