"""Interface for Blender objects."""

import bpy
from blender_sdg.core.model import Element
from typing import Tuple

import math


class BlenderElement(Element):
    """Base Interface for Blender objects."""

    object: bpy.types.Object

    def __init__(self, bpy_object: bpy.types.Object):
        """
        Initialize the interface with a Blender object,
        while storing the object's data.

        Parameters:
        ___________
        bpy_object: bpy.types.Object
            The Blender object to interface with.
        """
        super().__init__(
            name=bpy_object.name,
            location=(
                bpy_object.location.x,
                bpy_object.location.y,
                bpy_object.location.z,
            ),
            rotation=(
                bpy_object.rotation_euler.x,
                bpy_object.rotation_euler.y,
                bpy_object.rotation_euler.z,
            ),
            scale=(bpy_object.scale.x, bpy_object.scale.y, bpy_object.scale.z),
            object=bpy_object,
        )

    def set_location(self, location: Tuple[float, float, float]):
        """Set the location of the axis"""
        self.object.location = location

    def set_rotation(
        self, rotation: Tuple[float, float, float], convert_to_radians: bool = True
    ):
        """Set the rotation of the axis"""
        if convert_to_radians:
            rotation = tuple(math.radians(angle) for angle in rotation)
        self.object.rotation_euler = rotation

    def set_scale(self):
        """Set the scale of the axis"""
        raise NotImplementedError("Setting the scale of an element is not supported")

    def get_matrix(self, inverse: bool = False, normalized: bool = False):
        """Get the inverse matrix of the object"""
        matrix = (
            self.object.matrix_world.inverted() if inverse else self.object.matrix_world
        )
        return matrix.normalized() if normalized else matrix

    def get_mesh(self, preserve_all_data_layers: bool = True):
        """Get the mesh of the model"""
        return self.object.to_mesh(preserve_all_data_layers=preserve_all_data_layers)

    @classmethod
    def from_bpy_object(cls, blender_object: bpy.types.Object):
        return cls(blender_object)


class BlenderLight(BlenderElement):
    """Interface for Blender lights."""

    def set_energy(self, energy: float):
        """Set the energy of the light"""
        self.object.data.energy = energy
