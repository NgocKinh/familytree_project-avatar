from collections import deque
from backend.constants.marriage_constants import ACTIVE_MARRIAGE_STATUSES
from backend.db import get_connection
from sqlalchemy import text

def score_path(path):
    relations = [rel for _, rel, _ in path]

    score = 0

    for r in relations:
        if r == "SPOUSE":
            score += 10
        elif r == "PARENT":
            score += 5
        elif r == "CHILD":
            score += 3

    # ❌ phạt đường vòng
    if relations == ["PARENT", "CHILD", "PARENT"]:
        score -= 10

    return score

def find_shortest_path_db(from_id, to_id, db):
    """
    PATH DISCOVERY – HÀM CHUẨN DUY NHẤT

    Mục đích:
    - Tìm đường đi ngắn nhất từ from_id → to_id
    - Chỉ làm PATH (Discovery)
    - Không suy luận quan hệ
    - Không nội / ngoại
    - Không đếm đời

    Dữ liệu sử dụng:
    - family_relationships (parent / child)
    - marriages (spouse)

    Return:
    - [from_id, ..., to_id] nếu tìm được
    - None nếu không có đường đi
    """
    # ---------------------------------------
    # 0. Trường hợp đặc biệt
    # ---------------------------------------
    if from_id == to_id:
        return [from_id]
    # ---------------------------------------
    # 1. BUILD GRAPH FROM REAL DB
    # ---------------------------------------

    graph: dict[int, dict[int, str]] = {}

    # =========================
    # PARENT / CHILD
    # =========================
    rows = db.execute(text("""
        SELECT parent_id, child_id
        FROM parent_child
    """)).mappings().all()

    for row in rows:

        parent_id = row["parent_id"]
        child_id = row["child_id"]

        graph.setdefault(parent_id, {})
        graph.setdefault(child_id, {})

        graph[parent_id][child_id] = "CHILD"
        graph[child_id][parent_id] = "PARENT"

    # =========================
    # SPOUSE
    # =========================
    spouse_rows = db.execute(text("""
        SELECT spouse_a_id, spouse_b_id
        FROM marriages
        WHERE status != 'deleted'
    """)).mappings().all()

    for row in spouse_rows:

        a = row["spouse_a_id"]
        b = row["spouse_b_id"]

        if a is None or b is None:
            continue

        graph.setdefault(a, {})
        graph.setdefault(b, {})

        graph[a][b] = "SPOUSE"
        graph[b][a] = "SPOUSE"

    # ===== SPOUSE DIRECT OVERRIDE =====
    if (
        from_id in graph
        and to_id in graph[from_id]
        and graph[from_id][to_id] == "SPOUSE"
    ):
        return [(from_id, "SPOUSE", to_id)]

    # ---------------------------------------
    # 2. BFS TÌM ĐƯỜNG NGẮN NHẤT (EDGE TYPE)
    # ---------------------------------------
    import heapq

    queue = []
    heapq.heappush(queue, (0, from_id, [], False))

    visited = {}
    paths = []
    
    while queue:
        cost, current, path, used_spouse = heapq.heappop(queue)

        if current == to_id:
            paths.append(path)
            continue

        for neighbor, relation in graph.get(current, {}).items():

            # ✅ cho phép đi nhiều SPOUSE liên tiếp
            next_used_spouse = used_spouse

            step = (current, relation, neighbor)
            new_path = path + [step]

            extra_cost = 0 if relation == "SPOUSE" else 1
            new_cost = cost + 1 + extra_cost

            # 🔥 tránh path tệ hơn
            if neighbor in visited and visited[neighbor] <= new_cost:
                continue

            visited[neighbor] = new_cost

            heapq.heappush(queue, (
                new_cost,
                neighbor,
                new_path,
                next_used_spouse
            ))

    if not paths:
        return None

    best_path = max(paths, key=score_path)
    return best_path

# # ================================================================
# # 🔹 Lấy cha mẹ và con cái trực tiếp
# # ================================================================
# def get_parents_and_children(person_id):
    
#     try:
#         cursor.execute("""
#             SELECT person_id, related_person_id, relationship_type
#             FROM family_relationships
#             WHERE person_id = %s
#         """, (person_id,))
#         parents = set()
#         children = set()

#         for row in cursor.fetchall():
#             if row["relationship_type"] == "child":
#                 parents.add(row["related_person_id"])
#             elif row["relationship_type"] == "parent":
#                 children.add(row["related_person_id"])    
#     finally:
#         cursor.close()
#         conn.close()
#     return list(parents), list(children)

    # rows = db.execute(text("""
    # SELECT person_id, related_person_id, relationship_type
    # FROM family_relationships
    # """)).mappings().all()

    # # 👉 build graph (tách riêng)
    # for row in rows:
    #     a = row["person_id"]
    #     b = row["related_person_id"]
    #     rel = row["relationship_type"]

    #     if a is None or b is None:
    #         continue

    #     if rel == "parent":
    #         graph.setdefault(a, {})[b] = "PARENT"
    #         graph.setdefault(b, {})[a] = "CHILD"

    #     elif rel == "child":
    #         graph.setdefault(a, {})[b] = "CHILD"
    #         graph.setdefault(b, {})[a] = "PARENT"

    #     elif rel == "spouse":
    #         graph.setdefault(a, {})[b] = "SPOUSE"
    #         graph.setdefault(b, {})[a] = "SPOUSE"

    # # ---- Spouse ↔ Spouse
    # placeholders = ", ".join([f":s{i}" for i in range(len(ACTIVE_MARRIAGE_STATUSES))])

    # params = {f"s{i}": v for i, v in enumerate(ACTIVE_MARRIAGE_STATUSES)}

    spouse_rows = db.execute(text(f"""
        SELECT spouse_a_id, spouse_b_id
        FROM marriages
        WHERE status != 'deleted'
        OR status IN ({placeholders})
    """), params).mappings().all()

    # for row in spouse_rows:

    #     a = row["spouse_a_id"]
    #     b = row["spouse_b_id"]

    #     if a is None or b is None:
    #         continue

    #     graph.setdefault(a, {})[b] = "SPOUSE"
    #     graph.setdefault(b, {})[a] = "SPOUSE"

    # # ===== SPOUSE DIRECT OVERRIDE =====
    # if (
    #     from_id in graph
    #     and to_id in graph[from_id]
    #     and graph[from_id][to_id] == "SPOUSE"
    # ):
    #     return [(from_id, "SPOUSE", to_id)]   