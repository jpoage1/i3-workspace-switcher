import re

def get_i3_keybindings(i3_config_path: str) -> set:
    """Extract keybindings from i3 config file."""
    keybindings = set()
    
    try:
        with open(i3_config_path, "r") as file:
            config_data = file.read()
            
            # Regular expression to match keybindings (bindsym)
            keybinding_pattern = r"bindsym\s+([^\s]+)"
            matches = re.findall(keybinding_pattern, config_data)
            
            # Add matched keybindings to the set
            for match in matches:
                keybindings.add(match)
    except FileNotFoundError:
        print(f"i3 config file not found: {i3_config_path}")
    
    return keybindings

def defaultSequence():
    """Generate the sequence of letters and numbers."""
    numbers_sequence = [chr(ascii_value) for ascii_value in range(48, 58)]  # 0-9
    lower_case_sequence = [chr(ascii_value) for ascii_value in range(97, 123)]  # a-z
    upper_case_sequence = [chr(ascii_value) for ascii_value in range(65, 91)]  # A-Z
    return lower_case_sequence + upper_case_sequence  # a-z, A-Z

def generate_keybindings(i3_keybindings: set, sequence: list, modifier: str) -> list:
    """Generate keybindings, skipping already used ones and ensuring no overlap."""
    generated_keybindings = []
    for letter in sequence:
        # Check if the keybinding already exists
        if letter in i3_keybindings:
            continue  # Skip this letter if it's already in use
        if letter.isupper():
            # For uppercase letters, we need the Shift modifier
            keybinding = f"{modifier}+Shift+{letter.lower()}"
        else:
            # For lowercase letters, no Shift modifier
            keybinding = f"{modifier}+{letter}"
        
        # Add the keybinding to the list and the set
        generated_keybindings.append(keybinding)
        i3_keybindings.add(letter)  # Mark this key as used
    
    return generated_keybindings

# Example usage
i3_config_path = "~/.config/i3/config"  # Adjust path if necessary
modifier = "Mod4"  # This can be different for each workspace group

# Get i3 keybindings from the config file
i3_keybindings = get_i3_keybindings(i3_config_path)

# Generate keybindings using the default sequence and the provided modifier
sequence = defaultSequence()
generated_keybindings = generate_keybindings(i3_keybindings, sequence, modifier)

print("Generated keybindings:", generated_keybindings)
