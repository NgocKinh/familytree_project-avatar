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

    import heapq

    # (cost, node, path, used_spouse)
    queue = []
    heapq.heappush(queue, (0, start_id, [], False))

    visited = set([start_id])

    while queue:
        cost, current, path, used_spouse = heapq.heappop(queue)

        if current == target_id:
            return path

        if len(path) >= max_depth:
            continue

        for relation_type, neighbor_id in graph.get(current, []):

            next_used_spouse = used_spouse

            if neighbor_id in visited:
                continue

            step = (current, relation_type, neighbor_id)
            new_path = path + [step]

            visited.add(neighbor_id)

            # 🔥 COST: ưu tiên SPOUSE
            extra_cost = 0 if relation_type == "spouse" else 1
            new_cost = cost + 1 + extra_cost

            heapq.heappush(queue, (
                new_cost,
                neighbor_id,
                new_path,
                next_used_spouse
            ))

    return None