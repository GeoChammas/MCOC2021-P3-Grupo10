import networkx as nx
import osmnx as ox


ox.config(use_cache=True, log_console=True)

north = -33.14
south = -33.76
east = -70.20
west = -71.24

G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary|construction"]')

for i, edge in enumerate(G.edges):
	if "highway" in G.edges[edge[0], edge[1], 0] and "name" in G.edges[edge[0], edge[1], 0]:
		if G.edges[edge[0], edge[1], 0]["highway"] == "construction" and G.edges[edge[0], edge[1], 0]["name"] == "Autopista Vespucio Oriente":
			G.edges[edge[0], edge[1], 0]["highway"] = "motorway"

nx.write_gpickle(G, "Santiago_Grueso.gpickle")
