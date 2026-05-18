# =========================================================
# ENGINE V2 ORCHESTRATOR
# =========================================================

from backend.domain.engine_v2.graph_engine import (
    find_relationship_path
)
from backend.domain.engine_v2.relationship_normalizer import (
    normalize_path
)
from backend.domain.engine_v2.semantic.affinity_hierarchy_resolver import (
    resolve_affinity_peer_metadata
)
from backend.domain.engine_v2.semantic.relationship_renderer import (
    render_relationship
)
from backend.domain.engine_v2.metadata_layer import extract_sibling_metadata
# =========================================================
# MAIN ENGINE
# =========================================================

def resolve_relationship(a, b):

    # =====================================
    # 1. FIND PATH
    # =====================================

    raw_path = find_relationship_path(a, b)

    if not raw_path:
        return None

    # =====================================
    # 2. CONVERT PATH
    # =====================================

    path = raw_path

    # =====================================
    # 3. EXTRACT STEPS
    # =====================================

    steps = []

    for rel, node, meta in path:

        if rel == "self":
            continue

        steps.append(rel)

    # =====================================
    # 4. NORMALIZE
    # =====================================

    normalized = normalize_path(steps)

    # =====================================
    # 5. SEMANTIC ENRICHMENT
    # =====================================

    metadata = {}

    if normalized in (
        ["affinity_peer"],
        ["sibling_in_law"]
    ):

        metadata.update(
            resolve_affinity_peer_metadata(a, b, path)
        )

    # =====================================
    # 6. RENDER
    # =====================================

    rendered = render_relationship(
        a,
        b,
        normalized,
        metadata
    )

    return {
        "path": path,
        "steps": steps,
        "normalized": normalized,
        "metadata": metadata,
        "relation": rendered
    }