#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from mesh_manage.Config.color import d3_40_colors_rgb

from mesh_manage.Module.channel_mesh import ChannelMesh

class Painter(object):
    def __init__(self):
        self.channel_mesh_dict = {}
        self.merge_channel_mesh = ChannelMesh()
        return

    def reset(self):
        self.channel_mesh_dict = {}
        self.merge_channel_mesh = ChannelMesh()
        return True

    def addChannelMesh(self, mesh_file_path, mesh_name):
        if not os.path.exists(mesh_file_path):
            print("[WARN][Painter::addChannelMesh]")
            print("\t mesh_file not exist!")
            return False

        if mesh_name in self.channel_mesh_dict.keys():
            print("[ERROR][Painter::addChannelMesh]")
            print("\t mesh_name already exist!")
            return False

        channel_mesh = ChannelMesh(mesh_file_path, [], True)
        self.channel_mesh_dict[mesh_name] = channel_mesh
        return True

    def loadMeshFilePathDict(self, mesh_file_path_dict):
        for mesh_name, mesh_file_path in mesh_file_path_dict:
            if not self.addChannelMesh(mesh_file_path, mesh_name):
                print("[ERROR][Painter::loadMeshFilePathDict]")
                print("\t addChannelMesh failed!")
                return False
        return True

    def mergeChannelMesh(self, merge_mesh_dict):
        self.merge_channel_mesh = ChannelMesh()

        if len(merge_mesh_dict.keys()) == 0:
            return True

        source_mesh_name = merge_mesh_dict["source_name"]
        if source_mesh_name not in self.channel_mesh_dict.keys():
            print("[ERROR][Painter::mergeChannelMesh]")
            print("\t source_mesh", source_mesh_name, "not found!")
            return False

        self.merge_channel_mesh.copyChannelValue(
            self.channel_mesh_dict[source_mesh_name],
            merge_mesh_dict["source_channel_list"])

        for merge_mesh_name, merge_channel_name_list in merge_mesh_dict["merge"]:
            if merge_mesh_name not in self.channel_mesh_dict.keys():
                print("[ERROR][Painter::mergeChannelMesh]")
                print("\t merge_mesh_name", merge_mesh_name, "not found!")
                return False
            self.merge_channel_mesh.setChannelValueByKDTree(
                self.channel_mesh_dict[merge_mesh_name],
                merge_channel_name_list)
        return True

    def removeOutlierPoints(self, outlier_dist_max):
        self.merge_channel_mesh.removeOutlierPoints(outlier_dist_max)
        return True

    def paintColor(self, paint_channel_name, color_list):
        self.merge_channel_mesh.paintByLabel(paint_channel_name, color_list)
        return True

    def savePaintedPointCloud(self, save_file_path, print_progress=False):
        if not self.merge_channel_mesh.savePointCloud(save_file_path, print_progress):
            print("[ERROR][Painter::savePaintedPointCloud]")
            print("\t savePointCloud failed!")
            return False
        return True

    def savePaintedMesh(self, save_file_path, print_progress=False):
        if not self.merge_channel_mesh.saveMesh(save_file_path, print_progress):
            print("[ERROR][Painter::savePaintedMesh]")
            print("\t saveMesh failed!")
            return False
        return True

def demo_merge():
    mesh_file_path_dict = {
        "xyz": "./masked_pc/office/office_cut.ply",
        "label": "./masked_pc/office/office_DownSample_8_masked.pcd",
    }
    merge_mesh_dict = {
        "source_name": "xyz",
        "source_channel_list": ["x", "y", "z"],
        "merge": {
            "label": ["label"],
        }
    }
    outlier_dist_max = 0.05
    save_file_path = "./masked_pc/office/office_cut_merged.ply"

    painter = Painter()
    painter.loadMeshFilePathDict(mesh_file_path_dict)
    painter.mergeChannelMesh(merge_mesh_dict)
    painter.removeOutlierPoints(outlier_dist_max)
    painter.savePaintedPointCloud(save_file_path)
    return True

def demo_paint():
    mesh_file_path_dict = {
        "xyz": "./masked_pc/front_3d/04_masked.pcd",
    }
    paint_channel_name = "label"
    save_file_path = "./masked_pc/front_3d/04_masked_painted.ply"

    painter = Painter()
    painter.loadMeshFilePathDict(mesh_file_path_dict)
    painter.paintColor(paint_channel_name, d3_40_colors_rgb)
    painter.savePaintedPointCloud(save_file_path)
    return True

def demo_auto_paint():
    mesh_file_path_dict = {
        "xyz": "./masked_pc/office/office_cut.ply",
        "label": "./masked_pc/office/office_DownSample_8_masked.pcd",
    }
    merge_mesh_dict = {
        "source_name": "xyz",
        "source_channel_list": ["x", "y", "z"],
        "merge": {
            "label": ["label"],
        }
    }
    outlier_dist_max = 0.05
    paint_channel_name = "label"
    save_file_path = "./masked_pc/office/office_cut_painted.ply"

    painter = Painter()
    painter.loadMeshFilePathDict(mesh_file_path_dict)
    painter.mergeChannelMesh(merge_mesh_dict)
    painter.removeOutlierPoints(outlier_dist_max)
    painter.paintColor(paint_channel_name, d3_40_colors_rgb)
    painter.savePaintedPointCloud(save_file_path)
    return True

