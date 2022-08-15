#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from Data.channel_mesh import ChannelMesh

from Method.io import loadFileData

class MeshLoader(object):
    def __init__(self):
        self.channel_mesh = ChannelMesh()
        return

    def reset(self):
        self.channel_mesh.reset()
        return True

    def loadData(self, mesh_file_path):
        self.reset()

        print("[INFO][MeshLoader::loadData]")
        print("\t start load mesh :")
        print("\t mesh_file_path =", mesh_file_path)

        channel_name_list, channel_value_list_list, point_idx_list_list = loadFileData(mesh_file_path)
        if channel_name_list == [] or channel_value_list_list == []:
            print("[ERROR][MeshLoader::loadData]")
            print("\t loadFileData failed!")
            return False

        for channel_value_list in tqdm(channel_value_list_list):
            self.channel_mesh.addChannelPoint(channel_name_list, channel_value_list)

        self.channel_mesh.updateKDTree()

        if point_idx_list_list != []:
            for point_idx_list in point_idx_list_list:
                self.channel_mesh.addFace(point_idx_list)
        return True

def demo():
    obj_file_path = "/home/chli/chLi/OBJs/OpenGL/bunny_1.obj"

    mesh_loader = MeshLoader()
    mesh_loader.loadData(obj_file_path)
    return True

