from workspaces import Workspaces
from workspace import Workspace
from sequence import default_sequence  # Assuming this is defined in another file

class WorkspaceManager:
    def __init__(self):
        self.workspace_groups: list[Workspaces] = []
        self.used_identifiers: set[str] = set()
        self.used_focus_keys: set[str] = set()  # Tracks used focus keybindings
        self.used_move_keys: set[str] = set()   # Tracks used move keybindings
        self.sequence = default_sequence()  # Sequence for keybindings
        self.workspaces = []

    def create_workspace(self, name):
        workspace = Workspace(name, default_sequence)
        self.workspaces.append(workspace)
        print(f"Created workspace: {name}")

    def list_workspaces(self):
        print("Listing all workspaces:")
        for workspace in self.workspaces:
            workspace.display_info()
            
    def _get_next_available_number(self) -> str:
        """
        Returns the next available number as an integer.
        """
        # The number will always be an integer, incremented by 1 for each new workspace
        return len(self.workspace_groups) + 1  # This can be adjusted to fit your specific numbering strategy

    def _check_keybinding_conflict(self, keybinding: str, is_focus: bool) -> None:
        """Check for keybinding conflicts for focus or move keys."""
        if is_focus:
            if keybinding in self.used_focus_keys:
                raise ValueError(f"Focus keybinding {keybinding} is already used.")
            self.used_focus_keys.add(keybinding)
        else:
            if keybinding in self.used_move_keys:
                raise ValueError(f"Move keybinding {keybinding} is already used.")
            self.used_move_keys.add(keybinding)

    def _shift_focus_to_move_if_needed(self, needed_focus_keys: int, needed_move_keys: int) -> None:
        """Check if there are enough keybindings, and shift focus to move if needed."""
        total_needed = needed_focus_keys + needed_move_keys
        available_keys = len(self.sequence)
        if total_needed > available_keys:
            # If there aren't enough keys, shift focus keys to move keys
            available_focus_keys = min(needed_focus_keys, available_keys - needed_move_keys)
            for i in range(available_focus_keys, needed_focus_keys):
                # Shift the "focus" keys to "move" keys
                ws = self.workspace_groups[0].workspaces[i]
                ws.move_keys = ws.focus_keys  # Reassign focus to move

    def add_group(self, group: WorkspaceGroup) -> None:
        """Add a workspace group and handle keybinding conflicts."""
        for ws in group.workspaces:
            if ws.num is None:
                ws.num = self._get_next_available_number()

            identifier = ws.identifier()
            if identifier in self.used_identifiers:
                raise ValueError(f"Workspace identifier {identifier} already used.")
            self.used_identifiers.add(identifier)

            # Handle focus and move keybinding conflicts
            if ws.focus_keys() != ws.move_keys():  # Explicitly defined keybindings
                self._check_keybinding_conflict(ws.focus_keys(), is_focus=True)
                self._check_keybinding_conflict(ws.move_keys(), is_focus=False)

        self.workspace_groups.append(group)
        return group


    def add_workspace_to_group(self, group_index: int, workspace: Workspace) -> None:
        """Add workspace to an existing group."""
        if workspace.num is None:
            workspace.num = self._get_next_available_number()

        identifier = workspace.identifier()
        if identifier in self.used_identifiers:
            raise ValueError(f"Workspace identifier {identifier} already used.")
        self.used_identifiers.add(identifier)

        # Handle focus and move keybinding conflicts
        if workspace.focus_keys() != workspace.move_keys():  # Explicitly defined keybindings
            self._check_keybinding_conflict(workspace.focus_keys(), is_focus=True)
            self._check_keybinding_conflict(workspace.move_keys(), is_focus=False)

        self.workspace_groups[group_index].add(workspace)
    
    def resolve_keybinding_conflicts(self):
        """Handles the shifting of keybindings if needed (only when required)."""
        needed_focus_keys = sum(1 for ws in self.workspace_groups[0].workspaces if ws.focus_keys())
        needed_move_keys = sum(1 for ws in self.workspace_groups[0].workspaces if ws.move_keys())

        # Only shift focus to move if necessary, otherwise, leave as is
        self._shift_focus_to_move_if_needed(needed_focus_keys, needed_move_keys)
