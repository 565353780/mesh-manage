#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Data.channel_mesh import ChannelMesh

def demo():
    mesh_file_path = "/home/chli/chLi/ScanNet/scans/scene0474_02/scene0474_02_vh_clean_2.ply"

    channel_mesh = ChannelMesh(mesh_file_path)

    face_idx_list = [i for i in range(20)]

    point_idx_list = channel_mesh.getPointIdxListFromFaceIdxList(face_idx_list)

    channel_mesh.generateMeshByFace(face_idx_list, "/home/chli/chLi/channel_mesh/test1.ply")
    channel_mesh.generateMeshByPoint(point_idx_list, "/home/chli/chLi/channel_mesh/test2.ply")
    return True

