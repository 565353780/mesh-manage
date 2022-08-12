#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_mesh import ChannelMesh

class MeshLoader(object):
    def __init__(self):
        self.channel_mesh = ChannelMesh()
        return

def demo():
    obj_file_path = "/home/chli/scan2cad/scannet/scans/scene0474_02/scene0474_02_vh_clean.ply"
    mesh_loader = MeshLoader()
    mesh_loader.channel_mesh.loadOBJFile(obj_file_path)
    return True

