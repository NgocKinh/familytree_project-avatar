# =========================
# 🔥 xác định cách gọi
# =========================
def resolve_uncle_aunt_call(gender_b, side, older):

    if gender_b == "male":
        if older:
            call_south = "bác"
        else:
            call_south = "chú" if side == "paternal" else "cậu"

    else:
        if side == "paternal":
            call_south = "cô"
        else:
            call_south = "dì"

    call_north = call_south

    if call_south == "dì":
        call_north = "cô"

    return call_north, call_south

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
