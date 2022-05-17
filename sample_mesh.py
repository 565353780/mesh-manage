#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

mesh_file_basename = "f14"

mesh_file_path = "/home/chli/masked_pcd/" + mesh_file_basename + "/" + mesh_file_basename + ".ply"

print("start read file...")
mesh = o3d.io.read_triangle_mesh(mesh_file_path)
print("finish read file")

sample_mesh = mesh.simplify_vertex_clustering(0.01)
print("finish sample")

o3d.io.write_triangle_mesh("/home/chli/masked_pcd/" + mesh_file_basename + "/" + mesh_file_basename + "_sample_0.01_mesh.ply",
                           sample_mesh,
                           write_ascii=True)
print("finish save")

