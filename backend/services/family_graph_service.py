from backend.db import get_connection
from backend.domain.family_graph import FamilyGraph

def build_family_graph():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
  
    cursor.execute("SELECT spouse_a_id, spouse_b_id FROM marriage")
    marriages = cursor.fetchall()

    cursor.execute("SELECT parent_id, child_id FROM parent_child")
    parent_child_rows = cursor.fetchall()

    builder = FamilyGraph()

    graph = builder.build(marriages, parent_child_rows)

    cursor.close()
    conn.close()

    return graph

