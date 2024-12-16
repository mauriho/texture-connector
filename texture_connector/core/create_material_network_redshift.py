"""
========================================================================================
Name: create_material_network_redshift.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

import maya.cmds as cmds

from texture_connector.core.create_material_network import CreateMaterialNetwork


class CreateMaterialNetworkRedshift(CreateMaterialNetwork):
    MATERIAL_NODE = "RedshiftStandardMaterial"

    BASE_COLOR_MATERIAL_INPUT_NAME = "base_color"
    EMISSIVE_MATERIAL_INPUT_NAME = "emission_color"
    METALNESS_MATERIAL_INPUT_NAME = "metalness"
    NORMAL_MATERIAL_INPUT_NAME = "bump_input"
    OPACITY_MATERIAL_INPUT_NAME = "opacity_color"
    ROUGHNESS_MATERIAL_INPUT_NAME = "refl_roughness"

    TRIPLANAR_INPUT_NAME = "imageX"
    TRIPLANAR_ALPHA_OUTPUT_NAME = "outAlpha"
    TRIPLANAR_COLOR_OUTPUT_NAME = "outColor"

    def __init__(self) -> None:
        super().__init__()

    def _create_emissive_network(self) -> None:
        super()._create_emissive_network()

        cmds.setAttr(f"{self.material}.emission_weight", 1)

    def _create_triplanar_node_network(self, name: str) -> str:
        super()._create_triplanar_node_network(name)

        triplanar_node = cmds.shadingNode(
            "RedshiftTriPlanar", asTexture=True, name=f"{name}_RedshiftTriPlanar"
        )

        cmds.setAttr(f"{triplanar_node}.projSpaceType", 0)

        for i in range(3):
            cmds.connectAttr(
                f"{self.float_constant_node}.outFloat",
                f"{triplanar_node}.scale.scale{i}",
                force=True,
            )

        return triplanar_node
