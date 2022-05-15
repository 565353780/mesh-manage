#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

mesh_file_path = "/home/chli/chLi/coscan_data/compare_to_liu/matterport_05.ply"

mesh = o3d.io.read_triangle_mesh(mesh_file_path)
mesh.compute_vertex_normals()

# TODO: finish this algo

#  o3d.visualization.draw_geometries([mesh])
o3d.io.write_triangle_mesh(
    "/home/chli/chLi/coscan_data/compare_to_liu/matterport_05_test.ply", mesh)

