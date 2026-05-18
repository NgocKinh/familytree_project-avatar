from backend.domain.policies.marriage_policy import DefaultMarriagePolicy


def create_marriage_policy(**kwargs):
    return DefaultMarriagePolicy(**kwargs)