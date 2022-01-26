#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PointCloudClass.renderer import render

pointcloud_file_path = "./masked_pc/f14/f14.ply"
estimate_normals_radius = 0.05
estimate_normals_max_nn = 30

render(pointcloud_file_path, estimate_normals_radius, estimate_normals_max_nn)

