import numpy as np
import open3d as o3d
import struct
import os
import sys
from enum import Enum


class CloudFormat(Enum):
    PCD_ASCII = ".pcd"
    PCD_BIN = ".pcd"
    XYZ = ".xyz"
    XYZN = ".xyzn"
    XYZRGB = ".xyzrgb"
    PLY = ".ply"
    PTS = ".pts"
    BIN = ".bin"


def convert_from_bin(infile_path, outfile_path, out_cloud_format):
    size_float = 4
    list_points = []
    with open(infile_path, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_points.append([x, y, z])
            byte = f.read(size_float * 4)
    np_points = np.asarray(list_points)
    cloud_points = o3d.utility.Vector3dVector(np_points)
    cloud = o3d.geometry.PointCloud(cloud_points)
    print("Writing", outfile_path)
    if out_cloud_format.name == "PCD_BIN":
        o3d.io.write_point_cloud(outfile_path, cloud, write_ascii=False, print_progress=True)
    else:
        o3d.io.write_point_cloud(outfile_path, cloud, write_ascii=True, print_progress=True)


def convert_to_bin(infile_path, outfile_path):
    cloud = o3d.io.read_point_cloud(infile_path)
    points = np.asarray(cloud.points)
    print("Writing", outfile_path)
    with open(outfile_path, "wb") as f:
        for point in points:
            point_bytes = struct.pack("ffff", point[0], point[1], point[2], 1.0)
            f.write(point_bytes)


def convert(infile_path, outfile_path, out_cloud_format):
    cloud = o3d.io.read_point_cloud(infile_path)
    print("Writing", outfile_path)
    if out_cloud_format.name == "PCD_BIN":
        o3d.io.write_point_cloud(outfile_path, cloud, write_ascii=False, print_progress=True)
    else:
        o3d.io.write_point_cloud(outfile_path, cloud, write_ascii=True, print_progress=True)


def convert_files(in_folder, out_folder, in_cloud_format, out_cloud_format):
    for in_file in os.listdir(in_folder):
        file_name = in_file.split(".")[0]
        out_file = file_name + out_cloud_format.value

        infile_path = in_folder + in_file
        outfile_path = out_folder + out_file

        if in_cloud_format.name == "BIN":
            convert_from_bin(infile_path, outfile_path, out_cloud_format)
        else:
            if out_cloud_format.name == "BIN":
                convert_to_bin(infile_path, outfile_path)
            else:
                convert(infile_path, outfile_path, out_cloud_format)


def main():
    try:
        in_folder = sys.argv[1]
        out_folder = sys.argv[2]
        try:
            in_cloud_format = CloudFormat[sys.argv[3]]
            out_cloud_format = CloudFormat[sys.argv[4]]
            convert_files(in_folder, out_folder, in_cloud_format, out_cloud_format)
        except KeyError:
            print("Cloud formats must be one of the following:\n" +
                  "\t- PCD_ASCII\n" +
                  "\t- PCD_BIN\n" +
                  "\t- XYZ\n" +
                  "\t- XYZN\n" +
                  "\t- XYZRGB\n" +
                  "\t- PLY\n" +
                  "\t- PTS\n" +
                  "\t- BIN",
                  file=sys.stderr)
    except IndexError:
        if len(sys.argv) < 2:
            print("Missing input folder", file=sys.stderr)
        if len(sys.argv) < 3:
            print("Missing output folder", file=sys.stderr)
        if len(sys.argv) < 4:
            print("Missing input file format", file=sys.stderr)
        if len(sys.argv) < 5:
            print("Missing output file format", file=sys.stderr)


if __name__ == '__main__':
    main()
