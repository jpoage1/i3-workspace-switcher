from typing import Optional
import os
from workspace import Workspace
from workspaces import Workspaces
from workspace_group import WorkspaceGroup
from typing import TextIO
from workspace_groups import WorkspaceGroups

class WriteConfig():
    def __init__(self,
        workspace_groups: WorkspaceGroups,
        output_path: str = "output.conf") -> None:
        # Normalize to list of Workspaces
        if isinstance(workspace_groups, WorkspaceGroups):
            self.workspace_groups = workspace_groups
        elif isinstance(workspace_groups, WorkspaceGroup):
            self.workspace_groups = WorkspaceGroups()
            self.workspace_groups.add(workspace_groups)
        elif isinstance(workspace_groups, list):
            self.workspace_groups = WorkspaceGroups(workspace_groups)
        else:
            raise TypeError("Expected Workspaces or list of Workspaces objects")

        self.output_path = os.path.expanduser(output_path)
        # self.workspace = workspace


    def write_line(self, fp: TextIO, line: str) -> None:
        fp.write(f"{line.strip()}\n")

    def write_workspace(self, fp: TextIO, ws: Workspace, index: Optional[int] = None) -> None:
        """ Workspace Switcher.write_workspace """
        ws_name = ws.name or ''
        value = ws.value()
        identifier = ws.identifier()
        self.write_line(fp, f"# Workspace {ws.num}: {ws_name}")
        self.write_line(fp, f"set {identifier} {value}")
        self.write_line(fp, f"workspace {value} output $monitor_one")
        self.write_line(fp, f"bindsym {ws.focus_keys()} workspace number {identifier}")
        self.write_line(fp, f"bindsym {ws.move_keys()} move container to workspace number {identifier}")
    

    def write_all(self) -> None:
        """ WorkspaceSwitcher.write_all """
        with open(self.output_path, "w") as fp_write:
            for idx, group in enumerate(self.workspace_groups):
                group_name = f"Workspace Group {ws.name} at {idx+1}" if group.name else "Workspace Group {idx+1}"
                
                if not hasattr(group, "workspaces"):
                    raise AttributeError(f"{group_name} missing required 'workspaces' attribute")

                self.write_line(fp, f"\n# === {group_name} ===")
                for ws in group.workspaces:
                    self.write_workspace(fp, ws)