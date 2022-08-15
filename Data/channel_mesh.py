#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_pointcloud import ChannelPointCloud
from Data.face_set import FaceSet

class ChannelMesh(object):
    def __init__(self, channel_pointcloud=ChannelPointCloud(), face_set=FaceSet()):
        self.channel_pointcloud = channel_pointcloud
        self.face_set = face_set
        return

    def reset(self):
        self.channel_pointcloud.reset()
        self.face_set.reset()
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

        channel_mesh = ChannelMesh(channel_pointcloud, face_set)
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

        channel_mesh = ChannelMesh(channel_pointcloud, face_set)
        return channel_mesh

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[ChannelMesh]")
        print(line_start + "\t channel_pointcloud =")
        self.channel_pointcloud.outputInfo(info_level + 1)
        print(line_start + "\t face_set =")
        self.face_set.outputInfo(info_level + 1)
        return True

