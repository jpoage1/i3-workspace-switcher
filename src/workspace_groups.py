from workspace_group import WorkspaceGroup
class WorkspaceGroups:
    def __init__(self):
        self.groups = []  # List of WorkspaceGroup objects

    def add(self, group: WorkspaceGroup):
        """Add a WorkspaceGroup to the list."""
        self.groups.append(group)

    def display_all_groups(self):
        """Display all workspace groups."""
        print("Listing All Workspace Groups:")
        for group in self.groups:
            group.display_group()

    def create_group(self, modifier: str, workspace_names: list[str]):
        """Create a WorkspaceGroup and add it to the list."""
        group = WorkspaceGroup(modifier)
        group.create_group(workspace_names)
        self.add_group(group)
        print(f"Created Workspace Group with Modifier: {modifier}")