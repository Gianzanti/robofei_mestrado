import os
import time
import unittest

import mujoco
import numpy as np
import imageio
from pyvirtualdisplay import Display

# Start a virtual display
vdisplay = Display(visible=False, size=(400, 400))
vdisplay.start()

model_path = os.path.join(os.path.dirname(__file__), "..", "src", "model", "scene.xml")

class DarwinOp3_TestModel(unittest.TestCase):
    def test_model_properties(self):
        model = mujoco.MjModel.from_xml_path(model_path)
        data = mujoco.MjData(model)
        mujoco.mj_resetData(model, data)

        print ("Model properties")
        print ("nq (number of generalized coordinates = dim(qpos)): ", model.nq)
        print ("nv (number of degrees of freedom = dim(qvel)): ", model.nv)
        print ("nu (number of actuators/controls = dim(ctrl)): ", model.nu)
        print ("nbody (number of bodies): ", model.nbody)
        print ("njnt (number of joints): ", model.njnt)
        print ("nsensor (number of sensors): ", model.nsensor)
        print ("nsensordata: ", model.nsensordata)
        print ("Data properties")
        print ("qpos: ", data.qpos)
        print ("qvel: ", data.qvel)
        print ("qacc: ", data.qacc)
        print ("sensor_data: ", data.sensordata)

        # Madgwick filter
        gyroscope = np.array([data.sensordata[0:3]])
        print ("Gyroscope: ", gyroscope)
        accelerometer = np.array([data.sensordata[3:6]])
        print ("Accelerometer: ", accelerometer)
        magnetometer = np.array([data.sensordata[6:9]])
        print ("Magnetometer: ", magnetometer)

    def test_viewer(self):
        model = mujoco.MjModel.from_xml_path(model_path)
        self.assertIsNotNone(model)

        data = mujoco.MjData(model)
        self.assertIsNotNone(data)


        # Create a renderer
        renderer = mujoco.Renderer(model, height=400, width=400)
        mujoco.mj_forward(model, data)
        renderer.update_scene(data)

        duration = 3  # (seconds)
        framerate = 15  # (Hz)
        frames = []

        # Simulate and render frames
        print("Simulating and capturing frames...")
        # set initial state
        mujoco.mj_resetData(model, data)

        while data.time < duration:
            mujoco.mj_step(model, data)
            if len(frames) < data.time * framerate:
                # print("rendering frame", len(frames))
                # Render the scene and add the frame to our list
                renderer.update_scene(data)
                pixels = renderer.render()
                frames.append(pixels)

        # Save the video
        output_path = 'simulation_video.mp4'
        print(f"Saving video to {output_path}...")
        with imageio.get_writer(output_path, fps=framerate) as writer:
            for frame in frames:
                writer.append_data(frame)

        print("Video saved successfully!")

        # Clean up
        renderer.close()
        vdisplay.stop()