# =====================================
# FILE: render_layer.py
# =====================================
from backend.domain.engine_v2.data_layer_db import (
    get_siblings,
    get_spouse,
    get_spouses,
    get_birth,
    get_gender,
    get_parents,
)

from backend.domain.engine_v2.cultural_resolver import (
    resolve_uncle_aunt_call,
)

from backend.domain.engine_v2.metadata_layer import (
    extract_sibling_metadata,
)
def render_grandparent(metadata):

    side = metadata.get("side")
    gender = metadata.get("gender")

    if side == "paternal":

        if gender == "male":
            return "ông nội"

        return "bà nội"

    if side == "maternal":

        if gender == "male":
            return "ông ngoại"

        return "bà ngoại"

    return "ông/bà"

def render_grandchild(metadata):

    side = metadata.get("side")

    if side == "paternal":
        return "cháu nội"

    if side == "maternal":
        return "cháu ngoại"

    return "cháu"

def build_call(call_north=None, call_south=None, fallback=None):
    """
    Chuẩn hóa call cho toàn bộ hệ thống
    """

    if call_north or call_south:
        return {
            "north": call_north,
            "south": call_south
        }

    if fallback:
        return {
            "north": fallback,
            "south": fallback
        }

    return None

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

# =====================================
# 🔥 GRANDPARENT OUTPUT
# =====================================
def build_grandparent_output(metadata):

    side = metadata.get("side")
    gender = metadata.get("gender")

    relation = render_grandparent(metadata)

    return {
        "relation": relation,
        "relation_basic": "grandparent",
        "relation_side": side,
        "gender": gender,
        "call": {
            "north": relation,
            "south": relation
        }
    }
# def build_grandparent_output(metadata):

#     side = metadata.get("side")
#     gender = metadata.get("gender")

#     return {
#         "relation": render_grandparent(metadata),
#         "relation_basic": "grandparent",
#         "relation_side": side,
#         "gender": gender,
#         "call": None
#     }

# =====================================
# 🔥 GRANDCHILD OUTPUT
# =====================================

def build_grandchild_output(metadata):

    side = metadata.get("side")
    gender = metadata.get("gender")

    relation = render_grandchild(metadata)

    return {
        "relation": relation,
        "relation_basic": "grandchild",
        "relation_side": side,
        "gender": gender,
        "call": {
            "north": relation,
            "south": relation
        }
    }

# =====================================
# 🔥 SIBLING OUTPUT
# =====================================

def build_sibling_output(metadata):

    gender = metadata["gender"]
    older = metadata["older"]

    if gender == "male":
        label = "anh trai" if older else "em trai"
    else:
        label = "chị gái" if older else "em gái"

    return {
        "relation": label,
        "relation_basic": "sibling",
        "relation_side": None,
        "gender": gender,
        "call": {
            "north": label,
            "south": label
        }
    }

# =====================================
# 🔥 UNCLE / AUNT OUTPUT
# =====================================

def build_uncle_aunt_output(metadata, call_north, call_south):

    return {
        "relation": call_south,
        "relation_basic": "uncle_aunt",
        "relation_side": metadata["side"],
        "gender": metadata["gender"],
        "call": {
            "north": call_north,
            "south": call_south
        }
    }

# =====================================
# 🔥 NEPHEW / NIECE OUTPUT
# =====================================

def build_nephew_niece_output(metadata):

    gender = metadata["gender"]

    if gender == "male":

        return {
            "relation": "cháu trai",
            "relation_basic": "nephew_niece",
            "relation_side": metadata["side"],
            "gender": gender,
            "call": {
                "north": "cháu trai",
                "south": "cháu trai"
            }
        }

    return {
        "relation": "cháu gái",
        "relation_basic": "nephew_niece",
        "relation_side": metadata["side"],
        "gender": gender,
        "call": {
            "north": "cháu gái",
            "south": "cháu gái"
        }
    }

