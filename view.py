#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.render import render

# Param
pointcloud_file_path = "./masked_pc/office/office_cut_painted.ply"
estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

# Process
render(pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

