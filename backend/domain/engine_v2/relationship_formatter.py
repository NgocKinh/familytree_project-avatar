# ==========================================================
# File: relationship_formatter.py
# STEP 10 — FORMAT RELATION (LEVEL 2) — RULE TABLE VERSION
# ==========================================================
# normalize
print("🔥 FORMATTER FILE LOADED")
from data_layer import get_parents, get_gender, get_birth
REGION = "south"   # "north" | "south"
def normalize_steps_from_path(path):
    """
    Input:
        path = [('parent', 3, 'father'), ('child', 6, None)]
    Output:
        ['parent', 'child']
    """
    steps = []

    for p in path:
        if not p or not p[0]:
            continue

        relation = str(p[0]).strip().lower()
        steps.append(relation)

    return steps

# rules
# ⚠️ transitional semantic rules
# TODO: migrate to relationship_resolver.py
RULES = {
    
    ("spouse", "parent", "child"): {
        "relation_basic": "em vợ/chồng",
        "relation_detail": ""
    },

    ("sibling", "spouse", "sibling"): {
        "relation_basic": "anh/chị/em bên vợ/chồng",
        "relation_detail": ""
    },
}

# region config
REGION_MAP = {
    "north": {
        "cô": "cô",
        "chú": "chú",
        "cậu": "cậu",
        "dì": "dì",
        "thím": "thím",
        "mợ": "mợ"
    },
    "south": {
        "cô": "dì",
        "chú": "cậu",
        "cậu": "cậu",
        "dì": "dì",
        "thím": "mợ",
        "mợ": "mợ"
    }
}
def apply_region(term, context=None):
    if not term:
        return term

    region = context.get("region", "south") if context else "south"
    mapping = REGION_MAP.get(region, {})

    for k, v in mapping.items():
        term = term.replace(k, v)

    return term

# core rules
# ⚠️ transitional semantic rules
# TODO: migrate to relationship_resolver.py
CORE_RULES = {

    # ===== CHA / MẸ =====
    ("parent",): "cha/mẹ",

    # ===== CON =====
    ("child",): "con",

    # ===== ANH CHỊ EM =====
    ("sibling",): "anh/chị/em",

    # # ===== ÔNG BÀ =====
    # ("parent", "parent"): "ông/bà",

    # # ===== CHÁU =====
    # ("child", "child"): "cháu",

}

# smart engine
def build_blocks(path):
    result = []
    i = 0

    while i < len(path):

        # # ✅ CASE 1: parent → child → child  (cháu)
        # if (
        #     i + 2 < len(path)
        #     and path[i][0] == "parent"
        #     and path[i+1][0] == "child"
        #     and path[i+2][0] == "child"
        # ):
        #     result.append(("grandchild", None))
        #     i += 3
        #     continue

        # # ✅ CASE 2: parent → child  (sibling)
        # if (
        #     i + 1 < len(path)
        #     and path[i][0] == "parent"
        #     and path[i+1][0] == "child"
        # ):
        #     side = path[i][2]
        #     result.append(("sibling", side))
        #     i += 2
        #     continue

        # # ✅ CASE 3: parent -> parent -> child (uncle/aunt)
        # if (
        #     i + 2 < len(path)
        #     and path[i][0] == "parent"
        #     and path[i+1][0] == "parent"
        #     and path[i+2][0] == "child"
        # ):
        #     result.append(("uncle_aunt", None))
        #     i += 3
        #     continue

        # # ✅ CASE 4: parent -> child -> child (nephew/niece)
        # if (
        #     i + 2 < len(path)
        #     and path[i][0] == "parent"
        #     and path[i+1][0] == "child"
        #     and path[i+2][0] == "child"
        # ):
        #     result.append(("nephew_niece", None))
        #     i += 3
        #     continue

        # giữ nguyên bước thường
        result.append((path[i][0], path[i][2]))
        i += 1
    return result
              
