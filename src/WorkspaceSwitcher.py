class WorkspaceSwitcher:
    
    # Constructor
    def _init_(self,
        sequence: list=[],
        file: str:None,
        files: list:[],
        export: str:None):
        """ Workspace Switcher Constructor """
        self.file = file
        self.files = files
        self.export = export
        if sequence.len() > 0:
            self.sequence = sequence
        else
            self.sequence = self.defaultSequence()

        if self.imports is list:
            self.input_files = os.path.expanduser(input_file) for input_file in self.imports
        else
            self.input_files = os.path.expanduser(input_file)
        """ Workspaces Constructor """
        self.defaults = defaults or {
            'sequence': self.defaultSequence,
        }

        # Really hope nobody resorts to this
    def defaultSequence():
        # ASCII values for 0-9 are 48-57
        # ASCII values for a-z are 97-122
        # ASCII values for A-Z are 65-90

        # Create a sequence of numbers (0-9), lowercase letters (a-z), and uppercase letters (A-Z)
        numbers_sequence = [chr(ascii_value) for ascii_value in range(48, 58)]  # 0-9
        lower_case_sequence = [chr(ascii_value) for ascii_value in range(97, 123)]  # a-z
        upper_case_sequence = [chr(ascii_value) for ascii_value in range(65, 91)]  # A-Z

        # Combine all sequences
        return numbers_sequence + lower_case_sequence + upper_case_sequence
