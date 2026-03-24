from collections import deque

def bfs_blood_path(graph, source_id, target_id):
    """
    BFS chỉ duyệt quan hệ huyết thống:
    parent / child

    graph format:
    graph[node] = [(relation, neighbor), ...]
    """

    if source_id == target_id:
        return []

    queue = deque()
    visited = set()

    # queue item: (current_node, path)
    queue.append((source_id, []))
    visited.add(source_id)

    while queue:

        current_node, path = queue.popleft()

        if current_node not in graph:
            continue

        for relation, neighbor in graph[current_node]:

            # RULE 1: bỏ spouse
            if relation == "spouse":
                continue

            # RULE 2: chỉ cho parent / child
            if relation not in ("parent", "child", "father", "mother", "son", "daughter"):
                continue

            # RULE 3: tránh loop
            if neighbor in visited:
                continue

            new_path = path + [(current_node, relation, neighbor)]

            # FOUND
            if neighbor == target_id:
                return new_path

            visited.add(neighbor)
            queue.append((neighbor, new_path))

    return None


def bfs_kinship_path(graph, start_id, target_id, max_depth=10):
    """
    BFS kinship:
    - Cho phép đi qua spouse đúng 1 lần
    - Không thay thế bfs_blood_path (giữ backward compatibility)
    """

    # (node, path, used_spouse)
    queue = deque([(start_id, [], False)])

    # Quan trọng: visited phải gồm state
    visited = set([(start_id, False)])

    while queue:
        current, path, used_spouse = queue.popleft()

        if current == target_id:
            return path

        if len(path) >= max_depth:
            continue

        for relation_type, neighbor_id in graph.get(current, []):

            # --- RULE 3: spouse only once ---
            if relation_type == "spouse":
                if used_spouse:
                    continue
                next_used_spouse = True
            else:
                next_used_spouse = used_spouse

            state = (neighbor_id, next_used_spouse)

            if state in visited:
                continue

            visited.add(state)

            queue.append((
                neighbor_id,
                path + [(current, relation_type, neighbor_id)],
                next_used_spouse
            ))

    return None