def resolve_relation(blocks, context):

    a = context["source_person"]["id"]
    b = context["target_person"]["id"]

    gender_a = context["source_person"]["gender"]
    gender_b = context["target_person"]["gender"]
    print("🔥 BLOCKS =", blocks)
    # ===== CHA / MẸ =====
    if len(blocks) == 1 and blocks[0][0] == "parent":
        return None

    # ===== CON =====
    if len(blocks) == 1 and blocks[0][0] == "child":
        return None

    # ===== GRANDPARENT =====
    if [x[0] for x in blocks] == ["parent", "parent"]:

        metadata = context.get("metadata", {})

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

    # ===== GRANDCHILD =====
    if [x[0] for x in blocks] == ["child", "child"]:

        metadata = context.get("metadata", {})

        side = metadata.get("side")

        if side == "paternal":
            return "cháu nội"

        if side == "maternal":
            return "cháu ngoại"

        return "cháu"

    # # ===== ANH / CHỊ / EM =====
    # if len(blocks) == 1 and blocks[0][0] == "sibling":
    #     birth_a = get_birth(a)
    #     birth_b = get_birth(b)

    #     if birth_a and birth_b:
    #         if birth_b < birth_a:
    #             return None 
    #         else:
    #             return None 

    #     return None

    # ===== COUSIN =====
    if [x[0] for x in context["path"]] == ["parent", "parent", "child", "child"]:

        a = context["source_person"]["id"]
        b = context["target_person"]["id"]
        gender_b = context["target_person"]["gender"]

        parents_a = get_parents(a)
        parents_b = get_parents(b)

        father_a = next((p for p, r in parents_a if r == "father"), None)
        mother_a = next((p for p, r in parents_a if r == "mother"), None)

        parent_b = parents_b[0][0] if parents_b else None
        gender_parent_b = get_gender(parent_b)

        def is_sibling(x, y):
            if not x or not y:
                return False
            px = {pp for pp, _ in get_parents(x)}
            py = {pp for pp, _ in get_parents(y)}
            return len(px & py) > 0

        relation = None
        if father_a and is_sibling(parent_b, father_a):
            birth_pb = get_birth(parent_b)
            birth_fa = get_birth(father_a)
            if birth_pb and birth_fa:
                relation = "elder" if birth_pb < birth_fa else "younger"

        if mother_a and is_sibling(parent_b, mother_a):
            birth_pb = get_birth(parent_b)
            birth_ma = get_birth(mother_a)
            if birth_pb and birth_ma:
                relation = "elder" if birth_pb < birth_ma else "younger"

        # xác định cô/dì/chú/cậu (FIX ĐÚNG)
        uncle_label = None

        if father_a and is_sibling(parent_b, father_a):
            if gender_parent_b == "male":
                uncle_label = "bác" if relation == "elder" else "chú"
            else:
                uncle_label = "cô"

        elif mother_a and is_sibling(parent_b, mother_a):
            if gender_parent_b == "male":
                uncle_label = "cậu"
            else:
                uncle_label = "dì"

        # xác định cousin
        if relation == "elder":
            base = "anh họ" if gender_b == "male" else "chị họ"
        else:
            base = "em họ"

        if uncle_label:
            return f"{base} con của {uncle_label}"

        return base

    # ===== CANONICAL: UNCLE_AUNT =====
    if [x[0] for x in blocks] == ["uncle_aunt"]:

        a = context["source_person"]["id"]   # người đi hỏi (1)
        b = context["target_person"]["id"]   # người được hỏi (4, 21, 22)
        gender_b = context["target_person"]["gender"]
        side = None
        older = None
        parents_a = get_parents(a)
        father_a = next((p for p, r in parents_a if r == "father"), None)
        mother_a = next((p for p, r in parents_a if r == "mother"), None)

        def is_sibling(x, y):
            if not x or not y:
                return None
            px = {pp for pp, _ in get_parents(x)}
            py = {pp for pp, _ in get_parents(y)}
            return None

        # # 👉 bên nội (anh/em của cha)
        # if father_a and is_sibling(b, father_a):

        #     side = "paternal"

        #     if gender_b == "male":

        #         birth_b = get_birth(b)
        #         birth_father = get_birth(father_a)

        #         if birth_b and birth_father:
        #             older = birth_b < birth_father
        #             return None

        #         return None

        #     else:
        #         return None

        # # 👉 bên ngoại (anh/em của mẹ)
        # if mother_a and is_sibling(b, mother_a):

        #     side = "maternal"

        #     return None
        
    # ===== CHỊ DÂU / ANH RỂ =====
    if [x[0] for x in blocks] == ["sibling", "spouse"]:
        # 🔥 lấy sibling từ path (chuẩn)
        sibling = None
        for rel, node, meta in context["path"]:
            if rel == "child":
                sibling = node
                break

        birth_a = get_birth(a)
        birth_sibling = get_birth(sibling) if sibling else None

        is_elder = False
        if birth_a and birth_sibling:
            is_elder = birth_sibling < birth_a

        if gender_b == "female":
            return "chị dâu" if is_elder else "em dâu"

        if gender_b == "male":
            return "anh rể" if is_elder else "em rể"

        return "dâu/rể"

    # ===== EM VỢ / EM CHỒNG =====
    if [x[0] for x in blocks] == ["spouse", "parent", "child"]:
        if gender_a == "female":
            return "em chồng"
        else:
            return "em vợ"
    # ===== IN-LAW SÂU (AUTO BUILD) =====
    # pattern: parent → child → spouse → parent → child

    pattern = [x[0] for x in context["path"]]

    if pattern == ["parent","child","spouse","parent","child"]:
   
        a = context["source_person"]["id"]
        b = context["target_person"]["id"]

        gender_b = context["target_person"]["gender"]

        # 🔥 tìm sibling (node trung gian)
        sibling = None
        for rel, node, meta in context["path"]:
            if rel == "child":
                sibling = node
                break

        # 🔥 tìm spouse của sibling (QUAN TRỌNG)
        spouse = None
        found_sibling = False

        for rel, node, meta in context["path"]:
            if rel == "child":
                found_sibling = True
                continue

            if found_sibling and rel == "spouse":
                spouse = node
                break

        # giữ lại mid để dùng cho so tuổi
        mid = sibling

        # 🔥 lấy gender spouse từ data_layer
        gender_spouse = get_gender(spouse)

        # 🔥 xác định quan hệ trung gian
        if gender_spouse == "female":
            middle = "chị dâu"
        else:
            middle = "anh rể"

        # 🔥 xác định lớn / nhỏ
        birth_mid = get_birth(mid)
        birth_b = get_birth(b)

        is_elder = False
        if birth_mid and birth_b:
            is_elder = birth_b < birth_mid

        # 🔥 xác định quan hệ cuối
        if gender_b == "male":
            final = "anh" if is_elder else "em trai"
        else:
            final = "chị" if is_elder else "em gái"

        # 🔥 ghép câu tự nhiên
        return f"{final} của {middle}"
    return None

