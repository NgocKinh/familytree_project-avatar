from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db

from backend.domain.relation_path_utils import find_shortest_path_db
router = APIRouter()
from backend.domain.engine_v2.relationship_resolver import resolver_relationship
from backend.domain.engine_v2.relationship_engine import (
    resolve_relationship
)

# def infer_relationship(path):
#     if not path:
#         return "unknown"

#     relations = [rel for _, rel, _ in path]

#     # STEP PARENT
#     if relations == ["SPOUSE", "SPOUSE", "PARENT"]:
#         return "step-parent"

#     # PARENT
#     if relations == ["PARENT"]:
#         return "parent"

#     # CHILD
#     if relations == ["CHILD"]:
#         return "child"

#     # UNCLE / AUNT
#     if relations == ["PARENT", "CHILD", "PARENT"]:
#         return "uncle/aunt"

#     return "unknown"


# def map_gendered_relationship(base_relation, gender):
#     if base_relation == "step-parent":
#         if gender == "male":
#             return "step-father"
#         elif gender == "female":
#             return "step-mother"
#         return "step-parent"

#     return base_relation


@router.get("/api/relationship")
def get_relationship(
    source_id: int,
    target_id: int,
    db: Session = Depends(get_db)
):
    # SELF
    if source_id == target_id:
        return {
            "relationship": "self",
            "path": [source_id],
            "metadata": {}
        }

    # 1. FIND PATH
    path = find_shortest_path_db(source_id, target_id, db)

    # 2. ENGINE_V2 RESOLVER
    new_result = resolve_relationship(source_id, target_id)

    if new_result and new_result.get("normalized") in (
        ["sibling_in_law"],
        ["affinity_peer"]
    ):
        result = new_result
    else:
        result = resolver_relationship(source_id, target_id)

    return {
        "source_id": source_id,
        "target_id": target_id,
        **result
    }