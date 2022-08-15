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

    def generateMeshByFace(self, face_idx_list):
        point_idx_list = []
        mapping_dict = {}

        for face_idx in face_idx_list:
            face = self.channel_mesh.getFace(face_idx)
            if face is None:
                print("[ERROR][MeshLoader::generateSubMesh]")
                print("\t getFace failed!")
                return False

            for point_idx in face.point_idx_list:
                if point_idx in point_idx_list:
                    continue
                mapping_dict[str(point_idx)] = len(point_idx_list)
                point_idx_list.append(point_idx)

        channel_pointcloud = self.channel_mesh.getFilterChannelPointCloud(point_idx_list)
        face_set = self.channel_mesh.getMappingFaceSet(mapping_dict)

        channel_mesh = ChannelMesh(channel_pointcloud, face_set)
        channel_mesh.outputInfo(1)
        return True

    def generateMeshByPoint(self, point_idx_list):
        return True

def demo():
    mesh_file_path = "/home/chli/scan2cad/scannet/scans/scene0474_02/scene0474_02_vh_clean_2.ply"

    mesh_loader = MeshLoader()
    mesh_loader.loadData(mesh_file_path)

    face_idx_list = [i for i in range(20)]
    mesh_loader.generateMeshByFace(face_idx_list)
    return True

