bl_info = {
    "name": "Quick Interpolation",
    "description": "Batch apply texture interpolation settings for all materials in a scene or for the active material.",
    "author": "Austin Egge",
    "version": (1, 0, 0),   
    "blender": (3, 0, 0),
    "category": "Material",
}

import bpy

# Function to set interpolation for the image textures
def set_interpolation(interpolation_type, apply_to_all, context):
    texture_count = 0
    if apply_to_all == 'ALL':
        # Loop through all materials
        for material in bpy.data.materials:
            if material.node_tree:  # Skip materials without node trees
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':  # Only modify image texture nodes
                        node.interpolation = interpolation_type
                        texture_count += 1
    else:
        # Only loop through the active material
        active_material = context.active_object.active_material
        if active_material and active_material.node_tree:
            for node in active_material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':  # Only modify image texture nodes
                    node.interpolation = interpolation_type
                    texture_count += 1
    return texture_count

# Operator to run the main function
class QuickInterpolationOperator(bpy.types.Operator):
    bl_idname = "material.quick_interpolation_set"
    bl_label = "Quick Interpolation: Set Interpolation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        interpolation_type = context.scene.quick_interpolation_type
        apply_to_all = context.scene.quick_interpolation_apply_to_all
        texture_count = set_interpolation(interpolation_type, apply_to_all, context)
        # Report the result
        self.report({'INFO'}, f"Set {texture_count} texture(s) to {interpolation_type}.")
        return {'FINISHED'}

# Panel for Material Properties
class QuickInterpolationPanel(bpy.types.Panel):
    # Creates a panel in the Material Properties tab
    bl_label = "Quick Interpolation"
    bl_idname = "MATERIAL_PT_quick_interpolation"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    # Adds the panel to the Material tab
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown for selecting interpolation type
        layout.label(text="Interpolation Type:")
        layout.prop(scene, "quick_interpolation_type", text="")

        # Dropdown for selecting apply to all materials or active material
        layout.label(text="Apply to:")
        layout.prop(scene, "quick_interpolation_apply_to_all", text="")

        # Button to run the operator
        layout.operator("material.quick_interpolation_set", text="Apply Interpolation")

# Registering custom properties
def register():
    # Register properties to store the dropdown selections
    bpy.types.Scene.quick_interpolation_type = bpy.props.EnumProperty(
        name="Interpolation Type",
        items=[
            ('Closest', 'Closest', 'Use Closest interpolation (sharp)'),
            ('Linear', 'Linear', 'Use Linear interpolation (smooth)'),
            ('Cubic', 'Cubic', 'Use Cubic interpolation (smooth, high quality)'),
            ('Smart', 'Smart', 'Use Smart interpolation (bicubic when magnifying, else bilinear)'),
        ],
    )

    bpy.types.Scene.quick_interpolation_apply_to_all = bpy.props.EnumProperty(
        name="Apply To",
        items=[
            ('ALL', 'All Textures in Scene', 'Apply to all textures in the scene'),
            ('SELECTED', 'Textures in Active Material', 'Apply to textures in the active material'),
        ],
        default='SELECTED',
    )

    bpy.utils.register_class(QuickInterpolationOperator)
    bpy.utils.register_class(QuickInterpolationPanel)

def unregister():
    # Unregister properties and classes
    del bpy.types.Scene.quick_interpolation_type
    del bpy.types.Scene.quick_interpolation_apply_to_all
    bpy.utils.unregister_class(QuickInterpolationOperator)
    bpy.utils.unregister_class(QuickInterpolationPanel)

if __name__ == "__main__":
    register()