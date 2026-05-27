# ======================================================
# LUNAR CAN CHI UTILS
# ======================================================

CAN_LIST = [
    "Giáp", "Ất", "Bính", "Đinh", "Mậu",
    "Kỷ", "Canh", "Tân", "Nhâm", "Quý"
]

CHI_LIST = [
    "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
    "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"
]


def get_can_chi_year(year: int) -> str:
    can = CAN_LIST[(year + 6) % 10]
    chi = CHI_LIST[(year + 8) % 12]

    return f"{can} {chi}"