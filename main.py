import trimesh
import pyrender
import numpy as np

# load + center mesh
tri_mesh = trimesh.load("skull.obj")
mesh = pyrender.Mesh.from_trimesh(tri_mesh)
mesh_pose = np.eye(4)

# scene setup
scene = pyrender.Scene(bg_color=[0,0,0,0])
scene.add(mesh, pose=mesh_pose)

camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.414)
light = pyrender.DirectionalLight()

# calculate camera pose based on bounding box of the mesh
bbox = tri_mesh.bounding_box.extents
scale = np.max(bbox)
camera_distance = scale * 2
cam_pose = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,camera_distance],
    [0,0,0,1]
])

scene.add(camera, pose=cam_pose)
scene.add(light, pose=cam_pose)

pyrender.Viewer(scene, viewer_flags={"use_raymond_lighting": True})

# offscreen rendering before contours + suggestive contours
#r = pyrender.OffscreenRenderer(640, 640)
#color, depth = r.render(scene)
