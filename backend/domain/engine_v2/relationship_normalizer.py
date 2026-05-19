# =====================================
# 🔵 RELATIONSHIP NORMALIZER
# =====================================
# ==========================================================
# CANONICAL RELATIONSHIP DETECTOR
# ==========================================================
#
# PURPOSE:
# Convert raw genealogy path into canonical relationship.
#
# Examples:
# parent -> child           => sibling
# parent -> parent          => grandparent
# parent -> parent -> child => uncle_aunt
#
# NOTE:
# This file is part of the MAIN runtime pipeline.
# It is NOT a simple formatter/cleanup layer.
# ==========================================================
def normalize_path(path_steps):
  
    # parent -> child = sibling
    if path_steps == ["parent", "child"]:
        return ["sibling"]

    # parent -> child -> spouse = sibling_in_law
    if path_steps == ["parent", "child", "spouse"]:
        return ["sibling_in_law"]

    # child -> spouse = child_in_law
    if path_steps == ["child", "spouse"]:
        return ["child_in_law"]

    # spouse -> parent = parent_in_law
    if path_steps == ["spouse", "parent"]:
        return ["parent_in_law"]

    # spouse -> parent -> child = sibling_in_law
    if path_steps == ["spouse", "parent", "child"]:
        return ["sibling_in_law"]

    # spouse -> parent -> child -> spouse
    # = affinity_peer
    if path_steps == ["spouse", "parent", "child", "spouse"]:
        return ["affinity_peer"] 

    # parent -> parent -> child -> spouse
    # source is nephew/niece of target
    if path_steps == ["parent", "parent", "child", "spouse"]:
        return ["nephew_niece"]       

    # parent -> parent -> child = uncle_aunt
    if path_steps == ["parent", "parent", "child"]:
        return ["uncle_aunt"]

    # parent -> child -> child = nephew_niece
    if path_steps == ["parent", "child", "child"]:
        return ["nephew_niece"]

    # spouse -> parent -> child -> child
    # source is spouse of uncle/aunt of target
    if path_steps == ["spouse", "parent", "child", "child"]:
        return ["spouse_of_uncle_aunt"] 
    
    # parent -> parent = grandparent
    if path_steps == ["parent", "parent"]:
        return ["grandparent"]

    # child -> child = grandchild
    if path_steps == ["child", "child"]:
        return ["grandchild"]
    

    return ["unknown"]