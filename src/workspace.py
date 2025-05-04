workspaces = [
    {
        "num": "1", # Optional
        "name": "one", # Optional
        "focus": "$mod+1", # Optional
        "move": "$mod+Shift+1", # Optional
    }
]
from sequence import default_sequence  # Assuming this is defined in another file

class Workspace:
    def __init__(self,
        num: int=None,
        name: str=None,
        focus_binding: int=None,
        focus_modifier: str='$mod',
        move_binding: int=1,
        move_modifier: str='$mod+Shift'):
        
        self._num = num
        self.name = name
        self.focus_modifier = focus_modifier
        self.focus_binding = focus_binding
        self.move_modifier = move_modifier
        self.move_binding = move_binding
        
        if self._num is None:
            self._num = 1  # Default start number if none provided.

    def display_info(self):
        print(f"Workspace Name: {self.name}")

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        if value < 0:
            raise ValueError("Workspace number cannot be negative.")
        self._num = value

    def identifier(self) -> str:
        # Use the sequence for identifier generation (not the actual 'num')
        sequence_value = self._get_sequence_for_key(self.num)
        name = self.name.replace(" ", "_") if self.name else "" 
        return f"$ws{self.num}_{sequence_value}_{name}" if name else f"$ws{self.num}_{sequence_value}"

    def value(self):
        return f"{self.num}:\"{self.name}\""

    def focus_keys(self) -> str:
        # Use the sequence for keybindings, while keeping 'num' as an integer for the workspace number
        if self.focus_binding is None:  # If not explicitly set, generate automatically
            return f"{self.focus_modifier}+{self._get_sequence_for_key(self.num)}"
        else:  # User explicitly set the focus keybinding
            return f"{self.focus_modifier}+{self.focus_binding}"

    def move_keys(self) -> str:
        if self.move_binding is None:  # If not explicitly set, generate automatically
            return f"{self.move_modifier}+{self._get_sequence_for_key(self.num)}"
        else:  # User explicitly set the move keybinding
            return f"{self.move_modifier}+{self.move_binding}"

    def _get_sequence_for_key(self, num: int) -> str:
        """ Helper method to fetch the appropriate sequence character for num. """
        return default_sequence()[num % len(default_sequence())]  # Wrap around the sequence

    # Add this method to apply defaults
    def apply_defaults(self, defaults):
        self.focus_modifier = defaults.get('focus_modifier', self.focus_modifier)
        self.move_modifier = defaults.get('move_modifier', self.move_modifier)