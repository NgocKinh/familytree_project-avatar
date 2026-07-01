# ==========================================================
# File: graph_engine.py
# STEP 5.2 — Clean Graph Engine
# ==========================================================

from collections import deque
from backend.domain.engine_v2.data_layer_db import (
    get_parents,
    get_spouse,
    get_spouses,
    get_children
)

def find_relationship_path(start, target):

    if start == target:
        return [("self", start, None)]

    visited = set()
    queue = deque()

    queue.append((start, [("self", start, None)]))
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        # =========================
        # 🔹 PARENT
        # =========================
        for parent, role in get_parents(current):
            if parent not in visited:
                if parent == target:
                    return path + [("parent", parent, role)]

            visited.add(parent)
            queue.append((parent, path + [("parent", parent, role)]))

        # =========================
        # 🔹 CHILD
        # =========================
        for child in get_children(current):
            if child not in visited:
                if child == target:
                    return path + [("child", child, None)]

                visited.add(child)
                queue.append((child, path + [("child", child, None)]))

        # =========================
        # 🔹 SPOUSE
        # =========================
        spouses = get_spouses(current)

        for spouse in spouses:
            if spouse and spouse not in visited:
                if spouse == target:
                    return path + [("spouse", spouse, None)]

                visited.add(spouse)
                queue.append((spouse, path + [("spouse", spouse, None)]))
    return None