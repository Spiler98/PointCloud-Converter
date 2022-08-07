# PointCloud-Converter

## Description
* This is a small Python script that can convert point clouds to different formats
* When launched, it will convert every point cloud from a folder with a given input format to a desired output format

## Dependencies
* [NumPy](https://numpy.org/)
* [Open3D](http://www.open3d.org/)

## Running
* Program was developed in Python 3.9.9
* Running: ```py converter.py input_folder_path output_folder_path input_format output_format```
* Command line parameters for point cloud formats
  * "PCD_ASCII" - ascii ```.pcd```
  * "PCD_BIN" - binary ```.pcd```
  * "XYZ", "XYZN", "XYZRGB" - ```.xyz```, ```.xyzn```, ```.xyzrgb```
  * "PLY" - ```.ply```
  * "PTS" - ```.pts```
  * "BIN" - plain ```.bin```
  
 ## Notes
 * If you're converting from a format that's missing normals to ```.xyzn```, then the program will create a ```.xyz``` file instead
 * Same with missing rgb and ```.xyzrgb```
