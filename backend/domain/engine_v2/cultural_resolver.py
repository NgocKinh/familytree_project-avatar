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
        
