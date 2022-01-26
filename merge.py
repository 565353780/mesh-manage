#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PointCloudClass.channel_pointcloud import ChannelPointCloud

def demo():
    source_pointcloud = ChannelPointCloud()
    source_pointcloud.loadData("./masked_pc/home/home_cut.ply",
                               ["x", "y", "z", "r", "g", "b"],
                               [0, 1, 2, 3, 4, 5])

    label_pointcloud = ChannelPointCloud()
    label_pointcloud.loadData("./masked_pc/home/home_DownSample_8_masked.pcd",
                              ["x", "y", "z", "instance_label"],
                              [0, 1, 2, 4])

    merge_pointcloud = ChannelPointCloud()
    merge_pointcloud.copyChannelValue(source_pointcloud, ["x", "y", "z", "r", "g", "b"])
    merge_pointcloud.setChannelValueByKDTree(label_pointcloud, ["label"])

    merge_pointcloud.savePointCloud("./test.pcd")
    return True

if __name__ == "__main__":
    demo()

