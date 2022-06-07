import os

os.environ['PYOPENGL_PLATFORM'] = 'osmesa'

import math

import numpy as np
import open3d as o3d
import cv2


def getModelAndRender(fileName, albedoName, xangle, yangle, cameraeye, modelname):
    render = o3d.visualization.rendering.OffscreenRenderer(2000, 2000, headless=True)
    model, mat = getModel(fileName=fileName, albedoName=albedoName, xangle=xangle, yangle=yangle)
    render.scene.add_geometry("model", model, mat)
    center = [0, 0, 0]  # look_at target
    eye = cameraeye  # camera position
    up = [0, 1, 0]  # camera orientation
    render.scene.camera.look_at(center, eye, up)
    render.scene.set_background([255, 0, 0, 0])
    # render.render_to_image()
    img_o3d = render.render_to_image()
    return img_o3d
    #


def getModel(fileName, albedoName, xangle, yangle):
    model_name = fileName
    model = o3d.io.read_triangle_mesh(model_name)

    R = model.get_rotation_matrix_from_xyz((math.radians(yangle), (math.radians(-xangle)), 0))
    model.rotate(R, center=(0, 0, 0))

    material = o3d.visualization.rendering.MaterialRecord()
    material.shader = "defaultLit"
    albedo_name = albedoName
    material.albedo_img = o3d.io.read_image(albedo_name)

    return (model, material)


for x in range(-45, 46):
    for y in range(-45, 46):
        xangle = x * 2
        yangle = y * 2
        img = getModelAndRender("../../models/viking/viking.obj", "../../models/viking/helmet_color.png", xangle, yangle,
                                [0, 0.2, 1],
                                "hat")
        fname = "imgs/viking/viking_" + str(xangle) + "_" + str(yangle) + ".jpg"
        o3d.io.write_image(fname, img)
        print(fname)
