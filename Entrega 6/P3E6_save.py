import networkx as nx
import osmnx as ox


ox.config(use_cache=True, log_console=True)

north = -33.14
south = -33.76
east = -70.20
west = -71.24

G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary"]')

nx.write_gpickle(G, "Santiago_sin_AVO.gpickle")