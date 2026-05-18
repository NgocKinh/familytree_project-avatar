from backend.domain.relation_rules import RELATION_RULES


def infer_relationship(path):
    if not path:
        return "unknown"

    relations = [rel.strip().upper() for _, rel, _ in path]
    
    key = tuple(relations)

    return RELATION_RULES.get(key, "unknown")
