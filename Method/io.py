#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.path import getValidFilePath

def loadPCD(pcd_file_path):
    valid_file_path = getValidFilePath(pcd_file_path)
    if valid_file_path is None:
        print("[ERROR][io::loadPCD]")
        print("\t getValidFilePath failed!")
        return [], []

    channel_name_list = []
    point_num = -1
    data_start_line_idx = -1

    lines = []
    with open(valid_file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]

        if "FIELDS" in line:
            channel_name_list = line.split("\n")[0].split("FIELDS ")[1].split(" ")
            continue

        if "POINTS" in line:
            point_num = int(line.split("\n")[0].split(" ")[1])
            continue

        if "DATA ascii" in line:
            data_start_line_idx = i + 1
            break

    if data_start_line_idx == -1:
        print("[ERROR][io::loadPCD]")
        print("\t data_start_line not found!")
        return [], []

    if point_num == -1:
        return [], []

    channel_value_list_list = []

    point_data_line_list = lines[data_start_line_idx: data_start_line_idx + point_num]
    for point_data_line in point_data_line_list:
        point_data = point_data_line.split("\n")[0].split(" ")[:len(channel_name_list)]

        channel_value_list = []
        for i in range(len(channel_name_list)):
            channel_value_list.append(float(point_data[i]))

        channel_value_list_list.append(channel_value_list)

    return channel_name_list, channel_value_list_list

def loadPLY(ply_file_path, load_point_only=False):
    valid_file_path = getValidFilePath(ply_file_path)
    if valid_file_path is None:
        print("[ERROR][io::loadPLY]")
        print("\t getValidFilePath failed!")
        if load_point_only:
            return [], []
        return [], [], []

    channel_name_list = []
    point_num = -1
    face_num = -1
    data_start_line_idx = -1

    lines = []
    with open(valid_file_path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]

        if "property" in line:
            if "property list" in line:
                continue
            channel_name = line.split("\n")[0].split(" ")[2]
            channel_name_list.append(channel_name)
            continue

        if "element vertex" in line:
            point_num = int(line.split("\n")[0].split(" ")[2])
            continue

        if "element face" in line:
            face_num = int(line.split("\n")[0].split(" ")[2])
            continue

        if "end_header" in line:
            data_start_line_idx = i + 1
            break

    if data_start_line_idx == -1:
        print("[ERROR][io::loadPLY]")
        print("\t data_start_line not found!")
        if load_point_only:
            return [], []
        return [], [], []

    if point_num == -1:
        if load_point_only:
            return [], []
        return [], [], []

    channel_value_list_list = []

    point_data_line_list = lines[data_start_line_idx: data_start_line_idx + point_num]
    for point_data_line in point_data_line_list:
        point_data = point_data_line.split("\n")[0].split(" ")[:len(channel_name_list)]

        channel_value_list = []
        for i in range(len(channel_name_list)):
            channel_value_list.append(float(point_data[i]))

        channel_value_list_list.append(channel_value_list)

    if load_point_only:
        return channel_name_list, channel_value_list_list

    if face_num == -1:
        return channel_name_list, channel_value_list_list, []

    point_idx_list_list = []

    face_data_line_list = lines[data_start_line_idx + point_num: data_start_line_idx + point_num + face_num]
    for face_data_line in face_data_line_list:
        face_data = face_data_line.split("\n")[0].split(" ")
        point_idx_num = int(face_data[0])
        point_idx_list = []
        for i in range(point_idx_num):
            point_idx_list.append(int(face_data[i + 1]))
        point_idx_list_list.append(point_idx_list)

    return channel_name_list, channel_value_list_list, point_idx_list_list

def loadFileData(file_path, load_point_only=False):
    if file_path[-4:] == ".pcd":
        return loadPCD(file_path)

    if file_path[-4:] == ".ply":
        return loadPLY(file_path, load_point_only)
    return

