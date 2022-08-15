#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import open3d as o3d
from tqdm import tqdm

from Data.channel_mesh import ChannelMesh

class MeshLoader(object):
    def __init__(self):
        self.channel_mesh = ChannelMesh()
        return

    def reset(self):
        self.channel_mesh.reset()
        return True

    def loadOBJ(self, obj_file_path):
        if not os.path.exists(obj_file_path):
            print("[ERROR][ChannelMesh::loadOBJFile]")
            print("\t obj_file not exist!")
            return False

        o3d_mesh = o3d.io.read_triangle_mesh(obj_file_path)
        points = np.asarray(o3d_mesh.vertices)
        colors = np.asarray(o3d_mesh.vertex_colors)
        for point, color in tqdm(zip(points, colors), total=len(points)):
            color *= 255
            channel_value_list = [point[0], point[1], point[2], round(color[0]), round(color[1]), round(color[2])]
            self.channel_mesh.addChannelPoint(["x", "y", "z", "r", "g", "b"], channel_value_list)

        #  faces = np.asarray(o3d_mesh.faces)
        #  print(faces)
        return True

def demo():
    obj_file_path = "/home/chli/chLi/OBJs/OpenGL/bunny_1.obj"

    mesh_loader = MeshLoader()
    mesh_loader.loadOBJ(obj_file_path)
    return True

