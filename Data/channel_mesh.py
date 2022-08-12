#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import open3d as o3d

from Data.channel_pointcloud import ChannelPointCloud
from Data.edge_set import EdgeSet
from Data.face_set import FaceSet

class ChannelMesh(object):
    def __init__(self):
        self.channel_pointcloud = ChannelPointCloud()
        self.edge_set = EdgeSet()
        self.face_set = FaceSet()
        return

    def reset(self):
        self.channel_pointcloud.reset()
        self.edge_set.reset()
        self.face_set.reset()
        return True

    def loadOBJFile(self, obj_file_path):
        if not os.path.exists(obj_file_path):
            print("[ERROR][ChannelMesh::loadOBJFile]")
            print("\t obj_file not exist!")
            return False

        o3d_mesh = o3d.io.read_triangle_mesh(obj_file_path)
        points = o3d_mesh.vertices().numpy()
        print(points.shape)

        return True

