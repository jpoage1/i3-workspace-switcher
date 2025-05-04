#!/usr/bin/env python3

import os
input_file = "~/.config/i3/workspace-list.txt"
output_file = "~/.config/i3/generated-workspaces.conf"

def create_worksheet(fp_write, ws_num, ws_name=""):
    ws_name = ws_name.strip()
    ws_identifier = f"$ws{ws_num}"
    key_num = ws_num % 10
    key_mod = "$mod"  # Default key_mod

    # Match statement for modifying key_mod and key_num based on workspace range
    match ws_num:
        case _ if 0 < ws_num <= 10:
            key_mod = "$mod"
        case _ if 10 < ws_num <= 20:
            key_mod = "$mod+$ctrl"
        case _ if 20 < ws_num <= 30:
            key_mod = "$mod+$alt"
        case _ if 30 < ws_num <= 40:
            key_mod = "$mod+$alt+$ctrl"

    # Output the workspace config
    nextline = f"# Workspace {ws_num}: {ws_name}\n"
    print(nextline, end='')
    fp_write.write(nextline)

    # Set workspace
    ws_var_val = f"{ws_num}:\"{ws_name}\"" if ws_name is not "" else f"{ws_num}"
    nextline = f"set {ws_identifier} {ws_var_val}\n"
    print(nextline, end='')
    fp_write.write(nextline)

    # Add workspace output binding
    nextline = f"workspace {ws_identifier} output $monitor_one\n"
    print(nextline, end='')
    fp_write.write(nextline)

    # Bind the workspace to the key
    nextline = f"bindsym {key_mod}+{key_num} workspace number {ws_identifier}\n"
    print(nextline, end='')
    fp_write.write(nextline)

    # move focused container to workspace
    nextline = f"bindsym {key_mod}+Shift+{key_num} move container to workspace number {ws_identifier}\n\n"
    print(nextline, end='')
    fp_write.write(nextline)

input_file = os.path.expanduser(input_file)
output_file = os.path.expanduser(output_file)
with open (input_file, "r") as fp_read:
    with open(output_file, "w") as fp_write:
        for ws_num, ws_name in enumerate(fp_read, start=1):  # Read the file line by line
            create_worksheet(fp_write, ws_num, ws_name)
        for i in range(ws_num+1, 41):
            create_worksheet(fp_write, i)  # You can replace this with whatever logic you need


#  
print(f"Generated workspace config at {output_file}")
