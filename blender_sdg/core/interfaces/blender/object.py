"""Interface for Blender objects."""

import bpy
from blender_sdg.types.model import Element
from typing import Tuple


class BlenderElement(Element):
    """Base Interface for Blender objects."""

    def __init__(self, bpy_object: bpy.types.Object):
        """
        Initialize the interface with a Blender object,
        while storing the object's data.

        Parameters:
        ___________
        bpy_object: bpy.types.Object
            The Blender object to interface with.
        """
        self.object = bpy_object
        self.name = bpy_object.name
        self.location = bpy_object.location
        self.rotation = bpy_object.rotation_euler

    def set_location(self):
        """Set the location of the object"""
        raise NotImplementedError

    def set_rotation(self):
        """Set the rotation of the object"""
        raise NotImplementedError

    def get_inverse_matrix(self):
        """Get the inverse matrix of the object"""
        return self.object.matrix_world.inverted()

    def get_mesh(self, preserve_all_data_layers: bool = True):
        """Get the mesh of the model"""
        return self.object.to_mesh(preserve_all_data_layers=preserve_all_data_layers)

    @classmethod
    def from_bpy_object(cls, blender_object: bpy.types.Object):
        return cls(blender_object)


class BlenderAxis(BlenderElement):
    """Interface for Blender axes."""

    def set_location(self, location: Tuple[float, float, float]):
        """Set the location of the axis"""
        self.object.location = location

    def set_rotation(self, rotation: Tuple[float, float, float]):
        """Set the rotation of the axis"""
        self.object.rotation_euler = rotation

    def set_scale(self, scale: float):
        """Set the scale of the axis"""
        self.object.scale = (scale, scale, scale)


class BlenderLight(BlenderElement):
    """Interface for Blender lights."""

    def set_energy(self, energy: float):
        """Set the energy of the light"""
        self.object.data.energy = energy
