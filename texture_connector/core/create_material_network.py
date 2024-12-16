"""
========================================================================================
Name: create_material_network.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from __future__ import annotations

from maya.api.OpenMaya import MGlobal
import maya.cmds as cmds

from texture_connector.config import UVTilingModes


class CreateMaterialNetwork:
    TEXTURE_CONNECTOR = "Texture Connector"

    MATERIAL_NODE = None
    USE_BUMP_2D_NODE = True

    BASE_COLOR_MATERIAL_INPUT_NAME = None
    EMISSIVE_MATERIAL_INPUT_NAME = None
    METALNESS_MATERIAL_INPUT_NAME = None
    NORMAL_MATERIAL_INPUT_NAME = None
    OPACITY_MATERIAL_INPUT_NAME = None
    ROUGHNESS_MATERIAL_INPUT_NAME = None

    TRIPLANAR_INPUT_NAME = None
    TRIPLANAR_ALPHA_OUTPUT_NAME = None
    TRIPLANAR_COLOR_OUTPUT_NAME = None

    def __init__(self) -> None:
        self.name = ""
        self.uv_tiling_mode = ""
        self.use_triplanar = False

        self.float_constant_node = ""
        self.material = ""
        self.place_2d_texture_node = ""
        self.shading_engine_node = ""

        self.base_color_color_space = ""
        self.base_color_file_path = ""
        self.base_color_file_node = ""
        self.base_color_suffix = ""
        self.base_color_triplanar_node = ""

        self.roughness_color_space = ""
        self.roughness_file_path = ""
        self.roughness_file_node = ""
        self.roughness_suffix = ""
        self.roughness_triplanar_node = ""

        self.metalness_color_space = ""
        self.metalness_file_path = ""
        self.metalness_file_node = ""
        self.metalness_suffix = ""
        self.metalness_triplanar_node = ""

        self.normal_color_space = ""
        self.normal_file_path = ""
        self.normal_file_node = ""
        self.normal_suffix = ""
        self.normal_triplanar_node = ""

        self.height_color_space = ""
        self.height_file_path = ""
        self.height_displacement_shader_node = ""
        self.height_file_node = ""
        self.height_suffix = ""
        self.height_triplanar_node = ""

        self.emissive_color_space = ""
        self.emissive_file_path = ""
        self.emissive_file_node = ""
        self.emissive_suffix = ""
        self.emissive_triplanar_node = ""

        self.opacity_color_space = ""
        self.opacity_file_path = ""
        self.opacity_file_node = ""
        self.opacity_suffix = ""
        self.opacity_triplanar_node = ""

    def create(self, name: str, use_triplanar: bool, uv_tiling_mode: str) -> None:
        self.name = name
        self.use_triplanar = use_triplanar
        self.uv_tiling_mode = uv_tiling_mode

        if not self.name:
            MGlobal.displayError(
                f"[{CreateMaterialNetwork.TEXTURE_CONNECTOR}] No name for the material."
            )
            return

        cmds.undoInfo(chunkName="CreateMaterialNetwork", openChunk=True)

        self._load_plugins()
        self._create_material()

        if self.base_color_file_path:
            self._create_base_color_network()

        if self.roughness_file_path:
            self._create_roughness_network()

        if self.metalness_file_path:
            self._create_metalness_network()

        if self.normal_file_path:
            self._create_normal_network()

        if self.height_file_path:
            self._create_height_network()

        if self.emissive_file_path:
            self._create_emissive_network()

        if self.opacity_file_path:
            self._create_opacity_network()

        cmds.select(clear=True)

        MGlobal.displayInfo(
            f"[{CreateMaterialNetwork.TEXTURE_CONNECTOR}] Created {self.name!r} "
            f"material network."
        )

        cmds.undoInfo(chunkName="CreateMaterialNetwork", closeChunk=True)

    def set_base_color_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.base_color_color_space = color_space
        self.base_color_file_path = file_path
        self.base_color_suffix = suffix

    def set_emissive_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.emissive_color_space = color_space
        self.emissive_file_path = file_path
        self.emissive_suffix = suffix

    def set_height_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.height_color_space = color_space
        self.height_file_path = file_path
        self.height_suffix = suffix

    def set_metalness_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.metalness_color_space = color_space
        self.metalness_file_path = file_path
        self.metalness_suffix = suffix

    def set_normal_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.normal_color_space = color_space
        self.normal_file_path = file_path
        self.normal_suffix = suffix

    def set_opacity_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.opacity_color_space = color_space
        self.opacity_file_path = file_path
        self.opacity_suffix = suffix

    def set_roughness_settings(
        self, color_space: str, file_path: str, suffix: str
    ) -> None:
        self.roughness_color_space = color_space
        self.roughness_file_path = file_path
        self.roughness_suffix = suffix

    def _create_base_color_network(self) -> None:
        self.base_color_file_node, self.base_color_triplanar_node = (
            self._create_standard_network(
                material_input_name=self.BASE_COLOR_MATERIAL_INPUT_NAME,
                out_alpha=False,
                suffix=self.base_color_suffix,
            )
        )

        self._set_texture_file_node_settings(
            color_space=self.base_color_color_space,
            file_path=self.base_color_file_path,
            node=self.base_color_file_node,
        )

    def _create_bump_2d_node(self) -> str:
        bump_2d_node = cmds.shadingNode(
            "bump2d", asUtility=True, name=f"{self.name}_bump2d"
        )
        cmds.setAttr(f"{bump_2d_node}.bumpInterp", 1)

        return bump_2d_node

    def _create_emissive_network(self) -> None:
        self.emissive_file_node, self.emissive_triplanar_node = (
            self._create_standard_network(
                material_input_name=self.EMISSIVE_MATERIAL_INPUT_NAME,
                out_alpha=False,
                suffix=self.emissive_suffix,
            )
        )

        self._set_texture_file_node_settings(
            color_space=self.emissive_color_space,
            file_path=self.emissive_file_path,
            node=self.emissive_file_node,
        )

    def _create_file_node_network(self, name: str) -> str:
        if not cmds.objExists(self.place_2d_texture_node):
            self._create_place_2d_texture_node()

        file_node = cmds.shadingNode(
            "file", asTexture=True, isColorManaged=True, name=f"{name}_file"
        )

        attributes = (
            ".coverage",
            ".translateFrame",
            ".rotateFrame",
            ".mirrorU",
            ".mirrorV",
            ".stagger",
            ".wrapU",
            ".wrapV",
            ".repeatUV",
            ".offset",
            ".rotateUV",
            ".noiseUV",
            ".vertexUvOne",
            ".vertexUvTwo",
            ".vertexUvThree",
            ".vertexCameraOne",
        )

        for attr in attributes:
            cmds.connectAttr(
                f"{self.place_2d_texture_node}{attr}", f"{file_node}{attr}", force=True
            )

        cmds.connectAttr(
            f"{self.place_2d_texture_node}.outUvFilterSize", f"{file_node}.uvFilterSize"
        )
        cmds.connectAttr(f"{self.place_2d_texture_node}.outUV", f"{file_node}.uv")

        return file_node

    def _create_float_constant_node(self) -> None:
        self.float_constant_node = cmds.shadingNode(
            "floatConstant", asUtility=True, name=f"{self.name}_floatConstant"
        )

    def _create_height_network(self) -> None:
        name = f"{self.name}_{self.height_suffix}"

        self.height_displacement_shader_node = cmds.shadingNode(
            "displacementShader", asShader=True, name=f"{name}_displacementShader"
        )

        self.height_file_node = self._create_file_node_network(name=name)

        if self.use_triplanar:
            self.height_triplanar_node = self._create_triplanar_node_network(name)

            cmds.connectAttr(
                f"{self.height_file_node}.outColor",
                f"{self.height_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}",
                force=True,
            )
            cmds.connectAttr(
                f"{self.height_triplanar_node}.{self.TRIPLANAR_ALPHA_OUTPUT_NAME}",
                f"{self.height_displacement_shader_node}.displacement",
                force=True,
            )
        else:
            cmds.connectAttr(
                f"{self.height_file_node}.outAlpha",
                f"{self.height_displacement_shader_node}.displacement",
                force=True,
            )

        cmds.connectAttr(
            f"{self.height_displacement_shader_node}.displacement",
            f"{self.shading_engine_node}.displacementShader",
            force=True,
        )

        self._set_texture_file_node_settings(
            color_space=self.height_color_space,
            file_path=self.height_file_path,
            node=self.height_file_node,
        )

        cmds.setAttr(f"{self.height_file_node}.alphaIsLuminance", True)

    def _create_material(self) -> None:
        self.material = cmds.shadingNode(
            self.MATERIAL_NODE, asShader=True, name=f"{self.name}_{self.MATERIAL_NODE}"
        )

        self.shading_engine_node = cmds.sets(
            renderable=True, noSurfaceShader=True, empty=True, name=f"{self.name}SG"
        )

        cmds.connectAttr(
            f"{self.material}.outColor",
            f"{self.shading_engine_node}.surfaceShader",
            force=True,
        )

    def _create_metalness_network(self) -> None:
        self.metalness_file_node, self.metalness_triplanar_node = (
            self._create_standard_network(
                material_input_name=self.METALNESS_MATERIAL_INPUT_NAME,
                out_alpha=True,
                suffix=self.metalness_suffix,
            )
        )

        self._set_texture_file_node_settings(
            color_space=self.metalness_color_space,
            file_path=self.metalness_file_path,
            node=self.metalness_file_node,
        )

        cmds.setAttr(f"{self.metalness_file_node}.alphaIsLuminance", True)

    def _create_normal_network(self) -> None:
        name = f"{self.name}_{self.normal_suffix}"
        bump_2d_node = ""

        self.normal_file_node = self._create_file_node_network(name=name)

        if self.USE_BUMP_2D_NODE:
            bump_2d_node = self._create_bump_2d_node()

            cmds.connectAttr(
                f"{self.normal_file_node}.outColorR",
                f"{bump_2d_node}.bumpValue",
                force=True,
            )

        if self.use_triplanar:
            self.normal_triplanar_node = self._create_triplanar_node_network(name=name)

            if self.USE_BUMP_2D_NODE:
                cmds.connectAttr(
                    f"{bump_2d_node}.outNormal",
                    f"{self.normal_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}",
                    force=True,
                )
            else:
                cmds.connectAttr(
                    f"{self.normal_file_node}.outColor",
                    f"{self.normal_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}",
                    force=True,
                )

            cmds.connectAttr(
                f"{self.normal_triplanar_node}.outColor",
                f"{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}",
                force=True,
            )
        else:
            if self.USE_BUMP_2D_NODE:
                cmds.connectAttr(
                    f"{bump_2d_node}.outNormal",
                    f"{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}",
                    force=True,
                )
            else:
                cmds.connectAttr(
                    f"{self.normal_file_node}.outColor",
                    f"{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}",
                    force=True,
                )

        self._set_texture_file_node_settings(
            color_space=self.normal_color_space,
            file_path=self.normal_file_path,
            node=self.normal_file_node,
        )

        cmds.setAttr(f"{self.normal_file_node}.alphaIsLuminance", True)

    def _create_place_2d_texture_node(self) -> None:
        self.place_2d_texture_node = cmds.shadingNode(
            "place2dTexture", asUtility=True, name=f"{self.name}_place2dTexture"
        )

    def _create_opacity_network(self) -> None:
        self.opacity_file_node, self.opacity_triplanar_node = (
            self._create_standard_network(
                material_input_name=self.OPACITY_MATERIAL_INPUT_NAME,
                out_alpha=False,
                suffix=self.opacity_suffix,
            )
        )

        self._set_texture_file_node_settings(
            color_space=self.opacity_color_space,
            file_path=self.opacity_file_path,
            node=self.opacity_file_node,
        )

        cmds.setAttr(f"{self.opacity_file_node}.alphaIsLuminance", True)

    def _create_roughness_network(self) -> None:
        self.roughness_file_node, self.roughness_triplanar_node = (
            self._create_standard_network(
                material_input_name=self.ROUGHNESS_MATERIAL_INPUT_NAME,
                out_alpha=True,
                suffix=self.roughness_suffix,
            )
        )

        self._set_texture_file_node_settings(
            color_space=self.roughness_color_space,
            file_path=self.roughness_file_path,
            node=self.roughness_file_node,
        )

        cmds.setAttr(f"{self.roughness_file_node}.alphaIsLuminance", True)

    def _create_standard_network(
        self, material_input_name: str, out_alpha: bool, suffix: str
    ) -> tuple[str, str]:
        name = f"{self.name}_{suffix}"

        file_node = self._create_file_node_network(name=name)
        triplanar_node = ""

        if self.use_triplanar:
            triplanar_node = self._create_triplanar_node_network(name=name)
            if out_alpha:
                out = self.TRIPLANAR_ALPHA_OUTPUT_NAME
            else:
                out = self.TRIPLANAR_COLOR_OUTPUT_NAME

            cmds.connectAttr(
                f"{file_node}.outColor",
                f"{triplanar_node}.{self.TRIPLANAR_INPUT_NAME}",
                force=True,
            )

            cmds.connectAttr(
                f"{triplanar_node}.{out}",
                f"{self.material}.{material_input_name}",
                force=True,
            )
        else:
            out = "outAlpha" if out_alpha else "outColor"

            cmds.connectAttr(
                f"{file_node}.{out}",
                f"{self.material}.{material_input_name}",
                force=True,
            )

        return file_node, triplanar_node

    def _create_triplanar_node_network(self, name: str) -> any:
        if not cmds.objExists(self.float_constant_node):
            self._create_float_constant_node()

    def _load_plugins(self) -> None:
        plugins_loaded = cmds.pluginInfo(listPlugins=True, query=True)
        look_dev_kit_plugin = "lookdevKit"

        if look_dev_kit_plugin not in plugins_loaded and self.use_triplanar:
            cmds.loadPlugin(f"{look_dev_kit_plugin}.py")

    def _set_texture_file_node_settings(
        self, color_space: str, file_path: str, node: str
    ) -> None:
        cmds.setAttr(f"{node}.ignoreColorSpaceFileRules", True)
        cmds.setAttr(f"{node}.fileTextureName", file_path, type="string")
        cmds.setAttr(f"{node}.colorSpace", color_space, type="string")

        if UVTilingModes.OFF == self.uv_tiling_mode:
            cmds.setAttr(f"{node}.uvTilingMode", 0)
        elif UVTilingModes.ZBRUSH == self.uv_tiling_mode:
            cmds.setAttr(f"{node}.uvTilingMode", 1)
        elif UVTilingModes.MUDBOX == self.uv_tiling_mode:
            cmds.setAttr(f"{node}.uvTilingMode", 2)
        elif UVTilingModes.MARI == self.uv_tiling_mode:
            cmds.setAttr(f"{node}.uvTilingMode", 3)
