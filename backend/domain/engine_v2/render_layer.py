# =====================================
# FILE: render_layer.py
# =====================================

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

    return {
        "relation": render_grandparent(metadata),
        "relation_basic": "grandparent",
        "relation_side": side,
        "gender": gender,
        "call": None
    }

# =====================================
# 🔥 GRANDCHILD OUTPUT
# =====================================

def build_grandchild_output(metadata):

    side = metadata.get("side")
    gender = metadata.get("gender")

    return {
        "relation": render_grandchild(metadata),
        "relation_basic": "grandchild",
        "relation_side": side,
        "gender": gender,
        "call": None
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