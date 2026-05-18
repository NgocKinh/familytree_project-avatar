# =========================================================
# File: engine_v2/metadata_layer.py
# =========================================================
# PURPOSE:
# Extract cultural metadata from canonical path
#
# Metadata:
# - paternal / maternal
# - older / younger
# - gender
#
# Engine v2 architecture:
# graph_engine
#     ↓
# canonical relationship
#     ↓
# metadata_layer
#     ↓
# relationship_resolver
# =========================================================
# =========================================================
# COMPARE AGE
# =========================================================
from backend.domain.engine_v2.data_layer_db import (
    get_birth,
    get_birth_order,
    get_gender
)

def is_older(person_a_birth, person_b_birth):

    """
    True  -> A older than B
    False -> A younger than B
    """

    if person_a_birth is None or person_b_birth is None:
        return False

    return person_a_birth < person_b_birth

# =========================================================
# DETECT SIDE
# =========================================================

def detect_side(path):

    """
    Detect paternal / maternal side
    based on parent role in path

    Example:
    ("parent", x, "father") -> paternal
    ("parent", x, "mother") -> maternal
    """

    for rel, node, meta in path:

        if rel == "parent":

            if meta == "father":
                return "paternal"

            if meta == "mother":
                return "maternal"

    return None


# =========================================================
# DETECT OLDER
# =========================================================

def detect_older(source_person, target_person):

    """
    Compare birth year
    True  -> source older
    False -> source younger
    """

    birth_a = source_person.get("birth_year")
    birth_b = target_person.get("birth_year")

    if birth_a is None or birth_b is None:
        return None

    return birth_a < birth_b


# =========================================================
# DETECT GENDER
# =========================================================

def detect_gender(source_person):

    """
    Return source gender
    """

    return source_person.get("gender")


# =========================================================
# EXTRACT METADATA
# =========================================================

