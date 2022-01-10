import numpy as np
import open3d as o3d

d3_40_colors_rgb: np.ndarray = np.array(
    [
        [164, 218, 252],
        [120, 173, 219],
        [253, 147, 81],
        [252, 234, 163],
        [0, 128, 128],
        [132, 220, 198],
        [255, 104, 107],
        [255, 166, 158],
        [148, 103, 189],
        [189, 147, 189],
        [140, 86, 75],
        [146, 94, 120],
        [227, 119, 194],
        [247, 182, 210],
        [127, 127, 127],
        [199, 199, 199],
        [188, 189, 34],
        [219, 219, 141],
        [23, 190, 207],
        [158, 218, 229],
        [57, 59, 121],
        [82, 84, 163],
        [107, 110, 207],
        [156, 158, 222],
        [99, 121, 57],
        [140, 162, 82],
        [181, 207, 107],
        [206, 219, 156],
        [140, 109, 49],
        [189, 158, 57],
        [231, 186, 82],
        [231, 203, 148],
        [132, 60, 57],
        [173, 73, 74],
        [214, 97, 107],
        [231, 150, 156],
        [123, 65, 115],
        [165, 81, 148],
        [206, 109, 189],
        [222, 158, 214],
    ],
    dtype=np.uint8,
)

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
