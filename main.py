
# workspace_sequence_0 = Workspaces([
#         Workspace(
#             name="One",
#         ),
#         Workspace(
#             name="Two",
#         ),
#         Workspace(
#             name="Three",
#         ),
#         Workspace(
#             name="Four",
#         ),
#     ],
#     focus_modifier_key="$mod",
# )
# workspace_sequence_1 = Workspaces([
#         Workspace(
#             name="One",
#         ),
#         Workspace(
#             name="Two",
#         ),
#         Workspace(
#             name="Three",
#         ),
#         Workspace(
#             name="Four",
#         ),
#     ],
#     focus_modifier_key="$mod",
# )

# manager = WorkspaceManager()
# manager.add_group(ws_group1)
# manager.add_group(ws_group2)
# manager.add_workspace_to_group(1, Workspace(name="misc"))



# WorkSpaceSwitcher([
#     workspace_sequence
# ])

# ws_collection_1 = Workspaces(workspace_list=workspace_data)
# writer = WriteWorkspaceConfig(ws_collections, "myconfig.conf")
# writer.write_all()

# main.py
from workspace_group import WorkspaceGroup
from write_config import WriteConfig

manager = WorkspaceManager()
# Create a workspace group
group = WorkspaceGroup(modifier="Mod4")
group.create_group(["Workspace 1", "Workspace 2", "Workspace 3"])

# Display all workspaces in the group
group.display_group()

# Now, let's save the configuration for the first workspace
write_config = WriteConfig(group)
write_config.write_all()

custom_sequence = {
    "sequence_id": 2,
    "description": "Custom workspace sequence",
    "settings": {
        "theme": "dark",
        "language": "fr"
    }
}

# Adding the new workspace
group.manager.create_workspace("Custom Workspace")
group.manager.workspaces[-1].sequence = custom_sequence  # Modify its sequence
group.display_group()
