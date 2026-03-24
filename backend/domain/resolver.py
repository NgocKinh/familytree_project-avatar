def resolve_relationship(path):

    if not path:
        return "no relation"

    relations = [step[1] for step in path]

    # parent
    if relations == ['parent']:
        return "parent"

    # child
    if relations == ['child']:
        return "child"

    # spouse
    if relations == ['spouse']:
        return "spouse"

    # grandparent
    if relations == ['parent','parent']:
        return "grandparent"

    # grandchild
    if relations == ['child','child']:
        return "grandchild"

    # sibling
    if relations == ['parent','child']:
        return "sibling"

    # parent-in-law
    if relations == ['spouse','parent']:
        return "parent-in-law"

    # child-in-law
    if relations == ['child','spouse']:
        return "child-in-law"

    # grandchild-in-law
    if relations == ['child','child','spouse']:
        return "grandchild-in-law"

    return "complex relation"
