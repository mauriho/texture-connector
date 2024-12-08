"""
========================================================================================================================
Name: create_material_network_arnold.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-08-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maya.cmds as cmds

from texture_connector.core.create_material_network import CreateMaterialNetwork


class CreateMaterialNetworkArnold(CreateMaterialNetwork):
    MATERIAL_NODE = 'aiStandardSurface'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'baseColor'
    EMISSIVE_MATERIAL_INPUT_NAME = 'emissionColor'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'normalCamera'
    OPACITY_MATERIAL_INPUT_NAME = 'opacity'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'specularRoughness'

    TRIPLANAR_INPUT_NAME = 'input'
    TRIPLANAR_ALPHA_OUTPUT_NAME = 'outColorR'
    TRIPLANAR_COLOR_OUTPUT_NAME = 'outColor'

    def __init__(self) -> None:
        super().__init__()

    def _create_emissive_network(self) -> None:
        super()._create_emissive_network()

        cmds.setAttr(f'{self.material}.emission', 1)

    def _create_triplanar_node_network(self, name: str) -> str:
        super()._create_triplanar_node_network(name)

        triplanar_node = cmds.shadingNode('aiTriplanar', asTexture=True, name=f'{name}_aiTriplanar')

        cmds.setAttr(f'{triplanar_node}.coordSpace', 0)

        for axis in ('X', 'Y', 'Z'):
            cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.scale{axis}', force=True)

        return triplanar_node
