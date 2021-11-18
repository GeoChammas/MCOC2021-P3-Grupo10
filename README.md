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
