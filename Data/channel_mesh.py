#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from Data.channel_pointcloud import ChannelPointCloud
from Data.face_set import FaceSet

from Method.io import loadFileData, saveChannelMesh

class ChannelMesh(object):
    def __init__(self, mesh_file_path=None, channel_pointcloud=ChannelPointCloud(), face_set=FaceSet()):
        self.channel_pointcloud = channel_pointcloud
        self.face_set = face_set

        if mesh_file_path is not None:
            self.loadData(mesh_file_path)
        return

    def reset(self):
        self.channel_pointcloud.reset()
        self.face_set.reset()
        return True

    def loadData(self, mesh_file_path):
        self.reset()

        print("[INFO][ChannelMesh::loadData]")
        print("\t start load mesh :")
        print("\t mesh_file_path =", mesh_file_path)

        channel_name_list, channel_value_list_list, point_idx_list_list = loadFileData(mesh_file_path)
        if channel_name_list == [] or channel_value_list_list == []:
            print("[ERROR][ChannelMesh::loadData]")
            print("\t loadFileData failed!")
            return False

        for channel_value_list in tqdm(channel_value_list_list):
            self.addChannelPoint(channel_name_list, channel_value_list)

        self.updateKDTree()

        if point_idx_list_list != []:
            for point_idx_list in point_idx_list_list:
                self.addFace(point_idx_list)
        return True

    def addChannelPoint(self, channel_name_list, channel_value_list):
        return self.channel_pointcloud.addChannelPoint(channel_name_list, channel_value_list)

    def updateKDTree(self):
        return self.channel_pointcloud.updateKDTree()

    def getChannelPoint(self, channel_point_idx):
        return self.channel_pointcloud.getChannelPoint(channel_point_idx)

    def addFace(self, point_idx_list):
        return self.face_set.addFace(point_idx_list)

    def getFace(self, face_idx):
        return self.face_set.getFace(face_idx)

    def getFaceIdxListInPointIdxList(self, point_idx_list):
        return self.face_set.getFaceIdxListInPointIdxList(point_idx_list)

    def getPointIdxListFromFaceIdxList(self, face_idx_list):
        return self.face_set.getPointIdxListAndMappingDict(face_idx_list)[0]

    def getChannelMeshByFace(self, face_idx_list):
        point_idx_list, mapping_dict = self.face_set.getPointIdxListAndMappingDict(face_idx_list)
        if point_idx_list is None or mapping_dict is None:
            print("[ERROR][ChannelMesh::getChannelMeshByFace]")
            print("\t getPointIdxListAndMappingDict failed!")
            return None

        channel_pointcloud = self.channel_pointcloud.getFilterChannelPointCloud(point_idx_list)
        if channel_pointcloud is None:
            print("[ERROR][ChannelMesh::getChannelMeshByFace]")
            print("\t getFilterChannelPointCloud failed!")
            return None

        face_set = self.face_set.getMappingFaceSet(face_idx_list, mapping_dict)
        if face_set is None:
            print("[ERROR][ChannelMesh::getChannelMeshByFace]")
            print("\t getMappingFaceSet failed!")
            return None

        channel_mesh = ChannelMesh(None, channel_pointcloud, face_set)
        return channel_mesh

    def getChannelMeshByPoint(self, point_idx_list):
        channel_pointcloud = self.channel_pointcloud.getFilterChannelPointCloud(point_idx_list)
        if channel_pointcloud is None:
            print("[ERROR][ChannelMesh::getChannelMeshByPoint]")
            print("\t getFilterChannelPointCloud failed!")
            return None

        face_set = self.face_set.getFaceSetInPointIdxList(point_idx_list)
        if face_set is None:
            print("[ERROR][ChannelMesh::getChannelMeshByPoint]")
            print("\t getFaceSetInPointIdxList failed!")
            return None

        channel_mesh = ChannelMesh(None, channel_pointcloud, face_set)
        return channel_mesh

    def saveMesh(self, save_file_path, print_progress=False):
        if not saveChannelMesh(self, save_file_path, print_progress):
            print("[ERROR][ChannelMesh::saveMesh]")
            print("\t saveChannelMesh failed!")
            return False
        return True

    def generateMeshByFace(self, face_idx_list, save_file_path, print_progress=False):
        channel_mesh = self.getChannelMeshByFace(face_idx_list)
        if channel_mesh is None:
            print("[ERROR][ChannelMesh::generateMeshByFace]")
            print("\t getChannelMeshByFace failed!")
            return False
        if not channel_mesh.saveMesh(save_file_path, print_progress):
            print("[ERROR][ChannelMesh::generateMeshByFace]")
            print("\t saveMesh failed!")
            return False
        return True

    def generateMeshByPoint(self, point_idx_list, save_file_path, print_progress=False):
        channel_mesh = self.getChannelMeshByPoint(point_idx_list)
        if channel_mesh is None:
            print("[ERROR][ChannelMesh::generateMeshByPoint]")
            print("\t getChannelMeshByPoint failed!")
            return False
        if not channel_mesh.saveMesh(save_file_path, print_progress):
            print("[ERROR][ChannelMesh::generateMeshByPoint]")
            print("\t saveMesh failed!")
            return False
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[ChannelMesh]")
        print(line_start + "\t channel_pointcloud =")
        self.channel_pointcloud.outputInfo(info_level + 1)
        print(line_start + "\t face_set =")
        self.face_set.outputInfo(info_level + 1)
        return True

