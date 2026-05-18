# =========================================================
# IN-LAW RULE ENGINE (VIETNAMESE – CLEAN VERSION)
# A → B = A gọi B là gì
# =========================================================

INLAW_RULES = {

    # =========================
    # SIBLING ↔ SPOUSE
    # =========================

    # A là sibling của R, B là spouse của R
    ("sibling_older", "spouse_female"): {
        "male": "chị dâu",
        "female": "chị dâu"
    },

    ("sibling_younger", "spouse_female"): {
        "male": "em dâu",
        "female": "em dâu"
    },

    ("sibling_older", "spouse_male"): {
        "male": "anh rể",
        "female": "anh rể"
    },

    ("sibling_younger", "spouse_male"): {
        "male": "em rể",
        "female": "em rể"
    },

    # =========================
    # SPOUSE ↔ SIBLING
    # =========================

    # A là spouse của R, B là sibling của R

    ("spouse_male", "sibling_younger"): "em vợ",
    ("spouse_male", "sibling_older_male"): "anh vợ",
    ("spouse_male", "sibling_older_female"): "chị vợ",

    ("spouse_female", "sibling_younger"): "em chồng",
    ("spouse_female", "sibling_older_male"): "anh chồng",
    ("spouse_female", "sibling_older_female"): "chị chồng",

    # =========================
    # PARENT IN-LAW
    # =========================

    ("spouse_male", "parent_male"): "cha vợ",
    ("spouse_male", "parent_female"): "mẹ vợ",

    ("spouse_female", "parent_male"): "cha chồng",
    ("spouse_female", "parent_female"): "mẹ chồng",

    # =========================
    # CHILD IN-LAW
    # =========================

    ("parent", "spouse_male"): "con rể",
    ("parent", "spouse_female"): "con dâu",
}