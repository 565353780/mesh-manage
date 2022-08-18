#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.pointcloud_painter import demo_merge, demo_paint, demo_auto_paint
from Module.sampler import demo_sample_pointcloud, demo_sample_mesh
from Module.channel_pointcloud import demo as pointcloud_demo
from Module.channel_mesh import demo as mesh_demo

if __name__ == "__main__":
    mesh_demo()

