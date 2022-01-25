#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

from Render import PointCloudRender

class Renderer(object):
    def __init__(self):

        self.d3_40_colors_rgb = np.array(
            [
                [164, 218, 252], [120, 173, 219], [253, 147, 81], [252, 234, 163], [0, 128, 128],
                [132, 220, 198], [255, 104, 107], [255, 166, 158], [148, 103, 189], [189, 147, 189],
                [140, 86, 75], [146, 94, 120], [227, 119, 194], [247, 182, 210], [127, 127, 127],
                [199, 199, 199], [188, 189, 34], [219, 219, 141], [23, 190, 207], [158, 218, 229],
                [57, 59, 121], [82, 84, 163], [107, 110, 207], [156, 158, 222], [99, 121, 57],
                [140, 162, 82], [181, 207, 107], [206, 219, 156], [140, 109, 49], [189, 158, 57],
                [231, 186, 82], [231, 203, 148], [132, 60, 57], [173, 73, 74], [214, 97, 107],
                [231, 150, 156], [123, 65, 115], [165, 81, 148], [206, 109, 189], [222, 158, 214]
            ],
            dtype=np.uint8,
        )

        gui.Application.instance.initialize()

        self.window = gui.Application.instance.create_window('Open3D Renderer', 800, 600)

        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(self.window.renderer)

        self.window.add_child(self.scene)

        #  bounds = o3d.geometry.AxisAlignedBoundingBox()
        #  bounds.create_from_points()
        #  self.scene.setup_camera(60, bounds, bounds.get_center())
        return

    def addPointCloud(self, name, pointcloud, material_name):
        material = rendering.Material()
        material.shader = material_name

        self.scene.scene.add_geometry(name, pointcloud, material)
        return True

    def run(self):
        gui.Application.instance.run()

if __name__ == "__main__":
    pointcloud_file_path = "./masked_pc/home/home_DownSample_8_masked_merged.pcd"
    label_channel_idx = 7

    #  labels = [
        #  "ZERO", "table", "chair", "sofa", "lamp",
        #  "bed", "cabinet", "lantern", "light", "wall",
        #  "painting", "refrigerator"]
    #  show_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]

    labels = [
        "BG",
        "person", "bicycle", "car", "motorcycle", "airplane",
        "bus", "train", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "bird",
        "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee",
        "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
        "wine glass", "cup", "fork", "knife", "spoon",
        "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut",
        "cake", "chair", "couch", "potted plant", "bed",
        "dining table", "toilet", "tv", "laptop", "mouse",
        "remote", "keyboard", "cell phone", "microwave", "oven",
        "toaster", "sink", "refrigerator", "book", "clock",
        "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
    ]
    show_labels = [
        #  0,
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25,
        26, 27, 28, 29, 30,
        31, 32, 33, 34, 35,
        36, 37, 38, 39, 40,
        41, 42, 43, 44, 45,
        46, 47, 48, 49, 50,
        51, 52, 53, 54, 55,
        56, 57, 58, 59, 60,
        61, 62, 63, 64, 65,
        66, 67, 68, 69, 70,
        71, 72, 73, 74, 75,
        76, 77, 78, 79, 80
    ]

    pointcloud_render = PointCloudRender()
    pointcloud_render.loadPointCloud(pointcloud_file_path,
                                     label_channel_idx,
                                     labels)
    pointcloud = pointcloud_render.getRenderedPointCloud(show_labels)

    renderer = Renderer()
    renderer.addPointCloud("test", pointcloud, "depth")
    renderer.run()

