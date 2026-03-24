from fastapi import APIRouter
# from app.core.relationship_resolver import RelationshipResolver

router = APIRouter()

# resolver = RelationshipResolver()

@router.get("/api/relationship")
def get_relationship(source_id: int, target_id: int):
    return resolver.resolve(source_id, target_id)