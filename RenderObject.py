#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from multiprocessing import Process
from tqdm import tqdm
import open3d as o3d

from time import time

class ObjectPointCloudRender:
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

        self.pointcloud_file_path_list = None
        self.label_channel_idx = None
        self.labels = None

        self.pointcloud_list = None
        self.labeled_point_cluster_list = None
        return

    def loadPointCloud(self,
                       pointcloud_file_path_list,
                       label_channel_idx,
                       labels):
        self.pointcloud_file_path_list = pointcloud_file_path_list
        self.label_channel_idx = label_channel_idx
        self.labels = labels

        self.pointcloud_list = []
        for pointcloud_file_path in self.pointcloud_file_path_list:
            print("start reading pointcloud :")
            print(pointcloud_file_path)
            pointcloud = o3d.io.read_point_cloud(pointcloud_file_path)
            self.pointcloud_list.append(pointcloud)
        return True

    def getPointListWithLabel(self, point_list, label_list, label):
        point_list_with_label = []
        for i in range(len(point_list)):
            if label_list[i] != label:
                continue
            point_list_with_label.append(point_list[i])
        return point_list_with_label

    def splitLabeledPoints(self, scene_pointcloud_file_path):
        self.labeled_point_cluster_list = []

        print("start reading labels...")
        lines = None
        with open(scene_pointcloud_file_path, "r") as f:
            lines = f.readlines()

        label_list = []
        find_start_line = False
        for line in tqdm(lines):
            if "DATA ascii" in line:
                find_start_line = True
                continue
            if not find_start_line:
                continue
            line_data = line.split("\n")[0].split(" ")
            if len(line_data) < self.label_channel_idx:
                continue
            label_list.append(int(line_data[self.label_channel_idx]))

        print("start reading points in pointcloud...", end="")
        scene_pointcloud = o3d.io.read_point_cloud(scene_pointcloud_file_path)
        points = np.asarray(scene_pointcloud.points).tolist()
        if len(points) != len(label_list):
            print("PointCloudRender::createColor : label size not matched!")
            return False
        print("SUCCESS!")

        labeled_point_list = []
        for _ in range(len(self.labels)):
            labeled_point_list.append([])
        print("start clustering points in pointcloud...")
        for i in tqdm(range(len(points))):
            point = points[i]
            label = label_list[i]
            labeled_point_list[label].append(point)
        for labeled_point_cluster in labeled_point_list:
            self.labeled_point_cluster_list.append(labeled_point_cluster)
        return True

    def render(self, show_labels, scene_pointcloud_file_path=None):
        if scene_pointcloud_file_path is not None:
            print("start reading wall...")
            self.splitLabeledPoints(scene_pointcloud_file_path)

        rendered_pointcloud = o3d.geometry.PointCloud()

        render_points = []
        render_colors = []
        print("start create rendered pointcloud...")
        for i in tqdm(range(len(self.pointcloud_list))):
            points = np.asarray(self.pointcloud_list[i].points).tolist()
            if len(points) == 0:
                continue
            for point in points:
                render_points.append(point)
                render_colors.append(self.d3_40_colors_rgb[i % len(self.d3_40_colors_rgb)] / 255.0)

        if scene_pointcloud_file_path is not None:
            print("start create rendered wall...")
            for wall_point in tqdm(self.labeled_point_cluster_list[0]):
                if abs(wall_point[2]) > 0.01:
                    continue
                render_points.append(wall_point)
                render_colors.append(np.array([132, 133, 135], dtype=np.uint8) / 255.0)

        rendered_pointcloud.points = o3d.utility.Vector3dVector(np.array(render_points))
        rendered_pointcloud.colors = o3d.utility.Vector3dVector(np.array(render_colors))

        o3d.visualization.draw_geometries([rendered_pointcloud])
        return True

if __name__ == "__main__":
    pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_16_16-35-51/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_16_17-8-46/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_16_18-34-9/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_16-18-20/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_16-29-9/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_16-48-51/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_17-38-53/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_18-53-11/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_19-7-35/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_19-37-51/"
    #  pointcloud_folder_path = "./masked_pc/RUN_LOG/2022_1_17_19-56-28/"

    pointcloud_file_path_list = []
    pointcloud_folder_file_name_list = os.listdir(pointcloud_folder_path)
    scene_idx = 0
    for pointcloud_folder_file_name in pointcloud_folder_file_name_list:
        if "object" in pointcloud_folder_file_name:
            pointcloud_file_path_list.append(pointcloud_folder_path + pointcloud_folder_file_name)
        elif "scene" in pointcloud_folder_file_name:
            scene_idx = max(scene_idx, int(pointcloud_folder_file_name.split(".")[0].split("_")[1]))
    label_channel_idx = 3
    scene_pointcloud_file_path = pointcloud_folder_path + "scene_" + str(scene_idx) + ".pcd"

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
        0,
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


    pointcloud_render = ObjectPointCloudRender()
    pointcloud_render.loadPointCloud(pointcloud_file_path_list,
                                     label_channel_idx,
                                     labels)
    pointcloud_render.render(show_labels, scene_pointcloud_file_path)

