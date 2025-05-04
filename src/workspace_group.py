from workspace import Workspace
from workspaces import Workspaces
from workspace_manager import WorkspaceManager

class WorkspaceGroup:
    def __init__(self, name: str='', modifier: str='Mod4', workspaces: Workspaces = []):
        self.name = name
        self.modifier = modifier
        self.workspaces = workspaces  # list of workspaces in the group
        self.manager = WorkspaceManager()

    def create_group(self, workspace_names):
        for name in workspace_names:
            self.manager.create_workspace(name)

    def display_group(self):
        print(
            f"Workspace Group {self.name} Details:\n"
            f"Name: {self.name}\n"
            f"Modifier: {self.modifier}\n"
            f"Workspaces Count: {len(self.workspaces)}\n",
            sep = "\n"
        )
        self.manager.list_workspaces()
        