# ==========================================================
# File: graph_engine.py
# STEP 5.2 — Clean Graph Engine
# ==========================================================

from collections import deque
from backend.domain.engine_v2.data_layer_db import (
    load_parent_child_graph,
    load_marriage_graph,
)

def find_relationship_path(start, target):

    if start == target:
        return [("self", start, None)]

    visited = set()
    queue = deque()

    queue.append((start, [("self", start, None)]))
    visited.add(start)

    parents_map, children_map = load_parent_child_graph()
    spouses_map = load_marriage_graph()

    while queue:
        current, path = queue.popleft()

        # =========================
        # 🔹 PARENT
        # =========================

        for parent, role in parents_map.get(current, []):
            if parent not in visited:
                if parent == target:
                    return path + [("parent", parent, role)]

                visited.add(parent)
                queue.append((parent, path + [("parent", parent, role)]))

        # =========================
        # 🔹 CHILD
        # =========================

        for child in children_map.get(current, []):
            if child not in visited:
                if child == target:
                    return path + [("child", child, None)]

                visited.add(child)
                queue.append((child, path + [("child", child, None)]))

        # =========================
        # 🔹 SPOUSE
        # =========================

        for spouse in spouses_map.get(current, []):
            if spouse and spouse not in visited:
                if spouse == target:
                    return path + [("spouse", spouse, None)]

                visited.add(spouse)
                queue.append((spouse, path + [("spouse", spouse, None)]))

    return None