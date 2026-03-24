from typing import List
from fastapi import HTTPException

from app.database import get_person_by_id
from app.relation_engine_v2 import RelationEngineV2

from app.core.blood_engine import BloodEngine
from app.core.relationship_candidate import RelationshipCandidate
from app.core.priority_conflict_engine import PriorityConflictEngine
from app.core.affinity_engine import AffinityResolverEngine

from backend.services.family_graph_service import build_family_graph
from backend.core.path_finder import bfs_kinship_path


class RuleEngine:

    def resolve(self, path):
        print("🔥 RULE ENGINE ACTIVE 🔥")

        if not path:
            return None

        # ===== DIRECT CASE =====
        if len(path) == 1:
            _, rel, _ = path[0]
            if rel == "spouse":
                return "spouse"

        # ===== BUILD FEATURES =====
        has_spouse = any(rel == "spouse" for _, rel, _ in path)

        direction = []
        for _, rel, _ in path:
            if rel == "parent":
                direction.append("UP")
            elif rel == "child":
                direction.append("DOWN")

        relations = [rel for _, rel, _ in path]
        print("RELATIONS DEBUG:", relations)

        # =====================================================
        # ===== AFFINITY RULES (ƯU TIÊN TRƯỚC) =====
        # =====================================================

        if relations == ["spouse", "parent"]:
            return "parent_in_law"

        if relations == ["spouse", "sibling"]:
            return "sibling_in_law"

        if relations == ["sibling", "spouse"]:
            return "sibling_in_law"

        if relations == ["spouse", "child"]:
            return "step_child"

        if relations == ["parent", "spouse"]:
            return "step_parent"

        if relations == ["child", "spouse"]:
            return "child_in_law"
        # =====================================================
        # ===== BLOOD RULES =====
        # =====================================================

        if direction == ['UP']:
            return "parent"

        if direction == ['DOWN']:
            return "child"

        if direction == ['UP', 'UP']:
            return "grandparent"

        if direction == ['DOWN', 'DOWN']:
            return "grandchild"

        if direction == ['UP', 'DOWN']:
            return "sibling"

        if direction == ['UP', 'UP', 'DOWN']:
            return "uncle/aunt"

        if direction == ['UP', 'DOWN', 'DOWN']:
            return "nephew/niece"

        if direction == ['UP', 'UP', 'DOWN', 'DOWN']:
            return "cousin"

        # ===== DEEP RULES =====

        if all(d == "UP" for d in direction) and direction:
            level = len(direction)
            if level == 1:
                return "parent"
            elif level == 2:
                return "grandparent"
            else:
                return "great-" * (level - 2) + "grandparent"

        if all(d == "DOWN" for d in direction) and direction:
            level = len(direction)
            if level == 1:
                return "child"
            elif level == 2:
                return "grandchild"
            else:
                return "great-" * (level - 2) + "grandchild"

        return None

    def to_vietnamese(self, relation, gender_list):
        if relation is None:
            return None

        gender = gender_list[-1] if gender_list else "M"

        base_map = {
            "parent": {"M": "bố", "F": "mẹ"},
            "child": {"M": "con trai", "F": "con gái"},
            "spouse": {"M": "chồng", "F": "vợ"},
            "sibling": {"M": "anh/em trai", "F": "chị/em gái"},

            "parent_in_law": {"M": "bố vợ", "F": "mẹ vợ"},
            "child_in_law": {"M": "con rể", "F": "con dâu"},
            "sibling_in_law": {"M": "anh/em rể", "F": "chị/em dâu"},

            "step_parent": {"M": "cha dượng", "F": "mẹ kế"},
            "step_child": {"M": "con riêng", "F": "con riêng"},
        }

        if relation in base_map:
            return base_map[relation].get(gender, base_map[relation]["M"])

        return relation

class RelationshipResolver:

    def __init__(self):
        self.rule_engine = RuleEngine()

    def resolve(self, source_id: int, target_id: int) -> dict:
        final_relation = None
        gender_list = []
        print("SOURCE =", source_id)
        print("TARGET =", target_id)
        print("RESOLVER VERSION TEST")

        candidates: List[RelationshipCandidate] = []

        # -----------------------------
        # BUILD GRAPH
        # -----------------------------
        graph = build_family_graph()

        print("DEBUG GRAPH NODE 110:", graph.get(110))
        print("DEBUG GRAPH NODE 106:", graph.get(106))
        print("DEBUG GRAPH NODE 124:", graph.get(124))

        # -----------------------------
        # BFS PATH (V3B3)
        # -----------------------------
        path = bfs_kinship_path(graph, source_id, target_id)

        print("KINSHIP PATH:", path)
        print("DEBUG PATH:", path)

        # -----------------------------
        # RULE ENGINE
        # -----------------------------
        new_relation = self.rule_engine.resolve(path)
        print("RULE ENGINE =", new_relation)

        # -----------------------------
        # BLOOD ENGINE (LEGACY)
        # -----------------------------
        if path:

            blood_engine = BloodEngine()
            blood_candidates = blood_engine.resolve(source_id, target_id, path)

            direction_list = []
            gender_list = []
            lineage_list = []

            person_cache = {}

            for node, relation, neighbor in path:

                if relation == "parent":
                    direction_list.append("UP")
                    lineage_list.append("P")

                elif relation == "child":
                    direction_list.append("DOWN")

                else:
                    continue

                if neighbor not in person_cache:
                    person_cache[neighbor] = get_person_by_id(neighbor)

                person = person_cache[neighbor]

                if not person:
                    gender = "M"
                else:
                    g = person["gender"]
                    if g == "male":
                        gender = "M"
                    elif g == "female":
                        gender = "F"
                    else:
                        gender = "M"

                gender_list.append(gender)

            depth = len(direction_list)

            print("DEBUG direction_path:", direction_list)
            print("DEBUG gender_path:", gender_list)
            print("DEBUG lineage_path:", lineage_list)

            relation_name = RelationEngineV2.classify(
                direction_list,
                gender_list,
                lineage_list,
                depth
            )

            # ===== RULE ENGINE PRIORITY =====
            if new_relation is not None:
                print("USING RULE ENGINE RESULT")
                final_relation = new_relation
            else:
                print("FALLBACK TO LEGACY")
                final_relation = relation_name

            if blood_candidates:
                blood_candidates[0].name = relation_name
                blood_candidates[0].priority = 1

            candidates.extend(blood_candidates)

        # -----------------------------
        # AFFINITY ENGINE (OPTIONAL)
        # -----------------------------
        affinity_engine = AffinityResolverEngine()
        affinity_candidates = affinity_engine.resolve(source_id, target_id)

        candidates.extend(affinity_candidates)

        # -----------------------------
        # RESULT SELECTION
        # -----------------------------
        print("CANDIDATES:", candidates)

        if final_relation is None and not candidates:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy quan hệ"
            )

        engine = PriorityConflictEngine()
        best = engine.resolve(candidates)

        if best:
            print("DEBUG RELATION (LEGACY) =", best.name)
        else:
            print("DEBUG RELATION (RULE ENGINE) =", final_relation)


        vn_relation = self.rule_engine.to_vietnamese(final_relation, gender_list)

        return {
            "source_id": source_id,
            "target_id": target_id,
            "relationship": vn_relation
        }
