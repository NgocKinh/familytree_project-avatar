# relationship_resolver.py
from backend.domain.engine_v2.relationship_engine_clean import resolve_inlaw_clean
from backend.domain.engine_v2.relationship_normalizer import normalize_path
from backend.domain.engine_v2.data_layer_db import (
    get_children,
    get_siblings,
    get_spouse,
    get_birth,
    get_gender,
    get_parents
)
from backend.domain.engine_v2.graph_engine import find_relationship_path
from backend.domain.engine_v2.family_side_analyzer import detect_side

from backend.domain.engine_v2.metadata_layer import (
    extract_uncle_aunt_metadata,
    extract_sibling_metadata,
    extract_nephew_niece_metadata,
    extract_metadata
)
from backend.domain.engine_v2.render_layer import (
    build_standard_output,
)
from .relations.constants import (
    REGION,
    SPOUSE_MAP,
)
from .relations.helpers import build_call
from backend.domain.engine_v2.inlaw_resolver import (
    is_child_in_law,
    is_parent_in_law,
    is_sibling_in_law,
    is_sibling_of_spouse,
)

# ==========================================================
# ✅ [STEP 5.3] Convert NEW path → OLD format
# ==========================================================
def convert_path_format(new_path):

    if not new_path:
        return []

    converted = []

    # bỏ ('self', start)
    for rel, node, meta in new_path:
        if rel == "self":
            continue
        converted.append((rel, node, meta))
    return converted

# ======================================================
# 🔥 STEP 12: LẤY THÔNG TIN PERSON
# ⚠️ LEGACY BLOCK
# ======================================================

def resolver_relationship(a: int, b: int):

    # 1. tìm path
    # =========================
    # 🔁 NEW ENGINE (SAFE MODE)
    # =========================

    new_path = find_relationship_path(a, b)

    path = convert_path_format(new_path)
    # =====================================
    # 🔥 EXTRACT METADATA / PERSON OBJECTS
    # =====================================

    source_person = {
        "id": a,
        "gender": get_gender(a),
        "birth_year": get_birth(a)
    }

    target_person = {
        "id": b,
        "gender": get_gender(b),
        "birth_year": get_birth(b)
    }
    metadata = extract_metadata(
        path,
        source_person,
        target_person
    )

    # =====================================
    # 🔵 EXTRACT RELATION STEPS
    # =====================================

    steps = []

    for rel, node, meta in path:
        steps.append(rel)

    # =====================================
    # 🔵 NORMALIZE PATH
    # =====================================

    normalized = normalize_path(steps)

    # =====================================
    # 🔵 SAFE RELATION
    # =====================================

    if (
        isinstance(normalized, list)
        and len(normalized) > 0
    ):
        if len(normalized) == 1:
            relation = normalized[0]
        else:
            relation = "unknown"

    standard_output = build_standard_output(
        a,
        b,
        relation,
        path,
        metadata
    )

    return {
        "a": a,
        "b": b,
        "path": path,
        "relationship": relation,
        # 🔥 NEW: cultural metadata
        "metadata": metadata,
        "result": standard_output,

        # 🔥 STEP 12: thêm metadata
        "target_person": {
            "id": b,
            "gender": get_gender(b),
            "birth_year": get_birth(b)
        },
        # 🔥 STEP 13: thêm người A
        "source_person": {
            "id": a,
            "gender": get_gender(a),
            "birth_year": get_birth(a)
        }    
    }
