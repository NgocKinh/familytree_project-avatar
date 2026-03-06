def are_related(conn, id1: int, id2: int) -> bool:

    if id1 == id2:
        return True

    query = """
    WITH RECURSIVE lineage AS (

        SELECT parent_id AS ancestor, child_id, 1 AS depth
        FROM parent_child
        WHERE child_id IN (%s, %s)

        UNION ALL

        SELECT pc.parent_id, l.child_id, l.depth + 1
        FROM parent_child pc
        JOIN lineage l
            ON pc.child_id = l.ancestor
        WHERE l.depth < 5
    )

    SELECT 1
    FROM lineage l1
    JOIN lineage l2
    ON l1.ancestor = l2.ancestor
    WHERE l1.child_id = %s
    AND l2.child_id = %s
    LIMIT 1;
    """

    cur = conn.cursor(dictionary=True)
    cur.execute(query, (id1, id2, id1, id2))
    result = cur.fetchone()

    return result is not None
