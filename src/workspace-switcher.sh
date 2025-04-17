#!/bin/bash

MODULE_NAME="workspace_switcher"
HOOK_INDEX=1
LOCKFILE="/tmp/polybar-ipc-$MODULE_NAME.lock"

rofi_menu() {
  rofi -dmenu -p "$@"
}
dmenu_menu() {
  dmenu -i -p  "$@"
}

scroll() {
  direction="$1"
  cache_file="/tmp/polybar-ws-index"

  # Load current index
  if [[ -f $cache_file ]]; then
      index=$(<"$cache_file")
  else
      index=0
  fi

  # Update index
  count=${#WORKSPACES_ARRAY[@]}
  if [[ "$direction" == "up" ]]; then
      ((index++))
  elif [[ "$direction" == "down" ]]; then
   if [ "$index" -lt 1 ]; then
      index=0
    else
      ((index--))
    fi
  fi
  # Save new index
  echo "$index" > "$cache_file"

}
workspace_bar() {

  current_index=0
  cache_file="/tmp/polybar-ws-index"

  # Load saved index
  if [[ -f $cache_file ]]; then
      current_index=$(<"$cache_file")
  fi

  # Clamp index
  [[ $current_index -lt 0 ]] && current_index=0
  max_index=$((${#WORKSPACE_ARRAY[@]} - 5))
  [[ $current_index -gt $max_index ]] && current_index=$max_index

  num_workspaces=10

  current=$(i3-msg -t get_workspaces | jq -r '.[] | select(.focused==true).name')
  echo -n "%{u#00ff00 +u}$(workspace_item "$current")%{u-} "
  echo -n "%{A1:workspace-switcher scroll=down :}    ⬅️  %{A}"
  echo -n "     %{A1:workspace-switcher scroll=up:}➡️    %{A} "
  echo -n "%{A4:workspace-switcher scroll=up :}%{A5:workspace-switcher scroll=down :}"

  for ((i = current_index; i < current_index + $num_workspaces && i < ${#WORKSPACE_ARRAY[@]}; i++)); do
    ws="${WORKSPACE_ARRAY[i]}"
    item=$(workspace_item "$ws")
    if [[ "$ws" != "$current" ]]; then
      echo -n "$item "
    else
      ((num_workspaces++))
    #   echo -n "%{u#00ff00 +u}$item%{u-} "
    fi
  done
  echo -n "%{A}%{A}"
  echo -n "%{A1:workspace-switcher scroll=up:}    ➡️    %{A} "
  echo
}
workspace_item() {
    ws="$1"
    name="${ws#*:}"
    number="${ws%%:*}"
    name=${name//\"/}
    [[ "$name" == "$number" ]] && label="${name:-$number}" || label="$number $name"
    cmd_prefix="workspace-switcher ws=\"$number|$name\""
    echo -n "%{A1:$cmd_prefix switch:}%{A3:$cmd_prefix move:}%{A2:$cmd_prefix shift:}$label%{A}%{A}%{A} "
}


find_workspace_config() {
  # Try to find a match
  for path in "${valid_paths[@]}"; do
    file_content=$(<"$path")
    if [[ "$file_content" == "$config_from_i3" ]]; then
      # echo "✅ i3 is using this config file: $path" >&2
      export WORKSPACE_CONFIG="$path"
    fi
  done
  if [[ -z $WORKSPACE_CONFIG ]]; then
      echo "❌ No config file on disk matches the one loaded in memory." >&2
      echo "If you are using a config from a non-standard location, ensure" >&2
      echo "you are using absolute paths for resolving includes in your i3-config." >&2
      echo "Alternatively, pass the --config=/path/to/config if you are using includes." >&2
  fi
}
parse_workspace_lines() {
  workspace_lines="$1"
  # Rewrite each line, resolving variables
  while read -r line; do
    ws_var=$(echo "$line" | awk '{print $2}')
    mon_var=$(echo "$line" | awk '{print $4}')

    ws_val="${vars[$ws_var]}"
    mon_val="${vars[$mon_var]}"

    if [[ -n "$ws_val" && -n "$mon_val" ]]; then
      echo "workspace \"$ws_val\" output $mon_val"
    else
      # Leave the line untouched if the variable isn't found
      echo "$line"
    fi
  done <<< "$workspace_lines"
}
# resolve_includes() {
#   local input="$1"
#   local base_dir="$2"
#   local output=""

#   while IFS= read -r line; do
#     if [[ "$line" =~ ^include[[:space:]]+(.+) ]]; then
#       include_path=$(eval echo "${BASH_REMATCH[1]}")
#       # Resolve relative paths against the base directory
#       if [[ "$include_path" != /* ]]; then
#         include_path="$base_dir/$include_path"
#       fi
#       if [[ -f "$include_path" ]]; then
#         included_content=$(<"$include_path")
#         included_base_dir=$(dirname "$include_path")
#         included_resolved=$(resolve_includes "$included_content" "$included_base_dir")
#         output+="$included_resolved"$'\n'
#       else
#         echo "Warning: included file '$include_path' not found." >&2
#       fi
#     else
#       output+="$line"$'\n'
#     fi
#   done <<< "$input"

#   echo "$output"
# }
# get_workspaces() {
#     local cache_file="/tmp/i3-workspaces.cache"
#   local timestamp_file="/tmp/i3-config.timestamp"
  
#   # Normalize and remove empty/null paths
#   valid_paths=()
#   [[ -n "$CONFIG_PATH" && -f "$CONFIG_PATH" ]] && valid_paths+=("$CONFIG_PATH")
#   for path in "${POSSIBLE_PATHS[@]}"; do
#     [[ -n "$path" && -f "$path" ]] && valid_paths+=("$path")
#   done

#   find_workspace_config

#   # Get the config directory
#   base_dir=$(dirname "$WORKSPACE_CONFIG")
#   # Flatten config
#   flattened_config=$(resolve_includes "$config_from_i3" "$base_dir")

#   # Extract variable definitions
#   declare -A vars
#   while read -r line; do
#     var_name=$(echo "$line" | awk '{print $2}')
#     var_value=$(echo "$line" | cut -d' ' -f3-)
#     vars["$var_name"]="$var_value"
#   done < <(echo "$flattened_config" | grep -E '^set \$[A-Za-z_][A-Za-z0-9_]* .+')

#   # Find workspace lines using variables
#   workspace_lines=$(echo "$flattened_config" | grep -E '^workspace \$[A-Za-z_][A-Za-z0-9_]* output \$[A-Za-z_][A-Za-z0-9_]*')

#   workspaces_names=$(echo "$(parse_workspace_lines "$workspace_lines")" | awk '{print $2}' | sed 's/^"//; s/"$//')
#   echo "$workspaces_names"
# }

get_menu_option() {
  label="$2"
  if [[ -z $MENU_TYPE ]]; then
    if [[ -n $alt_cmd ]]; then
      MENU_TYPE="$alt_cmd"
      echo "⚠️ Using fallback menu type: $MENU_TYPE" >&2
    else
      echo "❌ No menu type provided, and no fallback available." >&2
      exit 1
    fi
  fi

  if ! command -v ${MENU_TYPE%%_*} &>/dev/null; then
    echo "❌ Menu command '${MENU_TYPE%%_*}' not found on system." >&2
    exit 1
  fi
  echo -e "$WORKSPACES" | $MENU_TYPE "$label"
}
get_selected_workspace() {
  label="$1"
  # Get selected workspace
  selected_workspace=$(get_menu_option "$WORKSPACES" "$label")
  if [[ -z "$selected_workspace" ]]; then
    echo "No workspace selected" >&2
    exit 1
  fi
  echo "Selected workspace: $selected_workspace" >&2
  export SELECTED_WORKSPACE=$selected_workspace
}
switch_workspace() {

  # Get the workspace number
  workspace_number=$(echo "$SELECTED_WORKSPACE" | awk '{print $1}')

  # Get the workspace name
  workspace_name=$(echo "$SELECTED_WORKSPACE" | awk '{print $2}')

  # Switch to the workspace
  if [[ -z "$workspace_number" ]]; then
    echo "No workspace number provided, instead received: $SELECTED_WORKSPACE" >&2
    exit 1
  fi
  if [[ -z "$workspace_name" ]]; then
    label=$workspace_number
  else
    label="$workspace_number:\"$workspace_name\""
  fi
  echo "Switching to workspace: $label" >&2
  i3-msg workspace "$label"
}
move_window() {
    # Get the focused window's ID in i3
    focused_window_id=$(i3-msg -t get_tree | jq '.. | select(.focused? == true) | .id')
    echo "Moving window id: $focused_window_id" >&2

    selected_window_num=$(i3-msg -t get_tree | jq --argjson id "$focused_window_id" 'recurse(.nodes[]?, .floating_nodes[]?) | select(.id == $id) | .window')
    echo "With window num: $selected_window_num" >&2

    # Focus the selected workspace and move the focused window to it
    i3-msg [id=$selected_window_num] move window to workspace "$SELECTED_WORKSPACE"
}
shift_workspace() {
    move_window
    switch_workspace
}
cleanup() {
  [[ -f "$LOCKFILE" && "$(cat "$LOCKFILE")" == "$$" ]] && rm -f "$LOCKFILE"
  exit
}
start_ipc_listener() {
  # Only one listener should be running
  if [ -e "$LOCKFILE" ] && kill -0 "$(cat "$LOCKFILE")" 2>/dev/null; then
    echo "Already running"
    return  # Already running
  fi
  echo "Starting background process for workspace-switcher"

  # Save current PID so we know listener is running
  echo $$ > "$LOCKFILE"

  # Clean up on kill/exit
  trap cleanup EXIT INT TERM

  # Start IPC listener in background
  i3-msg -t subscribe '[ "workspace" ]' | while read -r _; do
    polybar_hook
  done &
  #polybar_hook
  exit 0
}
polybar_hook () {
  polybar-msg action "#$MODULE_NAME.hook.$HOOK_INDEX"
}
main() {
  config=""
  ALT_CMD=""
  positional=()
  if [[ "$1" == "--launch" ]]; then
      echo "test"
      polybar_hook
      exit 0
  elif [[ "$1" = "--startup" ]]; then
    echo "Starting Workspace Switcher"
    start_ipc_listener
    return 0
  fi

  # Parse arguments
  for arg in "$@"; do
    case "$arg" in
      -h|--help)
        echo "Usage: $0 [--config=PATH] [-rofi|-dmenu] [switch|move|list]" >&2
        exit 0
        ;;
      --config=*)
        CONFIG_PATH="${arg#*=}"
        ;;
      -rofi)
        mode="menu"
        MENU_TYPE="rofi_menu"
        ;;
      -dmenu)
        mode="menu"
        MENU_TYPE="dmenu_menu"
        ;;
      ws=*)
        ws="${arg#*=}"
        number="${ws%%|*}"
        name="${ws#*|}"
        export SELECTED_WORKSPACE="$number:\"$name\""
        ;;
      scroll=*)
        mode="scroll"
        direction="${arg#*=}"
        ;;
      alt=*)
        ALT_CMD="${arg#*=}"
        ;;
      *)
        positional+=("$arg")
        ;;
    esac
  done

  command=${positional[0]}

  if [[ "$mode" = "scroll" ]]; then
    if [[ "$direction" = "up" || "$direction" = "down" ]]; then
      scroll "$direction"
      echo "scrolled $direction"
      echo "$@" >> /tmp/polybar-test
    fi
    exit 0
  fi

  # Access:
  # $config    → path to config file
  # $mode      → 'rofi' or 'dmenu'
  # $alt_cmd   → alternate fallback command
  # ${positional[0]} → optional command (e.g., "switch", "reload", etc.)

  # Debug output
  # echo "Config: $config" >&2
  # echo "Menu: $MENU_TYPE" >&2
  # echo "Alt: $ALT_CMD" >&2
  # echo "Command: $command" >&2



  # Possible config paths (in search order)
  POSSIBLE_PATHS=(
    "$CONFIG_PATH"
    "$I3_CONFIG_PATH"
    "$XDG_CONFIG_HOME/i3/config"
    "$HOME/.config/i3/config"
    "$HOME/.i3/config"
    "/etc/i3/config"
  )

  # Get config content in memory
  config_from_i3=$(i3-msg -t get_config)
  
  export WORKSPACES=$(get_workspaces)
  read -ra WORKSPACE_ARRAY <<< "$WORKSPACES"

  export WORKSPACE_ARRAY
  IFS=$'\n' read -r -d '' -a WORKSPACE_ARRAY <<< "$WORKSPACES"

  case "$command" in
    --startup)
      start_ipc_listener
      # workspace_bar
      ;;
    --launch)
      echo "test"
      #polybar_hook
      exit 0
      # workspace_bar
      ;;
    bar)
      # echo "Workspace Bar"
      workspace_bar
      ;;
    list)
      echo "List workspaces" >&2
      echo "$WORKSPACES"
      ;;
    switch)
      echo "Switch workspaces" >&2
      [[ -n "$SELECTED_WORKSPACE" ]] || get_selected_workspace "Go to workspace"
      switch_workspace
      ;;
    shift)
      echo "Shift workspaces" >&2
      [[ -n "$SELECTED_WORKSPACE" ]] || get_selected_workspace "Shift to workspace"
      shift_workspace
      ;;
    move)
      echo "Move Workspaces" >&2
      [[ -n "$SELECTED_WORKSPACE" ]] || get_selected_workspace "Move window to workspace"
      move_window
      ;;
    *)
      echo "Invalid command or no command provided" >&2
      ;;
  esac
}
main "$@" || exit 1
exit 0