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
from backend.domain.engine_v2.cultural_resolver import (
    resolve_uncle_aunt_call
)
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
# REGION = "north"

# SPOUSE_MAP = {
#     "bác": "bác gái",
#     "chú": "thím",
#     "cậu": "mợ",
#     "cô": "dượng",
#     "dì": "dượng",
#     "bác gái": "bác trai"
# }
# ======================================================
# 🔥 STEP 12: LẤY THÔNG TIN PERSON
# ======================================================
# ⚠️ LEGACY BLOCK
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

# ==========================================================
# 🔥 STEP 6 — UNCLE/AUNT ORCHESTRATOR
# ==========================================================
       
def resolve_uncle_aunt_v2(a, b):
    from data_layer import get_parent, get_children, get_birth

    gender_a = get_gender(a)

    # =========================
    # 🔹 CHA/MẸ của B
    # =========================
    parents_b = []

    # lấy tất cả cha/mẹ của B
    for parent_id, role in get_parents(b):
        parents_b.append(parent_id)

    if not parents_b:
        return None

    # =========================
    # 🔥 LOOP QUA CẢ CHA VÀ MẸ
    # =========================
    for parent_b in parents_b:

        grandparent = get_parent(parent_b)
        if not grandparent:
            continue

        siblings_parent = get_children(grandparent)
        siblings_parent = [x for x in siblings_parent if x != parent_b]

        if a not in siblings_parent:
            continue

        gender_parent = get_gender(parent_b)

        if gender_parent == "male":
            side = "paternal"
        else:
            side = "maternal"

        birth_a = get_birth(a)
        birth_parent = get_birth(parent_b)

        older = False
        if birth_a and birth_parent:
            older = birth_a < birth_parent

        # =========================
        # 🔥 CULTURAL RESOLUTION
        # =========================
        return resolve_uncle_aunt_call(
            gender_a,
            side,
            older
        )[1] 

# =====================================
# 🔥 LEVEL 3 — CON DÂU / CON RỂ
# =====================================
def is_child_in_law(a, b):
    """
    A có phải con dâu / con rể của B không
    """

    # 👉 tìm tất cả con của B
    children = get_children(b)

    # 👉 kiểm tra A có phải vợ/chồng của con không
    for child in children:
        spouse = get_spouse(child)

        if spouse == a:
            gender_a = get_gender(a)

            if gender_a == "female":
                return "con dâu"
            elif gender_a == "male":
                return "con rể"

    return None
# =====================================
# 🔥 LEVEL 3 — CHA VỢ / MẸ CHỒNG
# =====================================
def is_parent_in_law(a, b):
    spouse = get_spouse(b)
    if not spouse:
        return None

    # tìm cha/mẹ của spouse
    parents = get_parents(spouse)

    for parent_id, role in parents:
        if parent_id == a:

            if gender_a == "male":
                return "cha vợ" if gender_spouse == "female" else "cha chồng"
            elif gender_a == "female":
                return "mẹ vợ" if gender_spouse == "female" else "mẹ chồng"

    return None
# =====================================
# 🔥 LEVEL 3 — ANH RỂ / CHỊ DÂU
# =====================================
def is_sibling_in_law(a, b):
    """
    A có phải vợ/chồng của anh/chị/em của B không
    """

    siblings = get_siblings(b)

    for sib in siblings:
        spouse = get_spouse(sib)

        if spouse == a:
            gender_a = get_gender(a)
            birth_sib = get_birth(sib)
            birth_b = get_birth(b)

            if not birth_sib or not birth_b:
                return "anh rể" if gender_a == "male" else "chị dâu"

            older = birth_sib < birth_b  # 👉 SIBLING so với B

            if gender_a == "male":
                return "anh rể" if older else "em rể"
            else:
                return "chị dâu" if older else "em dâu"

    return None
# =====================================
# 🔥 LEVEL 3 — ANH CHỒNG / EM CHỒNG / CHỊ VỢ / EM VỢ
# =====================================
def is_sibling_of_spouse(a, b):
    """
    A là anh/chị/em của vợ/chồng của B
    → trả về: anh chồng / em chồng / chị chồng / em vợ
    """

    spouse = get_spouse(b)
    if not spouse:
        return None

    siblings = get_siblings(spouse)

    if a not in siblings:
        return None

    gender_a = get_gender(a)

    birth_b = get_birth(b)
    birth_spouse = get_birth(spouse)

    older = False
    if birth_b and birth_spouse:
        older = birth_b < birth_spouse

    # 🔥 PHÂN BIỆT CHỒNG / VỢ
    spouse_gender = get_gender(spouse)

    # 👉 spouse là NAM → A là anh/em CHỒNG
    if spouse_gender == "male":
        if gender_a == "male":
            return "anh chồng" if older else "em chồng"
        else:
            return "chị chồng" if older else "em chồng"

    # 👉 spouse là NỮ → A là anh/em VỢ
    else:
        if gender_a == "male":
            return "anh vợ" if older else "em vợ"
        else:
            return "chị dâu" if older else "em dâu"

