RELATION_RULES = {

    # ========================
    # DIRECT
    # ========================
    ("PARENT",): "parent",
    ("CHILD",): "child",

    # ========================
    # LINEAL (dòng thẳng)
    # ========================
    ("PARENT", "PARENT"): "grandparent",
    ("CHILD", "CHILD"): "grandchild",

    ("PARENT", "PARENT", "PARENT"): "great-grandparent",
    ("CHILD", "CHILD", "CHILD"): "great-grandchild",

    # ========================
    # SIBLING
    # ========================
    ("PARENT", "CHILD"): "sibling",
    ("CHILD", "PARENT"): "sibling",

    # ========================
    # UNCLE / AUNT
    # ========================
    ("PARENT", "CHILD", "PARENT"): "uncle/aunt",
    ("PARENT", "PARENT", "CHILD"): "uncle/aunt",

    # ========================
    # COUSIN
    # ========================
    ("PARENT", "PARENT", "CHILD", "CHILD"): "cousin",

    # ========================
    # IN-LAW
    # ========================
    ("SPOUSE",): "spouse",


    ("SPOUSE", "CHILD"): "child-in-law",

    ("SPOUSE", "PARENT"): "step-parent",   # tùy logic bạn có thể đổi
    ("CHILD", "SPOUSE"): "step-child",

    # ========================
    # STEP FAMILY (QUAN TRỌNG)
    # ========================
    
    ("SPOUSE", "SPOUSE", "PARENT"): "step-parent",
    ("SPOUSE", "SPOUSE", "CHILD"): "step-child",

    # ========================
    # EXTENDED (có thể thêm sau)
    # ========================
    ("SPOUSE", "PARENT", "CHILD"): "sibling-in-law",
    ("PARENT", "SPOUSE", "PARENT"): "grandparent-in-law",
}