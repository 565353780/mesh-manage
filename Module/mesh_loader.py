#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from Data.channel_mesh import ChannelMesh

from Method.io import loadFileData

class MeshLoader(object):
    def __init__(self, mesh_file_path=None):
        self.channel_mesh = ChannelMesh()

        if mesh_file_path is not None:
            self.loadData(mesh_file_path)
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

    def generateMeshByFace(self, face_idx_list, save_file_path):
        channel_mesh = self.channel_mesh.getChannelMeshByFace(face_idx_list)
        if channel_mesh is None:
            print("[ERROR][MeshLoader::generateMeshByFace]")
            print("\t getChannelMeshByFace failed!")
            return False
        if not channel_mesh.saveMesh(save_file_path):
            print("[ERROR][MeshLoader::generateMeshByFace]")
            print("\t saveMesh failed!")
            return False
        return True

    def generateMeshByPoint(self, point_idx_list, save_file_path):
        channel_mesh = self.channel_mesh.getChannelMeshByPoint(point_idx_list)
        if channel_mesh is None:
            print("[ERROR][MeshLoader::generateMeshByPoint]")
            print("\t getChannelMeshByPoint failed!")
            return False
        if not channel_mesh.saveMesh(save_file_path):
            print("[ERROR][MeshLoader::generateMeshByPoint]")
            print("\t saveMesh failed!")
            return False
        return True

def demo():
    mesh_file_path = "/home/chli/scan2cad/scannet/scans/scene0474_02/scene0474_02_vh_clean_2.ply"

    mesh_loader = MeshLoader(mesh_file_path)

    face_idx_list = [i for i in range(20)]

    point_idx_list = mesh_loader.channel_mesh.getPointIdxListFromFaceIdxList(face_idx_list)

    mesh_loader.generateMeshByFace(face_idx_list, "/home/chli/chLi/channel_mesh/test1.ply")
    mesh_loader.generateMeshByPoint(point_idx_list, "/home/chli/chLi/channel_mesh/test2.ply")
    return True

