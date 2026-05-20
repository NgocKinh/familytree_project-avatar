# =========================================================
# IN-LAW RESOLVER
# =========================================================

from backend.domain.engine_v2.data_layer_db import (
    get_siblings,
    get_spouse,
    get_birth,
    get_gender,
    get_parents,
    get_children,
)

# =====================================
# 🔥 LEVEL 3 — CON DÂU / CON RỂ
# =====================================

def is_child_in_law(a, b):
    """
    A có phải con dâu / con rể của B không
    """

    children = get_children(b)

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

    gender_a = get_gender(a)
    gender_spouse = get_gender(spouse)

    parents = get_parents(spouse)

    for parent_id, role in parents:

        if parent_id == a:

            if gender_a == "male":

                return (
                    "cha vợ"
                    if gender_spouse == "female"
                    else "cha chồng"
                )

            elif gender_a == "female":

                return (
                    "mẹ vợ"
                    if gender_spouse == "female"
                    else "mẹ chồng"
                )

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

                return (
                    "anh rể"
                    if gender_a == "male"
                    else "chị dâu"
                )

            older = birth_sib < birth_b

            if gender_a == "male":
                return "anh rể" if older else "em rể"

            return "chị dâu" if older else "em dâu"

    return None

# =====================================
# 🔥 LEVEL 3 — ANH CHỒNG / EM CHỒNG
# =====================================

def is_sibling_of_spouse(a, b):
    """
    A là anh/chị/em của vợ/chồng của B
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

    spouse_gender = get_gender(spouse)

    # 👉 spouse là NAM
    if spouse_gender == "male":

        if gender_a == "male":
            return "anh chồng" if older else "em chồng"

        return "chị chồng" if older else "em chồng"

    # 👉 spouse là NỮ
    else:

        if gender_a == "male":
            return "anh vợ" if older else "em vợ"

        return "chị dâu" if older else "em dâu"