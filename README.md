# Grupo 10
## Integrantes:
George Chammas

Vicente Otaegui



# Entrega 2


Para esta entrega, se trabajó con la siguiente red

![fig1](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%202/fig1.png)

En donde los diferentes colores de los arcos corresponden a diferentes velocidades máximas a las que se puede viajar. 

El objetivo de esta entrega fue encontrar la ruta mínima (con tiempo de viaje mínimo) para realizar tres viajes independientes: de 0 a 9, de 4 a 5 y de 0 a 4.

A continuación, se presentan las rutas mínimas para cada uno de los tres viajes, junto con el tiempo de viaje de cada uno, en donde se destaca en color rojo los arcos que se usan en cada ruta.


![fig2](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%202/fig2.png)

![fig3](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%202/fig3.png)

![fig4](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%202/fig4.png)


# Entrega 3

## Integrante: George Chammas

![Zona 312 Las Condes George Chammas](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Zona%20312%20Las%20Condes%20George%20Chammas.png)


## Integrante: Vicente Otaegui

![Zona 333 Lo Barnechea Vicente Otaegui](https://github.com/VicenteOtaegui/MCOC2021-P3-Grupo10/blob/main/Zona%20333%20Lo%20Barnechea%20Vicente%20Otaegui.png) 


# Entrega 4

Para esta entrega, el objetivo fue encontrar el equilibrio de Wardrop de la siguiente red.

![Funciones de Costos](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%204/Funciones%20de%20Costos.png)

Se puede notar que cada arco tiene una función, la cual corresponde al costo de cada uno. Este depende del parámetro f correspondiente al flujo en el arco.

Además, a continuación se presenta la matriz origen-destino, correspondiente a la cantidad de viajes (demanda) que se quieren realizar entre cada par OD.

```python
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
```


Para encontrar el equilibrio de Wardrop, se implementó un algoritmo que consiste en empezar con 0 viajes en cada ruta, e ir incrementando la cantidad de viajes con un cierto porcentaje de la demanda de los correspondientes pares OD. Así, se le asignaba un flujo proporcional a cada una de las rutas al mismo tiempo, hasta cumplir con el 100% de la demanda de cada par OD. A continuación, se presenta el código utilizado para implementar este algoritmo.

```python
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
```

Primero, se define la función de costo, la cual obtiene el costo de cada arco en función del flujo en este. Este valor luego es usado para obtener la ruta de costo mínimo usando la función de dijkstra_path, donde se le entrega como peso (weight) el costo. Así, la ruta seleccionada cumplirá con el costo mínimo que puede haber entre el origen y destino que se le entrega a la misma función.

También, se puede notar la lista de incrementos, correspondiente a los porcentajes de la demanda que se usarán para asignar los flujos en la red, tal como se mencionó anteriormente. Como es posible observar, primero se incrementó el flujo en un 5% de la demanda 18 veces, llegando al 90% de esta. Luego, en 1% 9 veces llegando a 99%, posteriormente, 0.1% 9 veces llegando a 99.9% y finalmente 0.01% 10 veces, con lo cual se cumple el 100% de la demanda. Cabe destacar que esto se realizó para cada par OD a la vez, es decir, a modo de ejemplo, en la primera iteración, se asignó el flujo correspondiente al 5% de las demandas de todos los pares OD al mismo tiempo, para así mantenerse en el equilibrio en todo momento. Por otro lado, al ir asignando los flujos a los arcos de la red, también se asignaron los costos de estos, utilizando las funciones de costos de cada uno, los que se presentaron en la red de la imagen superior.


Al finalizar este algoritmo, se graficó la red con los flujos y costos asignados a cada arco, obteniendo lo siguiente.

![Flujos](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%204/Flujos.png)


![Costos](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%204/Costos.png)



Al tener todos los flujos y costos asignados, lo único que falta es verificar que se cumple el equilibrio de Wardrop. Para esto, para cada par origen-destino, se encontró su ruta mínima usando dijkstra_path y se recorrieron todos los arcos de esta ruta, sumando los costos de cada uno para encontrar el costo total de la ruta mínima. Entonces, así, ya se tienen los costos de todas las rutas mínimas de todos los pares OD. El problema es que, para un par OD, podrían haber varias rutas mínimas, todas con el mismo costo (el mínimo posible), pero la función dijkstra_path solo entrega una ruta mínima, y no todas. Para encontrar el resto de la rutas mínimas, se utilizó la función nx.all_simple_paths, la cual entrega una lista con todas las posibles rutas entre un par OD. Luego, se recorrieron los arcos de todas estas rutas, al igual que lo realizado para el dijkstra_path, sumando los costos de todos los arcos para encontrar el costo total de cada ruta. Teniendo estos costos, se compararon con los obtenidos con el dijkstra_path, los cuales corresponden a los mínimos. Se consideraron rutas mínimas todas las que tienen costos con una diferencia menor al 1% con respecto al costo mínimo. Así, se aseguró que se cumple el equilibrio de Wardrop, no perfectamente, pero sí con una error menor al 1%. 

Todo lo que se acaba de explicar, se realizó con el siguiente código.

```python
parOD = []
rutas_minimas = []
costos = []
for key in OD:
    origen = key[0]
    destino = key[1]
    ruta = []
    parOD.append(origen + destino)
    path = nx.dijkstra_path(G, origen, destino, weight="costo2")
    costo_minimo = 0
    Nparadas = len(path)
    for parada in range(Nparadas-1):
        O = path[parada]
        D = path[parada + 1]
        costo_minimo += G.edges[O, D]["costo2"]
    simple_paths = nx.all_simple_paths(G, origen, destino)
    for i in simple_paths:
        for j in i:
            costo_shortest_path = 0
            Nparadas = len(i)
            for parada in range(Nparadas-1):
                O = i[parada]
                D = i[parada + 1]
                costo_shortest_path += G.edges[O, D]["costo2"]
        if costo_shortest_path < 1.01*costo_minimo and costo_shortest_path > 0.99*costo_minimo:
                    ruta.append(i)
    rutas_minimas.append(ruta)
    costos.append(costo_minimo)
```

Para cada par OD, las rutas mínimas encontradas y sus costos se agregaron a las listas parOD, rutas_minimas y costos, las cuales se usan para armar la tabla con los resultados finales que se muestra a continuación, utilizando el siguiente código.

```python
table = {
    "Par OD": parOD,
    "Rutas Mínimas": rutas_minimas,
    "Costos": costos}     
print(tabulate(table, headers='keys', tablefmt='fancy_grid'))
```


![Tabla Final](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%204/Tabla%20Final.png)

# Entrega 5

Esta entrega tiene como objetivo producir un grafo y una matriz OD para todos los pares OD que utilizan la avenida Américo Vespucio Oriente como parte de su ruta. Para esto, se implementaron tres códigos.


## Código 1: P3E5_save

Este archivo busca el mapa de Santiago en internet, según las latitudes y longitudes entregadas, y lo guarda en formato .gpickle. Cabe destacar que se le indica que solo considere los highways que son motorways, primar, secondary, tertiary y construction (el cual contiene a AVO, que después se pasa a motorway).


## Código 2: P3E5

Este archivo abre el mapa guardado como .gpickle, las zonas en eod.json y la matriz OD en mod.csv. Con estos datos, se recorre sobre la matriz OD, encontrando todos los pares OD que usen AVO, guardándolos en un nuevo archivo csv (OD_reducida.csv). Así, se gana eficiencia porque ahora trabajamos con una matriz más pequeña que solo incluye los datos necesarios.


## Código 3: P3E5_ver

Este archivo abre OD_reducida.csv, genera la matriz y la recorre agregando las zonas a una lista para luego ser graficadas en gris. Además, grafica solo los highways que se encuentran en las zonas seleccionadas según los colores indicados en el enunciado y la avenida AVO en rojo.


A continuación, se presenta el grafo obtenido con las zonas de interés en gris y la avenida Américo Vespucio Oriente destacada en rojo.


![AVO](https://github.com/GeoChammas/MCOC2021-P3-Grupo10/blob/main/Entrega%205/AVO.png)


## Preguntas

### ¿Cómo seleccionó las zonas a incluir?

En el segundo archivo de código, se recorrió la matriz OD, se tomaron los nodos más cercanos a los representative points de la zona origen y de la destino y se utilizó la función nx.all_shortest_paths, que entrega todas las rutas más cortas entre dos nodos. Luego, para cada una de esas rutas, se recorrieron sus arcos y se vio si es que alguno correspondía a AVO. Si es que AVO sí se encontraba, entonces se agregaban las zonas origen y destino a una lista, si no, se seguía con el programa. Así, se armó una lista con todas las zonas pertinentes que usan AVO como parte de su ruta. A continuación, se presenta esta parte del código donde se realiza lo explicado.


```python
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
```


### ¿Cuántas zonas quedaron seleccionadas son?

Quedaron seleccionadas 487 zonas en total.


### ¿Cuántos viajes deberá asignar?

Se sumaron todas las demandas de de los pares OD seleccionados (los que se encuentran en la matriz OD reducida), llegando a un total de 436895.6647284921 viajes totales que se deberá asignar.


### ¿Cuales son los pares OD que espera Ud. que generen mayor flujo en AVO?

Creemos que las zonas que más usarán AVO, y por tanto generar el mayor flujo, son las que usan la avenida completa, provocando mayor congestión a lo largo de AVO. Estas corresponden a las que se encuentran al inicio y al final de la avenida. Las que están al inicio: 281, 282, 433, 434, 435. Las que están al final: 144, 145, 153, 578, 579, 580. Los viajes entre estas zonas deberían ser las que generan mayor flujo en AVO.
