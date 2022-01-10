import numpy as np
import open3d as o3d

def draw_point_cloud(pcd):
    o3d.visualization.draw_geometries(
        [pcd],
        lookat=np.array(
            [0.084408626421175248, 0.13317439366565242, -1.8910266378878333]
        ),
        up=np.array([0.05651698451038889, 0.33066863310774841, -0.94205312246205419]),
        front=np.array(
            [0.062946611792935578, 0.94050395200128578, 0.33390124338455612]
        ),
        zoom=0.65,
    )

def colorize_point_cloud(original_pcd, labels):
    np.asarray(original_pcd.colors)[:, :] = d3_40_colors_rgb[labels.astype(np.int32) % 40] / 255.0


def main():
    original_point_cloud = np.load("plots/point_cloud.npy")
    original_pcd = o3d.geometry.PointCloud()
    original_pcd.points = o3d.utility.Vector3dVector(original_point_cloud[:, :3])
    original_pcd.colors = o3d.utility.Vector3dVector((original_point_cloud[:, 3:6] / 255.0))

    colorize_point_cloud(original_pcd, original_point_cloud[:, 6])

    draw_point_cloud(original_pcd)

if __name__ == "__main__":
    main()

