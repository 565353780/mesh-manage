#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mesh_manage.Module.renderer import Renderer


def demo():
    renderer = Renderer()

    for idx in range(28):
        mesh_file_path = \
                "/home/chli/chLi/coscan_data/fast_forward/ff_recon_result_render_gray_blue/merged_vpp_mesh_" + str(idx) + ".ply"
        save_image_file_path = \
                "/home/chli/chLi/coscan_data/fast_forward/ff_recon_result_render_gray_blue/merged_vpp_mesh_" + str(idx) + ".png"

        #  renderer.renderMesh(mesh_file_path)
        renderer.saveRenderMeshImage(mesh_file_path, save_image_file_path)
        return
    return True
