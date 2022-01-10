import torch
import open3d as o3d
import numpy as np
import torch.utils.dlpack as dlp

def point_cloud_voxel_downsample(points: torch.Tensor, voxel_size=0.01):
    points = o3d.core.Tensor.from_dlpack(dlp.to_dlpack(points))
    pcd = o3d.t.geometry.PointCloud(points)
    pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    down_sampled_points = dlp.from_dlpack(pcd.point["positions"].to_dlpack())
    pcd.clear()
    return down_sampled_points

def point_cloud_voxel_downsample_with_rgb(input: torch.Tensor, voxel_size=0.01):
    if isinstance(input, np.ndarray):
        input = torch.from_numpy(input).cuda()
        init_numpy = True
    print(f"{input.shape[0]} points down sampling ... ...")
    points = o3d.core.Tensor.from_dlpack(dlp.to_dlpack(input[..., :3]))
    rgb = o3d.core.Tensor.from_dlpack(dlp.to_dlpack(input[..., 3:6]))
    label = o3d.core.Tensor.from_dlpack(dlp.to_dlpack(input[..., 6:7]))
    pcd = o3d.t.geometry.PointCloud().cuda()
    pcd.point["positions"] = points
    pcd.point["rgb"] = rgb
    pcd.point["label"] = label
    pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    sampled_points = dlp.from_dlpack(pcd.point["positions"].to_dlpack())
    sampled_rgb = dlp.from_dlpack(pcd.point["rgb"].to_dlpack())
    sampled_label = dlp.from_dlpack(pcd.point["label"].to_dlpack())
    down_points = torch.hstack([sampled_points, sampled_rgb, sampled_label])
    return down_points if not init_numpy else down_points.cpu().numpy()
