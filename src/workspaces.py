workspaces = [
    {
        "num": "1", # Optional
        "name": "one", # Optional
        "focus": "$mod+1", # Optional
        "move": "$mod+Shift+1", # Optional
    }
]
from workspace import Workspace

class Workspaces():
    def __init__(self,
        workspaces: list[Workspace]=None,
        focus_modifier: str = '$mod',
        move_modifier: str = 'mod_shift',
        sequence: list = [] ):
        """ Workspaces Constructor """
        self.defaults: dict[str,str] = {
            'focus_modifier': focus_modifier,
            'move_modifier': move_modifier
        }
        self.workspaces: list[Workspace] = []
        

         # Apply defaults and create workspacesif workspaces:
        for ws in workspaces:
            if isinstance(ws, Workspace):
                ws.apply_defaults(self.defaults)
                self.workspaces.append(ws)
            elif isinstance(ws, dict):
                workspace_obj = Workspace(**ws)
                workspace_obj.apply_defaults(self.defaults)
                self.workspaces.append(workspace_obj)

        self.focus_modifier = focus_modifier
        self.move_modifier = move_modifier
        self.sequence = sequence if len(sequence) > 0 else self.getDefaultSequence()
    
    def get_default_sequence(self) -> list:
        """
        Returns the default sequence of workspace numbers, auto-incremented.
        """
        return [workspace.num for workspace in self.workspaces]

    def add(self, workspace) -> None:
        if isinstance(workspace, Workspace):
            if workspace in self.workspaces:
                raise ValueError(f"Workspace {workspace.num} already added.")
            self.workspaces.append(workspace)
            
            # Ensure it's given a unique num if not set
            if workspace.num is None:
                workspace.num = self._get_next_available_number()
            self.workspaces.append(workspace)