def build_standard_output(a, b, relation, path, metadata):

    gender_a = get_gender(a)

    relation_text = None

    # =====================================
    # 🔥 LEVEL 2 — BASIC FAMILY LABEL
    # =====================================

    if relation == "parent":

        gender = metadata["gender"]

        relation_name = "cha" if gender == "male" else "mẹ"

        return {
            "relation": relation_name,
            "relation_basic": "parent",
            "relation_side": None,
            "gender": gender,
            "call": {
                "north": relation_name,
                "south": relation_name
            }
        }

    if relation == "child":    

        gender = metadata["gender"]

        relation_name = "con trai" if gender == "male" else "con gái"

        return {
            "relation": relation_name,
            "relation_basic": "child",
            "relation_side": None,
            "gender": gender,
            "call": {
                "north": relation_name,
                "south": relation_name
            }
        }

    if relation == "spouse":

        gender = metadata["gender"]

        relation_name = "chồng" if gender == "male" else "vợ"

        return {
            "relation": relation_name,
            "relation_basic": "spouse",
            "relation_side": None,
            "gender": gender,
            "call": {
                "north": relation_name,
                "south": relation_name
            }
        }

    # =====================================
    # 🔥 GRANDPARENT
    # =====================================

    if relation == "grandparent":
        return build_grandparent_output(metadata)

    # =====================================
    # 🔥 GRANDCHILD
    # =====================================

    if relation == "grandchild":
        return build_grandchild_output(metadata)

    # =====================================
    # 🔥 LEVEL 2.5 — ANH / CHỊ / EM
    # =====================================
    if relation == "sibling":

        metadata = extract_sibling_metadata(a, b)

        return build_sibling_output(metadata)

    # =====================================
    # 🔥 SIBLING IN-LAW
    # =====================================

    if relation == "sibling_in_law":

        gender_a = get_gender(a)
        kind = metadata.get("kind") if metadata else None
        # Case 1: A là vợ/chồng của anh/chị/em ruột B
        if kind == "spouse_sibling":
            for sib in get_siblings(b):
                if a in get_spouses(sib):
                    birth_sib = get_birth(sib)
                    birth_b = get_birth(b)
                    older = False
                    if birth_sib and birth_b:
                        older = birth_sib < birth_b
                    if gender_a == "male":
                        rel = "anh rể" if older else "em rể"
                    else:
                        rel = "chị dâu" if older else "em dâu"

                    return {
                        "relation": rel,
                        "relation_basic": "sibling_in_law",
                        "relation_side": None,
                        "gender": gender_a,
                        "call": {
                            "north": rel,
                            "south": rel
                        }
                    }

        # Case 2: A là anh/chị/em ruột của vợ/chồng B
        if kind == "sibling_spouse":
            spouse_b = get_spouse(b)

            if spouse_b:
                for sib in get_siblings(spouse_b):
                    if a == sib:
                        spouse_gender = get_gender(spouse_b)

                        birth_a = get_birth(a)
                        birth_spouse_b = get_birth(spouse_b)
                        older = False
                        if birth_a and birth_spouse_b:
                            older = birth_a < birth_spouse_b

                        if spouse_gender == "female":
                            if gender_a == "male":
                                rel = "anh vợ" if older else "em vợ"
                            else:
                                rel = "chị vợ" if older else "em vợ"
                        else:
                            if gender_a == "male":
                                rel = "anh chồng" if older else "em chồng"
                            else:
                                rel = "chị chồng" if older else "em chồng"

                        return {
                            "relation": rel,
                            "relation_basic": "sibling_in_law",
                            "relation_side": None,
                            "gender": gender_a,
                            "call": {
                                "north": rel,
                                "south": rel
                            }
                        }

        return {
            "relation": "chưa xác định mối quan hệ",
            "gender": gender_a,
            "call": None
        }

    # =====================================
    # 🔥 CHILD IN-LAW
    # =====================================

    if relation == "child_in_law":

        gender_b = get_gender(b)

        rel = "con dâu" if gender_b == "female" else "con rể"

        return {
            "relation": rel,
            "relation_basic": "in-law",
            "relation_side": None,
            "gender": gender_b,
            "call": {
                "north": rel,
                "south": rel
            }
        } 

    # =====================================
    # 🔥 PARENT IN-LAW
    # =====================================

    if relation == "parent_in_law":

        gender_a = get_gender(a)
        gender_b = get_gender(b)

        # =====================================
        # 🔥 SOURCE LÀ NAM
        # =====================================

        if gender_a == "male":

            rel = "ba vợ" if gender_b == "male" else "mẹ vợ"

        # =====================================
        # 🔥 SOURCE LÀ NỮ
        # =====================================

        else:

            rel = "ba chồng" if gender_b == "male" else "mẹ chồng"

        return {
            "relation": rel,
            "relation_basic": "in-law",
            "relation_side": None,
            "gender": gender_b,
            "call": {
                "north": rel,
                "south": rel
            }
        }    
    # =====================================
    # 🔥 STEP 6.2 — NEPHEW / NIECE (FINAL CLEAN)
    # =====================================
    # ⚠️ NOT USED BY CURRENT CANONICAL FLOW
    if relation == "nephew/niece":

        gender_a = get_gender(a)

        # =========================
        # 🔹 tìm CHA/MẸ của A
        # =========================
        parents_a = get_parents(a)

        if not parents_a:
            return {
                "relation": "unknown",
                "gender": gender_a,
                "call": None
            }

        found_parent = None
        side = None

        # =========================
        # 🔥 tìm parent đúng (có quan hệ với B)
        # =========================
        for parent_id, role in parents_a:
            siblings = get_siblings(parent_id)

            if b in siblings:
                found_parent = parent_id

                if role == "father":
                    side = "paternal"
                elif role == "mother":
                    side = "maternal"

                break

        if not found_parent:
            return {
                "relation": "unknown",
                "gender": gender_a,
                "call": None
            }

        # =========================
        # 🔥 xác định cách gọi
        # =========================
        gender_b = get_gender(b)

        birth_b = get_birth(b)
        birth_parent = get_birth(found_parent)

        older = False
        if birth_b and birth_parent:
            older = birth_b < birth_parent

        call_north, call_south = resolve_uncle_aunt_call(
            gender_b,
            side,
            older
        )

        # =========================
        # 🔥 text hiển thị
        # =========================
        if gender_a == "male":
            relation_text = f"cháu trai gọi {call_north} (Bắc) / {call_south} (Nam)"
        else:
            relation_text = f"cháu gái gọi {call_north} (Bắc) / {call_south} (Nam)"

        return {
            "relation": relation_text,
            "relation_basic": "cháu",
            "relation_side": side,
            "gender": gender_a,
            "call": {
                "north": call_north,
                "south": call_south
            }
        }
    # =====================================
    # 🔥 UNCLE / AUNT (CANONICAL)
    # =====================================
    if relation == "uncle_aunt":

        if not metadata:
            return {
                "relation": "unknown",
                "gender": None,
                "call": None
            }

        call_north, call_south = resolve_uncle_aunt_call(
            metadata["gender"],
            metadata["side"],
            metadata["older"]
        )

        return build_uncle_aunt_output(
            metadata,
            call_north,
            call_south
        )
    # =====================================
    # 🔥 NEPHEW / NIECE
    # =====================================

    if relation == "nephew_niece":

        if not metadata:
            return {
                "relation": "unknown",
                "gender": None,
                "call": None
            }

        return build_nephew_niece_output(metadata)
    # =====================================
    # SPOUSE OF UNCLE / AUNT
    # =====================================

    if relation == "spouse_of_uncle_aunt":

        side = metadata.get("side")
        gender = metadata.get("gender")
        older = metadata.get("older")

        if side == "paternal":

            if gender == "male":
                if older:
                    relation_name = "bác trai"
                else:
                    relation_name = "dượng"
            else:
                if older:
                    relation_name = "bác gái"
                else:
                    relation_name = "thím"

        elif side == "maternal":

            if gender == "male":
                relation_name = "dượng"
            else:
                relation_name = "mợ"

        else:
            relation_name = "chưa xác định mối quan hệ"

        return {
            "relation": relation_name,
            "relation_basic": relation,
            "relation_side": side,
            "gender": gender,
            "call": {
                "north": relation_name,
                "south": relation_name
            }
        }    
    # =====================================
    # DEFAULT
    # =====================================
    return {
        "relation": "chưa xác định mối quan hệ",
        "gender": gender_a,
        "call": None
    }