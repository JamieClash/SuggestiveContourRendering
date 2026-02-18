import trimesh
import pyrender
import numpy as np

# load + center mesh
tri_mesh = trimesh.load("skull.obj")
tri_mesh.apply_translation(-tri_mesh.centroid)

mesh = pyrender.Mesh.from_trimesh(tri_mesh)
mesh_pose = np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,-1,0,0],
    [0,0,0,1]
])

# scene setup
scene = pyrender.Scene(bg_color=[0,0,0,0])
scene.add(mesh, pose=mesh_pose)

camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.414)
light = pyrender.DirectionalLight()

# calculate camera pose based on bounding box of the mesh
bbox = tri_mesh.bounding_box.extents
scale = np.max(bbox)
camera_distance = scale * 2

def look_at(target, eye, up):
    forward = target - eye
    forward /= np.linalg.norm(forward)

    right = np.cross(forward, up)
    right /= np.linalg.norm(right)

    up = np.cross(right, forward)
    
    pose = np.eye(4)
    pose[:3, 0] = right
    pose[:3, 1] = up
    pose[:3, 2] = -forward
    pose[:3, 3] = eye

    return pose

origin = np.zeros(3)
eye = np.array([0, 0, camera_distance])
up = np.array([0, 1, 0])

cam_pose = look_at(origin, eye, up)
scene.add(camera, pose=cam_pose)
scene.add(light, pose=cam_pose)

pyrender.Viewer(scene, viewer_flags={"use_raymond_lighting": True})

# offscreen rendering before contours + suggestive contours
#r = pyrender.OffscreenRenderer(640, 640)
#color, depth = r.render(scene)
