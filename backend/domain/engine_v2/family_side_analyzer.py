# ==========================================================
# FAMILY SIDE ANALYZER
# ==========================================================

def detect_side(path):
    """
    Determine paternal / maternal branch from path roles.
    father -> paternal
    mother -> maternal
    """

    for node, rel, role in path:
        if role == "father":
            return "paternal"

        if role == "mother":
            return "maternal"

    return None