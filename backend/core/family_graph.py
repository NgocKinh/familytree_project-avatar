from collections import defaultdict


class FamilyGraph:

    def __init__(self):
        self.graph = defaultdict(list)
        self.children = defaultdict(list)
        
    def add_edge(self, a, b, relation):
        self.graph[a].append((relation, b))

    def build(self, marriages, parent_child_rows):

        # spouse
        for m in marriages:
            a = m["spouse_a_id"]
            b = m["spouse_b_id"]

            self.add_edge(a, b, "spouse")
            self.add_edge(b, a, "spouse")

        # parent-child
        for row in parent_child_rows:

            parent = row["parent_id"]
            child = row["child_id"]

            self.children[parent].append(child)

            self.add_edge(parent, child, "child")
            self.add_edge(child, parent, "parent")
        # build sibling edges
        for parent, kids in self.children.items():

            for i in range(len(kids)):
                for j in range(i + 1, len(kids)):

                    a = kids[i]
                    b = kids[j]

                    self.add_edge(a, b, "sibling")
                    self.add_edge(b, a, "sibling")
                    
        return self.graph
