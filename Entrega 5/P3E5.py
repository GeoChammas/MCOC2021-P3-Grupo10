import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
import numpy as np
import csv



def costo(n1, n2, att_arco):
    
    usar_arco_numero = 0
    arco = att_arco[usar_arco_numero]
    
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
        
    f = 0
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

G = nx.read_gpickle("Santiago_Grueso.gpickle")

zonas_gdf = gps.read_file("eod.json")


rows = []
with open("mod.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
        
OD = {}
for row in rows:
    OD[(int(row[0]), int(row[1]))] = float(row[2])


gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


zonas_avo = []

for key in OD:
    zona_origen = key[0]
    zona_destino = key[1]

    
    #Representative Point Origen
    p = zonas_gdf[zonas_gdf.ID==zona_origen].representative_point()
    try:
        cx_zona_origen, cy_zona_origen = float(p.x), float(p.y)
    except:
        try:
            cx_zona_origen, cy_zona_origen = float(zonas_gdf[zonas_gdf.ID==zona_origen].centroid.x), float(zonas_gdf[zonas_gdf.ID==zona_origen].centroid.y)
        except:
            print("No hay punto")

    distancia_minima = np.infty

    for i, node in enumerate(G.nodes):
        cx_nodo = G.nodes[node]["x"]
        cy_nodo = G.nodes[node]["y"]
        
        dist_nodo = np.sqrt((cx_nodo-cx_zona_origen)**2 + (cy_nodo-cy_zona_origen)**2)
        
        if dist_nodo < distancia_minima:
            distancia_minima = dist_nodo
            nodo_origen = node


    #Representative Point Origen
    p = zonas_gdf[zonas_gdf.ID==zona_destino].representative_point()
    try:
        cx_zona_destino, cy_zona_destino = float(p.x), float(p.y)
    except:
        try:
            cx_zona_destino, cy_zona_destino = float(zonas_gdf[zonas_gdf.ID==zona_destino].centroid.x), float(zonas_gdf[zonas_gdf.ID==zona_destino].centroid.y)
        except:
            print("No hay punto")
    
    distancia_minima = np.infty

    for i, node in enumerate(G.nodes):
        cx_nodo = G.nodes[node]["x"]
        cy_nodo = G.nodes[node]["y"]
        
        dist_nodo = np.sqrt((cx_nodo-cx_zona_destino)**2 + (cy_nodo-cy_zona_destino)**2)
        
        if dist_nodo < distancia_minima:
            distancia_minima = dist_nodo
            nodo_destino = node
    
    try:    
        path = list(nx.all_shortest_paths(G, nodo_origen, nodo_destino, weight = costo))
        for i in path:
            Nparadas = len(i)
            for parada in range(Nparadas-1):
                n1 = i[parada]
                n2 = i[parada+1]
                tomar_arco = 0
                arco = G.edges[n1, n2, tomar_arco]
                
                if "name" in arco:    
                    name = str(arco["name"])
                else:
                    name = ""
                
                if name.find("Autopista Vespucio Oriente") >=0:
                    zonas_avo.append(zona_origen)
                    zonas_avo.append(zona_destino)
                    
    except:
        print(f"No hay rutas entre {nodo_origen} y {nodo_destino}")


zonas_avo = sorted(set(zonas_avo))
print(zonas_avo)
# zonas_seleccionadas = zonas_gdf[zonas_gdf["ID"].isin(zonas_avo)]
zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_avo)]


OD_reducida={}

for key in OD:
	if key[0] in zonas_avo or key[1] in zonas_avo:
		OD_reducida[(int(key[0]), int(key[1]))] = float(OD[key])
        

with open("OD_reducida.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    for key in OD_reducida:
        writer.writerow([key[0], key[1], OD_reducida[key]])
        

# plt.figure()
# ax = plt.subplot(111)
# zonas_seleccionadas.plot(ax=ax, color = "#CDCDCD")
# gdf_edges[gdf_edges.highway=="motorway"].plot(ax=ax, color="orange", linewidth = 0.5)
# gdf_edges[gdf_edges.highway=="primary"].plot(ax=ax, color="yellow", linewidth = 0.5)
# gdf_edges[gdf_edges.highway=="secondary"].plot(ax=ax, color="green", linewidth = 0.5)
# gdf_edges[gdf_edges.highway=="tertiary"].plot(ax=ax, color="blue", linewidth = 0.5)
# gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth = 3)    
# plt.show()

