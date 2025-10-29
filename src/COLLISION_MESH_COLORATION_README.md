# Collision mesh coloration
This document aims to provide guidance for the manual coloration of Collada (.dae) collision meshes for the Weld cell
The package for this documentation is located in the ROS_FLEXARC_DT directory on David Johnsons GU502GV
## Important modifications
### `<library_effects>` and `<library_materials>`
Underneath the `<assets>` and before the `<library_geometries>` chunk of the .dae file, the following code snippets should be added.
```
    <library_effects>
        <effect id="ID1">
        <profile_COMMON>
            <technique sid="COMMON">
            <phong>
                <emission>
                <color>0 1 0 1</color>
                </emission>
                <ambient>
                <color>0 1 0 1</color>
                </ambient>
                <diffuse>
                <color>0 1 0 1</color>
                </diffuse>
                <specular>
                <color>0 1 0 1</color>
                </specular>
            </phong>
            </technique>
        </profile_COMMON>
        </effect>
    </library_effects>
    <library_materials>
        <material id="ID2">
        <instance_effect url="#ID1" />
        </material>
    </library_materials>
```

In the `<triangles>` section above `</mesh>`, a user should see a `count=#` parameter. next to this, you should add a new parameter `material="ID9` inside the brackets. 

Finally, in the `<library_visual_scenes>`, underneath `<instance_geometry>`, you should add the following code block. 
```
                <instance_geometry url="#shape0-lib">
                    <bind_material>
                        <technique_common>
                            <instance_material symbol="ID9" target="#ID2" />
                        </technique_common>
                    </bind_material>
                </instance_geometry>
```
note that in `<instance_geometry>`, the close bracked has been moved to the bottom of this code block with `</instance_geometry>`. 

This should be all of the modifications made manually to modify .dae mesh coloration in RVIZ without creating any significant breaks in mesh loading. 

### Specific Color RGB values
|Color | r g b a (normalized)|
| --- | :---: |
|Maroon | .3 0 0 1|
|Orange | 

## Warnings
Be careful if using "replace all" to change the color definition, it will change vertex values if you are not careful and it will crash rviz