def get_uncle_aunt_call(side, gender, birth_a, birth_parent, region):
    # fallback
    if not birth_a or not birth_parent:
        if side == "paternal":
            return "chú" if gender == "male" else "cô"
        else:
            return "cậu" if gender == "male" else "dì"

    older = birth_a < birth_parent

    # =========================
    # 🔴 BÊN NỘI (CHA)
    # =========================
    if side == "paternal":
        if gender == "male":
            return "bác" if older else "chú"
        else:
            return "cô"

    # =========================
    # 🔵 BÊN NGOẠI (MẸ)
    # =========================
    if side == "maternal":

        # ===== MIỀN BẮC =====
        if region == "north":
            if gender == "male":
                return "bác" if older else "cậu"
            else:
                return "cô"   # theo bảng bạn đưa

        # ===== MIỀN NAM =====
        else:
            if gender == "male":
                return "cậu"
            else:
                return "dì"

    return "không rõ"

# def build_standard_output(a, b, relation, path, metadata):

#     gender_a = get_gender(a)

#     relation_text = None

#     # =====================================
#     # 🔥 LEVEL 2 — BASIC FAMILY LABEL
#     # =====================================

#     if relation == "child":

#         gender = metadata["gender"]

#         return {
#             "relation": "con trai" if gender == "male" else "con gái",
#             "relation_basic": "child",
#             "relation_side": None,
#             "gender": gender,
#             "call": None
#         }

#     if relation == "parent":

#         gender = metadata["gender"]

#         return {
#             "relation": "cha" if gender == "male" else "mẹ",
#             "relation_basic": "parent",
#             "relation_side": None,
#             "gender": gender,
#             "call": None
#         }

#     if relation == "spouse":

#         gender = metadata["gender"]

#         return {
#             "relation": "chồng" if gender == "male" else "vợ",
#             "relation_basic": "spouse",
#             "relation_side": None,
#             "gender": gender,
#             "call": None
#         }

#     # =====================================
#     # 🔥 GRANDPARENT
#     # =====================================

#     if relation == "grandparent":
#         return build_grandparent_output(metadata)

#     # =====================================
#     # 🔥 GRANDCHILD
#     # =====================================

#     if relation == "grandchild":
#         return build_grandchild_output(metadata)

#     # =====================================
#     # 🔥 LEVEL 2.5 — ANH / CHỊ / EM
#     # =====================================
#     if relation == "sibling":

#         metadata = extract_sibling_metadata(a, b)

#         return build_sibling_output(metadata)

#     # =====================================
#     # 🔥 SIBLING IN-LAW
#     # =====================================

#     if relation == "sibling_in_law":

#         gender_a = get_gender(a)

#         spouse = get_spouse(a)
#         if not spouse:
#             return {
#                 "relation": "chưa xác định mối quan hệ",
#                 "gender": gender_a,
#                 "call": None
#             }

#         siblings = get_siblings(spouse)

#         if b not in siblings:
#             return {
#                 "relation": "chưa xác định mối quan hệ",
#                 "gender": gender_a,
#                 "call": None
#             }

#         gender_b = get_gender(b)
#         spouse_gender = get_gender(spouse)

#         birth_a = get_birth(a)
#         birth_b = get_birth(b)

#         older = False
#         if birth_a and birth_b:
#             older = birth_b < birth_a

#         # =========================
#         # 🔥 CORE LOGIC FIX
#         # =========================

#         if spouse_gender == "female":
#             # bên vợ
#             if gender_b == "male":
#                 rel = "anh vợ" if older else "em vợ"
#             else:
#                 rel = "chị vợ" if older else "em vợ"

#         else:
#             # bên chồng
#             if gender_b == "male":
#                 rel = "anh rể" if older else "em rể"
#             else:
#                 rel = "chị dâu" if older else "em dâu"

#         return {
#             "relation": rel,
#             "relation_basic": "sibling_in_law",
#             "relation_side": None,
#             "gender": gender_b,
#             "call": {
#                 "north": rel,
#                 "south": rel
#             }
#         }

#     # =====================================
#     # 🔥 CHILD IN-LAW
#     # =====================================

#     if relation == "child_in_law":

#         gender_b = get_gender(b)

#         rel = "con dâu" if gender_b == "female" else "con rể"

#         return {
#             "relation": rel,
#             "relation_basic": "in-law",
#             "relation_side": None,
#             "gender": gender_b,
#             "call": {
#                 "north": rel,
#                 "south": rel
#             }
#         } 

#     # =====================================
#     # 🔥 PARENT IN-LAW
#     # =====================================

