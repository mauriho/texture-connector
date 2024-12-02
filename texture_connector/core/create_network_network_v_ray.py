"""
========================================================================================================================
Name: create_network_network_v_ray.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-01-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maya.cmds as cmds

from texture_connector.core.create_material_network import CreateMaterialNetwork


class CreateMaterialNetworkVRay(CreateMaterialNetwork):
    MATERIAL_NODE = 'VRayMtl'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'color'
    EMISSIVE_MATERIAL_INPUT_NAME = 'illumColor'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'bumpMap'
    OPACITY_MATERIAL_INPUT_NAME = 'opacityMap'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'reflectionGlossiness'

    TRIPLANAR_INPUT_NAME = 'textureX'
    TRIPLANAR_ALPHA_OUTPUT_NAME = 'outAlpha'
    TRIPLANAR_COLOR_OUTPUT_NAME = 'outColor'

    USE_BUMP_2D_NODE = False

    def __init__(self) -> None:
        super(CreateMaterialNetworkVRay, self).__init__()

    def _create_normal_network(self) -> None:
        super(CreateMaterialNetworkVRay, self)._create_normal_network()

        cmds.setAttr(f'{self.material}.bumpMapType', 1)

    def _create_roughness_network(self) -> None:
        super(CreateMaterialNetworkVRay, self)._create_roughness_network()

        cmds.setAttr(f'{self.material}.reflectionColor', 1, 1, 1, type='double3')
        cmds.setAttr(f'{self.material}.useRoughness', 1)

    def _create_triplanar_node_network(self, name: str) -> str:
        super(CreateMaterialNetworkVRay, self)._create_triplanar_node_network(name)

        triplanar_node = cmds.shadingNode('VRayTriplanar', asTexture=True, name=f'{name}_VRayTriplanar')

        cmds.setAttr(f'{triplanar_node}.refSpace', 1)

        cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.size', force=True)

        return triplanar_node
