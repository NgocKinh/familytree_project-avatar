from backend.services.family_graph_service import build_family_graph
from backend.core.path_finder import bfs_blood_path
from backend.core.resolver import resolve_relationship

graph = build_family_graph()

print("Graph[106] =", graph[106])
print("Graph[110] =", graph[110])
print("Graph[123] =", graph[123])
print("Total nodes =", len(graph))

path = bfs_blood_path(graph, 123, 111)
print("PATH EDGES =", path)
relation = resolve_relationship(path)

print("PATH 123 → 111 =", path)
print("RELATION 123 → 111 =", relation)