#     if relation == "parent_in_law":

#         gender_a = get_gender(a)
#         gender_b = get_gender(b)

#         # =====================================
#         # 🔥 SOURCE LÀ NAM
#         # =====================================

#         if gender_a == "male":

#             rel = "ba vợ" if gender_b == "male" else "mẹ vợ"

#         # =====================================
#         # 🔥 SOURCE LÀ NỮ
#         # =====================================

#         else:

#             rel = "ba chồng" if gender_b == "male" else "mẹ chồng"

#         return {
#             "relation": rel,
#             "relation_basic": "in-law",
#             "relation_side": None,
#             "gender": gender_b,
#             "call": {
#                 "north": rel,
#                 "south": rel
#             }
#         }    
#     # =====================================
#     # 🔥 STEP 6.2 — NEPHEW / NIECE (FINAL CLEAN)
#     # =====================================
#     # ⚠️ NOT USED BY CURRENT CANONICAL FLOW
#     if relation == "nephew/niece":

#         gender_a = get_gender(a)

#         # =========================
#         # 🔹 tìm CHA/MẸ của A
#         # =========================
#         parents_a = get_parents(a)

#         if not parents_a:
#             return {
#                 "relation": "unknown",
#                 "gender": gender_a,
#                 "call": None
#             }

#         found_parent = None
#         side = None

#         # =========================
#         # 🔥 tìm parent đúng (có quan hệ với B)
#         # =========================
#         for parent_id, role in parents_a:
#             siblings = get_siblings(parent_id)

#             if b in siblings:
#                 found_parent = parent_id

#                 if role == "father":
#                     side = "paternal"
#                 elif role == "mother":
#                     side = "maternal"

#                 break

#         if not found_parent:
#             return {
#                 "relation": "unknown",
#                 "gender": gender_a,
#                 "call": None
#             }

#         # =========================
#         # 🔥 xác định cách gọi
#         # =========================
#         gender_b = get_gender(b)

#         birth_b = get_birth(b)
#         birth_parent = get_birth(found_parent)

#         older = False
#         if birth_b and birth_parent:
#             older = birth_b < birth_parent

#         call_north, call_south = resolve_uncle_aunt_call(
#             gender_b,
#             side,
#             older
#         )

#         # =========================
#         # 🔥 text hiển thị
#         # =========================
#         if gender_a == "male":
#             relation_text = f"cháu trai gọi {call_north} (Bắc) / {call_south} (Nam)"
#         else:
#             relation_text = f"cháu gái gọi {call_north} (Bắc) / {call_south} (Nam)"

#         return {
#             "relation": relation_text,
#             "relation_basic": "cháu",
#             "relation_side": side,
#             "gender": gender_a,
#             "call": {
#                 "north": call_north,
#                 "south": call_south
#             }
#         }
#     # =====================================
#     # 🔥 UNCLE / AUNT (CANONICAL)
#     # =====================================
#     if relation == "uncle_aunt":

#         if not metadata:
#             return {
#                 "relation": "unknown",
#                 "gender": None,
#                 "call": None
#             }

#         call_north, call_south = resolve_uncle_aunt_call(
#             metadata["gender"],
#             metadata["side"],
#             metadata["older"]
#         )

#         return build_uncle_aunt_output(
#             metadata,
#             call_north,
#             call_south
#         )
#     # =====================================
#     # 🔥 NEPHEW / NIECE
#     # =====================================

#     if relation == "nephew_niece":

#         if not metadata:
#             return {
#                 "relation": "unknown",
#                 "gender": None,
#                 "call": None
#             }

#         return build_nephew_niece_output(metadata)
#     # =====================================
#     # SPOUSE OF UNCLE / AUNT
#     # =====================================

#     if relation == "spouse_of_uncle_aunt":

#         side = metadata.get("side")
#         gender = metadata.get("gender")
#         older = metadata.get("older")

#         if side == "paternal":

#             if gender == "male":
#                 if older:
#                     relation_name = "bác trai"
#                 else:
#                     relation_name = "dượng"
#             else:
#                 if older:
#                     relation_name = "bác gái"
#                 else:
#                     relation_name = "thím"

#         elif side == "maternal":

#             if gender == "male":
#                 relation_name = "dượng"
#             else:
#                 relation_name = "mợ"

#         else:
#             relation_name = "chưa xác định mối quan hệ"

#         return {
#             "relation": relation_name,
#             "relation_basic": relation,
#             "relation_side": side,
#             "gender": gender,
#             "call": {
#                 "north": relation_name,
#                 "south": relation_name
#             }
#         }    
#     # =====================================
#     # DEFAULT
#     # =====================================
#     return {
#         "relation": "chưa xác định mối quan hệ",
#         "gender": gender_a,
#         "call": None
#     }
    