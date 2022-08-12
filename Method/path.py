#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Method.trans_format import transFormat

def isDataAscii(file_path):
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r") as f:
        lines = []
        try:
            lines = f.readlines()
        except:
            return False

        for line in lines:
            if "DATA" in line:
                if "ascii" not in line:
                    return False
                return True

            if "format" in line:
                if "ascii" not in line:
                    return False
                return True

    print("[ERROR][path::isDataAscii]")
    print("\t not find format!")
    return False

def getValidFilePath(pointcloud_file_path):
    if not os.path.exists(pointcloud_file_path):
        print("[ERROR][path::getValidFilePath]")
        print("\t file not exist!")
        return None

    if isDataAscii(pointcloud_file_path):
        return pointcloud_file_path

    valid_file_path = pointcloud_file_path[:-4] + "_ascii" + pointcloud_file_path[-4:]
    if not os.path.exists(valid_file_path):
        transFormat(pointcloud_file_path, valid_file_path)
    return valid_file_path

