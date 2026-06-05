from backend.core.exceptions import BadRequestException, AppError 
from backend.constants.marriage_constants import ACTIVE_MARRIAGE_STATUSES
from backend.models.marriage_model import Marriage, MarriageStatus
from sqlalchemy import or_

ALLOW_POLYGAMY = False
class MarriagePolicy:

    def validate_marriage(self, spouse_a, spouse_b, existing_marriage):
        raise NotImplementedError

    def validate_end_marriage(self, marriage, reason):
        raise NotImplementedError


class DefaultMarriagePolicy(MarriagePolicy):

    def validate_marriage(self, spouse_a, spouse_b, existing_marriages):
        # 🔹 self marriage (backup, dù service đã check)
        if spouse_a.id == spouse_b.id:
            raise BadRequestException("Cannot marry yourself")

        # 🔹 same sex (nếu business rule yêu cầu)
        if (
            spouse_a.gender is not None and
            spouse_b.gender is not None and
            spouse_a.gender == spouse_b.gender
        ):
            raise BadRequestException("Same-sex marriage not allowed")

        # 🔹 tách active marriages
        active_marriages = [
            m for m in existing_marriages
            if m.status in ACTIVE_MARRIAGE_STATUSES
        ]

        # 🔹 check từng người
        if not ALLOW_POLYGAMY:
            for m in active_marriages:
                if spouse_a.id in (m.spouse_a_id, m.spouse_b_id):
                    raise AppError(
                        error="ACTIVE_MARRIAGE_EXISTS",
                        message="Thành viên này đã có quan hệ hôn nhân đang còn hiệu lực",
                        details={"person_id": spouse_a.id}
                    )

                if spouse_b.id in (m.spouse_a_id, m.spouse_b_id):
                    raise AppError(
                        error="ACTIVE_MARRIAGE_EXISTS",
                        message="Thành viên này đã có quan hệ hôn nhân đang còn hiệu lực",
                        details={"person_id": spouse_b.id}
                    )

        # 🔹 check duplicate A-B
        for m in existing_marriages:
            if {m.spouse_a_id, m.spouse_b_id} == {spouse_a.id, spouse_b.id}:
                if m.status in ACTIVE_MARRIAGE_STATUSES:
                    raise AppError(
                        error="DUPLICATE_ACTIVE_RELATIONSHIP",
                        message="Active relationship already exists between these two persons",
                        details={
                            "person1_id": spouse_a.id,
                            "person2_id": spouse_b.id
                        }
                    )

        return True

    def validate_end_marriage(self, marriage, reason):

        if marriage.status in [MarriageStatus.divorced, MarriageStatus.widowed]:
            raise BadRequestException("Marriage already ended")

    def can_transition(self, from_status, to_status):
        allowed = {
            "married": {"separated", "divorced", "widowed"},
            "separated": {"married", "divorced"},
            "divorced": {"married"},
            "widowed": {"married"},
            "cohabiting": {"married", "separated"},
        }

        if from_status == to_status:
            return False

        return to_status in allowed.get(from_status, set())