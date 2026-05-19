from backend.domain.engine_v2.data_layer_db import (
    get_gender
)

def render_relationship(a, b, normalized, metadata):

    relation = normalized[0]

    # =====================================
    # SIBLING IN LAW
    # =====================================

    if relation == "sibling_in_law":

        hierarchy = metadata.get("hierarchy")
        kind = metadata.get("kind")

        if kind == "spouse_sibling":

            gender_b = get_gender(b)
            spouse = metadata.get("spouse")
            spouse_gender = get_gender(spouse)

            if spouse_gender == "female":

                if gender_b == "male":
                    if hierarchy == "older":
                        return "anh vợ"
                    return "em vợ"

                if hierarchy == "older":
                    return "chị vợ"
                return "em vợ"

            if spouse_gender == "male":

                if gender_b == "male":
                    if hierarchy == "older":
                        return "anh chồng"
                    return "em chồng"

                if hierarchy == "older":
                    return "chị chồng"
                return "em chồng"

            return relation

        if kind == "sibling_spouse":

            inlaw = metadata.get("inlaw")
            gender_inlaw = get_gender(inlaw)

            if gender_inlaw == "male":
                if hierarchy == "older":
                    return "anh rể"
                return "em rể"

            if hierarchy == "older":
                return "chị dâu"
            return "em dâu"

        return relation
        
    # =====================================
    # SPOUSE OF UNCLE / AUNT
    # =====================================

    if relation == "spouse_of_uncle_aunt":

        side = metadata.get("side")
        gender = metadata.get("gender")
        older = metadata.get("older")

        if side == "paternal":

            if gender == "male":
                if older:
                    return "bác trai"
                return "dượng"

            if older:
                return "bác gái"
            return "thím"

        if side == "maternal":

            if gender == "male":
                return "dượng"

            return "mợ"

        return relation    
    # =====================================
    # AFFINITY PEER
    # =====================================

    if relation == "affinity_peer":

        hierarchy = metadata.get("hierarchy")
        side_context = metadata.get("side_context")
        gender_b = get_gender(b)

        # bên chồng: chị dâu / em dâu
        if side_context == "husband_side":
            if hierarchy == "older":
                return "chị dâu"
            return "em dâu"

        # bên vợ: anh rể / em rể
        if side_context == "wife_side":
            if hierarchy == "older":
                return "anh rể"
            return "em rể"

        # fallback cũ theo gender_b
        if gender_b == "female":
            if hierarchy == "older":
                return "chị dâu"
            return "em dâu"

        if hierarchy == "older":
            return "anh rể"
        return "em rể"

    return relation