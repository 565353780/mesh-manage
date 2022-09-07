#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Method.heatmap import getHeatMap

def demo():
    partial_mesh_file_path = \
        "/home/chli/chLi/coscan_data/scene_result/matterport3d_03/coscan/scene_19.ply"
    complete_mesh_file_path = \
        "/home/chli/chLi/coscan_data/scene_result/matterport3d_03/matterport_03_cut.ply"
    save_partial_mesh_file_path = \
        "/home/chli/chLi/coscan_data/scene_result/matterport3d_03/part_coscan.ply"
    save_complete_mesh_file_path = \
        "/home/chli/chLi/coscan_data/scene_result/matterport3d_03/comp_coscan.ply"
    error_max = 0.5

    getHeatMap(partial_mesh_file_path,
               complete_mesh_file_path,
               save_partial_mesh_file_path,
               save_complete_mesh_file_path,
               error_max=error_max,
               print_progress=True)
    return True

def demo_coscan():
    scene_result_folder_path = "/home/chli/chLi/coscan_data/scene_result/"
    scene_name = "front3d_19"
    gt_mesh_file_name = "19_cut.ply"
    coscan_result_file_name = "scene_29.ply"
    dong_result_file_name = "scene_27.ply"

    error_max = 0.1 # front3d
    #  error_max = 0.5 # mp3d

    coscan_partial_mesh_file_path = scene_result_folder_path + \
        scene_name + "/coscan/" + coscan_result_file_name
    dong_partial_mesh_file_path = scene_result_folder_path + \
        scene_name + "/dong/" + dong_result_file_name

    complete_mesh_file_path = scene_result_folder_path + \
        scene_name + "/" + gt_mesh_file_name

    coscan_save_partial_mesh_file_path = scene_result_folder_path + \
        scene_name + "/part_coscan.ply"
    dong_save_partial_mesh_file_path = scene_result_folder_path + \
        scene_name + "/part_dong.ply"

    coscan_save_complete_mesh_file_path = scene_result_folder_path + \
        scene_name + "/comp_coscan.ply"
    dong_save_complete_mesh_file_path = scene_result_folder_path + \
        scene_name + "/comp_dong.ply"

    print("start get coscan heatmap...")
    getHeatMap(coscan_partial_mesh_file_path,
               complete_mesh_file_path,
               coscan_save_partial_mesh_file_path,
               coscan_save_complete_mesh_file_path,
               error_max=error_max,
               print_progress=True)

    print("start get dong heatmap...")
    getHeatMap(dong_partial_mesh_file_path,
               complete_mesh_file_path,
               dong_save_partial_mesh_file_path,
               dong_save_complete_mesh_file_path,
               error_max=error_max,
               print_progress=True)
    return True

if __name__ == "__main__":
    #  demo()
    demo_coscan()

