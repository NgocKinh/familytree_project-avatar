def build_call(call_north=None, call_south=None, fallback=None):
    """
    Chuẩn hóa call cho toàn bộ hệ thống
    """

    if call_north or call_south:
        return {
            "north": call_north,
            "south": call_south
        }

    if fallback:
        return {
            "north": fallback,
            "south": fallback
        }

    return None