def extract_metadata(path, source_person, target_person):

    """
    Build metadata object for runtime resolver
    """

    metadata = {

        "side": detect_side(path),

        "older": detect_older(
            source_person,
            target_person
        ),

        "gender": detect_gender(source_person)

    }
    # =====================================
    # FIX GRANDPARENT
    # =====================================

    steps = [rel for rel, _, _ in path]
    if steps == ["parent", "parent"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_grandparent_metadata(
            a,
            b,
            path
        )

    # =====================================
    # FIX GRANDCHILD
    # =====================================

    if steps == ["child", "child"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_grandchild_metadata(
            a,
            b,
            path
        )    
    # =====================================
    # FIX UNCLE / AUNT
    # =====================================

    if steps == ["parent", "parent", "child"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_uncle_aunt_metadata(a, b)

    # =====================================
    # FIX NEPHEW / NIECE
    # =====================================

    if steps == ["parent", "child", "child"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_nephew_niece_metadata(a, b)

    # =====================================
    # FIX SIBLING
    # =====================================

    if steps == ["parent", "child"]:

        a = source_person.get("id")
        b = target_person.get("id")

        return extract_sibling_metadata(a, b)

    # =====================================
    # FIX PARENT
    # =====================================

    if steps == ["parent"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_parent_metadata(a, b)

    # =====================================
    # FIX CHILD
    # =====================================

    if steps == ["child"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_child_metadata(a, b)

    # =====================================
    # FIX SPOUSE
    # =====================================

    if steps == ["spouse"]:

        a = source_person.get("id")
        b = target_person.get("id")

        metadata = extract_spouse_metadata(a, b)

    return metadata
# =========================================================
# EXTRACT PARENT METADATA
# =========================================================

def extract_parent_metadata(a, b):

    return {
        "gender": get_gender(b)
    }


# =========================================================
# EXTRACT CHILD METADATA
# =========================================================

def extract_child_metadata(a, b):

    return {
        "gender": get_gender(b)
    }


# =========================================================
# EXTRACT SPOUSE METADATA
# =========================================================

def extract_spouse_metadata(a, b):

    return {
        "gender": get_gender(b)
    }

# =====================================
# EXTRACT GRANDPARENT METADATA
# =====================================

def extract_grandparent_metadata(a, b, path):

    first_role = path[0][2]

    if first_role == "father":
        side = "paternal"

    elif first_role == "mother":
        side = "maternal"

    else:
        side = None

    return {

        "side": side,

        "gender": get_gender(b),

        "older": False

    }

# =====================================
# EXTRACT GRANDCHILD METADATA
# =====================================

def extract_grandchild_metadata(a, b, path):

    first_step = path[0][1]

    parents_b = get_parents(b)

    father_b = next(
        (p for p, r in parents_b if r == "father"),
        None
    )

    mother_b = next(
        (p for p, r in parents_b if r == "mother"),
        None
    )

    if first_step == father_b:
        side = "paternal"

    elif first_step == mother_b:
        side = "maternal"

    else:
        side = None

    return {

        "side": side,

        "gender": get_gender(b),

        "older": True

    }    
# =========================================================
# EXTRACT UNCLE / AUNT METADATA
# =========================================================

from backend.domain.engine_v2.data_layer_db import (
    get_parents,
    get_gender,
    get_birth,
    get_birth_order,
    get_siblings
)

def extract_uncle_aunt_metadata(a, b):

    """
    Extract metadata for uncle/aunt relationship
    """

    parents_a = get_parents(a)

    if not parents_a:
        return None
    
    father_a = next(
        (p for p, r in parents_a if r == "father"),
        None
    )
    mother_a = next(
        (p for p, r in parents_a if r == "mother"),
        None
    )

    # =====================================
    # sibling helper
    # =====================================

    def is_sibling(x, y):

        if not x or not y:
            return False

        px = {pp for pp, _ in get_parents(x)}
        py = {pp for pp, _ in get_parents(y)}

        return len(px & py) > 0

    # =====================================
    # paternal side
    # =====================================

    if father_a and is_sibling(b, father_a):

        side = "paternal"

        gender = get_gender(b)

        birth_b = get_birth(b)
        birth_father = get_birth(father_a)

        older = is_older(
            birth_b,
            birth_father
        )

        return {
            "side": side,
            "gender": gender,
            "older": older
        }

    # =====================================
    # maternal side
    # =====================================

    if mother_a and is_sibling(b, mother_a):

        side = "maternal"

        gender = get_gender(b)

        birth_b = get_birth(b)
        birth_mother = get_birth(mother_a)

        older = is_older(
            birth_b,
            birth_mother
        )

        return {
            "side": side,
            "gender": gender,
            "older": older
        }

    return None
# =========================================================
# EXTRACT SIBLING METADATA
# =========================================================

def extract_sibling_metadata(a, b):

    birth_a = get_birth(a)
    birth_b = get_birth(b)

    older = is_older(
        birth_a,
        birth_b
    )

    return {
        "older": older,
        "gender": get_gender(a)
    }

# =========================================================
# EXTRACT NEPHEW / NIECE METADATA
# =========================================================

def extract_nephew_niece_metadata(a, b):

    gender = get_gender(b)

    parents_b = get_parents(b)

    if not parents_b:
        return None

    found_parent = None
    side = None
    parents_a = get_parents(a)

    father_a = next(
        (p for p, r in parents_a if r == "father"),
        None
    )

    mother_a = next(
        (p for p, r in parents_a if r == "mother"),
        None
    )
    for parent_id, role in parents_b:

        siblings = get_siblings(parent_id)
     
        if a in siblings:

            found_parent = parent_id

            if role == "father":
                side = "paternal"

            elif role == "mother":
                side = "maternal"

            break

    if not found_parent:
        return None

    birth_parent = get_birth(found_parent)
    birth_a = get_birth(a)

    older = birth_a < birth_parent
32  ef compare(db, person_a_id: int, person_b_id: int):
33      """
34      So sánh kết quả V1 vs V2 cho 1 cặp người
35      """
36      # BẬT V2 (rất quan trọng: bật trên MODULE, không phải biến local)
37      v2.COUSIN_V2_ENABLED = True
38  
39      r1 = v1.get_relationship(db, person_a_id, person_b_id)
40      r2 = v2.get_relationship_v2(db, person_a_id, person_b_id)
41  
42      print("=" * 60)
43      print(f"A = {person_a_id}, B = {person_b_id}")
44      print("V1:", r1)
45      print("V2:", r2)
46      print("=" * 60)
47      print()
    return {
        "side": side,
        "older": older,
        "gender": gender
    }    