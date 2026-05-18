# =========================================================
# AFFINITY HIERARCHY RESOLVER
# =========================================================

from backend.domain.engine_v2.data_layer_db import (
    get_birth,
    get_gender,
    get_birth_order
)


# =========================================================
# EXTRACT AFFINITY ANCHORS
# spouse -> parent -> child -> spouse
# =========================================================

def extract_affinity_peer_anchors(path):

    filtered = []

    for rel, node, meta in path:

        if rel == "self":
            continue

        filtered.append((rel, node, meta))

    if len(filtered) != 4:
        return None

    r1, n1, _ = filtered[0]
    r2, n2, _ = filtered[1]
    r3, n3, _ = filtered[2]
    r4, n4, _ = filtered[3]

    if [r1, r2, r3, r4] != [
        "spouse",
        "parent",
        "child",
        "spouse"
    ]:
        return None

    return {
        "anchor_source": n1,
        "anchor_target": n3
    }
# =========================================================
# EXTRACT SIBLING IN LAW ANCHORS
# =========================================================

def extract_sibling_inlaw_anchors(a, path):

    filtered = []

    for rel, node, meta in path:

        if rel == "self":
            continue

        filtered.append((rel, node, meta))

    if len(filtered) != 3:
        return None

    r1, n1, _ = filtered[0]
    r2, n2, _ = filtered[1]
    r3, n3, _ = filtered[2]

    if [r1, r2, r3] != [
        "parent",
        "child",
        "spouse"
    ]:
        return None

    return {
        "ego": a,
        "sibling": n2,
        "inlaw": n3
    }
def extract_spouse_sibling_anchors(a, path):

    filtered = []

    for rel, node, meta in path:

        if rel == "self":
            continue

        filtered.append((rel, node, meta))

    if len(filtered) != 3:
        return None

    r1, n1, _ = filtered[0]
    r2, n2, _ = filtered[1]
    r3, n3, _ = filtered[2]

    if [r1, r2, r3] != [
        "spouse",
        "parent",
        "child"
    ]:
        return None

    return {
        "ego": a,
        "spouse": n1,
        "sibling": n3,
        "kind": "spouse_sibling"
    }
# =========================================================
# COMPARE HIERARCHY
# =========================================================

def compare_hierarchy(a, b):

    ya = get_birth(a)
    yb = get_birth(b)

    if ya is None or yb is None:
        return None

    if ya < yb:
        return "older"

    if ya > yb:
        return "younger"

    return "same"


# =========================================================
# MAIN RESOLVER
# =========================================================
def detect_affinity_side_context(a, b, path):
    clean_path = path

    if clean_path and clean_path[0][0] == "self":
        clean_path = clean_path[1:]

    steps = [rel for rel, _, _ in clean_path]

    if steps == ["spouse", "parent", "child", "spouse"]:
        first_spouse = clean_path[0][1]
        spouse_gender = get_gender(first_spouse)

        if spouse_gender == "male":
            return "husband_side"

        if spouse_gender == "female":
            return "wife_side"

    return None

def resolve_affinity_peer_metadata(a, b, path):

    anchors = extract_affinity_peer_anchors(path)

    if anchors:

        hierarchy = compare_hierarchy(
            anchors["anchor_target"],
            anchors["anchor_source"]
        )

        return {
            "hierarchy": hierarchy,
            "anchor_source": anchors["anchor_source"],
            "anchor_target": anchors["anchor_target"],
            "kind": "affinity_peer",
            "side_context": detect_affinity_side_context(a, b, path)
        }

    anchors = extract_sibling_inlaw_anchors(a, path)

    if anchors:

        hierarchy = compare_hierarchy(
            anchors["sibling"],
            anchors["ego"]
        )

        return {
            "hierarchy": hierarchy,
            "ego": anchors["ego"],
            "sibling": anchors["sibling"],
            "inlaw": anchors["inlaw"],
            "kind": "sibling_spouse"
        }

    anchors = extract_spouse_sibling_anchors(a, path)

    if anchors:

        hierarchy = compare_hierarchy(
            anchors["sibling"],
            anchors["spouse"]
        )

        return {
            "hierarchy": hierarchy,
            "ego": anchors["ego"],
            "spouse": anchors["spouse"],
            "sibling": anchors["sibling"],
            "kind": "spouse_sibling"
        }

    return {}