# normalize rules
def normalize_steps(steps):

    if steps == ["parent", "parent", "child"]:
        return ["uncle_aunt"]

    return steps 
                  
def format_relation(path, context=None):
    """
    path = [(id, relation, meta), ...]
    """
    if context is None:
        context = {}

    # ======================================================
    # 🟡 [SAFE]: PATH NULL
    # ======================================================
    if not path:
        return {
            "relation_basic": "không rõ",
            "relation_detail": "",
            "relation_path": ""
        }

    # 🔥 STEP 1: clean path trước (QUAN TRỌNG)
    path = [
        (p[0].strip(), p[1], (p[2].strip() if p[2] else None))
        for p in path
    ]

    steps = normalize_steps_from_path(path)

    # 🔥 normalize loop (QUAN TRỌNG)
    while True:
        new_steps = normalize_steps(steps)
        if new_steps == steps:
            break
        steps = new_steps

    if not steps:
        return {
            "relation_basic": "không rõ",
            "relation_detail": "",
            "relation_path": ""
        }

    # core rules
    key = tuple(steps)

    if key in CORE_RULES:
        return {
            "relation_basic": apply_region(CORE_RULES[key], context),
            "relation_detail": apply_region(""),
            "relation_path": " → ".join(steps)
        }

    context["path"] = path
    blocks = build_blocks(path)
    result = resolve_relation(blocks, context)

    if result:
        return {
            "relation_basic": apply_region(result, context),
            "relation_detail": apply_region(result, context),
            "relation_path": " → ".join(steps)
        }
        
    if key in RULES:
        rule = RULES[key]
        return {
            "relation_basic": apply_region(rule["relation_basic"], context),
            "relation_detail": apply_region(rule["relation_detail"]),
            "relation_path": " → ".join(steps)
        }
    # fallback
    return {
        "relation_basic": apply_region("không rõ", context),
        "relation_detail": "",
        "relation_path": " → ".join(steps)
    }
