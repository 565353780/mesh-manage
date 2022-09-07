#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Config.move import MOVE_LIST_DICT

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
    move_list = MOVE_LIST_DICT["matterport3d_03"]
    error_max = 0.5
    is_visual = False
    print_progress = True

    getHeatMap(partial_mesh_file_path,
               complete_mesh_file_path,
               save_partial_mesh_file_path,
               save_complete_mesh_file_path,
               move_list=move_list,
               error_max=error_max,
               is_visual=is_visual,
               print_progress=print_progress)
    return True

def demo_coscan():
    scene_result_folder_path = "/home/chli/chLi/coscan_data/scene_result/"
    scene_name = "front3d_19"
    gt_mesh_file_name = "19_cut.ply"
    coscan_result_file_name = "scene_29.ply"
    dong_result_file_name = "scene_27.ply"
    move_list = MOVE_LIST_DICT["front3d_19"]

    error_max = 0.5
    is_visual = False
    print_progress = True

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

    print("==================================")
    print("==== start get coscan heatmap ====")
    print("==================================")
    getHeatMap(coscan_partial_mesh_file_path,
               complete_mesh_file_path,
               coscan_save_partial_mesh_file_path,
               coscan_save_complete_mesh_file_path,
               move_list=move_list,
               error_max=error_max,
               is_visual=is_visual,
               print_progress=print_progress)

    print("================================")
    print("==== start get dong heatmap ====")
    print("================================")
    getHeatMap(dong_partial_mesh_file_path,
               complete_mesh_file_path,
               dong_save_partial_mesh_file_path,
               dong_save_complete_mesh_file_path,
               move_list=move_list,
               error_max=error_max,
               is_visual=is_visual,
               print_progress=print_progress)
    return True

if __name__ == "__main__":
    #  demo()
    demo_coscan()
