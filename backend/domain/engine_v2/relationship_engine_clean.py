from backend.domain.engine_v2.data_layer_db import (
    get_spouse,
    get_siblings,
    get_parents,
    get_birth,
    get_gender
)
from backend.domain.engine_v2.inlaw_rules import INLAW_RULES


def is_sibling(a, b):
    return b in get_siblings(a)

def resolve_inlaw_clean(a, b):
    """
    A → B = A gọi B là gì
    """

    # =========================
    # 1. A là sibling của R
    # =========================
    for r in get_siblings(a):

        spouse_r = get_spouse(r)

        if spouse_r == b:

            gender_b = get_gender(b)

            # =====================================
            # 🔥 SO THỨ BẬC THEO SIBLING ANCHOR
            # a <-> r
            # KHÔNG phải a <-> b
            # =====================================

            birth_a = get_birth(a)
            birth_r = get_birth(r)

            older = False

            if birth_a and birth_r:
                older = birth_r < birth_a

            # =====================================
            # 🔥 XÁC ĐỊNH KEY
            # =====================================

            if older:
                key = ("sibling_older", f"spouse_{gender_b}")
            else:
                key = ("sibling_younger", f"spouse_{gender_b}")

            rule = INLAW_RULES.get(key)

            if isinstance(rule, dict):
                return rule.get(get_gender(a))

            return rule

    # =========================
    # 2. A là spouse của R
    # =========================
    spouse_a = get_spouse(a)

    if spouse_a:
        siblings_r = get_siblings(spouse_a)

        if b in siblings_r:
            gender_a = get_gender(a)

            # xác định vai của B
            birth_anchor = get_birth(spouse_a)
            birth_sibling = get_birth(b)

            if birth_anchor and birth_sibling:

                if birth_sibling < birth_anchor:
                    role = (
                        "sibling_older_male"
                        if get_gender(b) == "male"
                        else "sibling_older_female"
                    )

                else:
                    role = "sibling_younger"

            else:
                role = "sibling_younger"

            key = (f"spouse_{gender_a}", role)
            return INLAW_RULES.get(key)

    # =========================
    # 3. PARENT IN-LAW
    # =========================
    spouse_a = get_spouse(a)

    if spouse_a:
        parents_r = get_parents(spouse_a)

        if b in parents_r:
            key = (f"spouse_{get_gender(a)}", f"parent_{get_gender(b)}")
            return INLAW_RULES.get(key)

    # =========================
    # 4. CHILD IN-LAW
    # =========================
    for child, role in get_parents(b):
        spouse_child = get_spouse(child)

        if spouse_child == a:
            key = ("parent", f"spouse_{get_gender(a)}")
            return INLAW_RULES.get(key)

    return None