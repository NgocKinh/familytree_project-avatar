from app.database import get_family_path
from app.relation_engine_v2 import RelationEngineV2
from app.core.relationship_candidate import RelationshipCandidate, RelationType
import json


class BloodEngine:

    def resolve(self, source_id: int, target_id: int, path=None):
        candidates = []

        if not path:
            return candidates

        directions = []
        gender_path = []
        lineage_path = []

        for node, relation, neighbor in path:

            gender = None
            lineage = None

            if relation == "parent":
                directions.append("UP")
                lineage = "up"

            elif relation == "child":
                directions.append("DOWN")
                lineage = "down"

            elif relation == "spouse":
                continue

            gender_path.append(gender)
            lineage_path.append(lineage)

        # ---- Resolve simple relationships ----

        # Parent
        if directions == ["UP"]:
            candidates.append(
                RelationshipCandidate(
                    name="parent",
                    type=RelationType.BLOOD,
                    priority=1,
                    confidence=1.0
                )
            )

        # Child
        elif directions == ["DOWN"]:
            candidates.append(
                RelationshipCandidate(
                    name="child",
                    type=RelationType.BLOOD,
                    priority=1,
                    confidence=1.0
                )
            )

        # Grandparent
        elif directions == ["UP", "UP"]:
            candidates.append(
                RelationshipCandidate(
                    name="grandparent",
                    type=RelationType.BLOOD,
                    priority=1,
                    confidence=1.0
                )
            )

        # Grandchild
        elif directions == ["DOWN", "DOWN"]:
            candidates.append(
                RelationshipCandidate(
                    name="grandchild",
                    type=RelationType.BLOOD,
                    priority=1,
                    confidence=1.0
                )
            )

        return candidates