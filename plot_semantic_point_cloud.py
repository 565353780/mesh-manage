import numpy as np
import open3d as o3d

def colorize_point_cloud(original_pcd, labels):
    np.asarray(original_pcd.colors)[:, :] = d3_40_colors_rgb[labels.astype(np.int32) % 40] / 255.0


def main():
    original_point_cloud = np.load("plots/point_cloud.npy")
    original_pcd = o3d.geometry.PointCloud()
    original_pcd.points = o3d.utility.Vector3dVector(original_point_cloud[:, :3])
    original_pcd.colors = o3d.utility.Vector3dVector((original_point_cloud[:, 3:6] / 255.0))

    colorize_point_cloud(original_pcd, original_point_cloud[:, 6])

