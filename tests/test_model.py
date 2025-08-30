import os
import time
import unittest

import mujoco
import mujoco.viewer
import numpy as np

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
        # print ("ngeom (number of geoms): ", model.ngeom)
        # print ("nsite (number of sites): ", model.nsite)
        print ("nsensor (number of sensors): ", model.nsensor)
        print ("nsensordata: ", model.nsensordata)
        print ("Data properties")
        print ("qpos: ", data.qpos)
        print ("qvel: ", data.qvel)
        print ("qacc: ", data.qacc)
        # print ("qfrc_applied: ", data.qfrc_applied)
        print ("sensor_data: ", data.sensordata)

        # Madgwick filter
        gyroscope = np.array([data.sensordata[0:3]])
        print ("Gyroscope: ", gyroscope)
        accelerometer = np.array([data.sensordata[3:6]])
        print ("Accelerometer: ", accelerometer)
        magnetometer = np.array([data.sensordata[6:9]])
        print ("Magnetometer: ", magnetometer)
        # madgwick = Madgwick(gyr=gyroscope, acc=accelerometer,
        # mag=magnetometer, q0=[0.7071, 0.0, 0.7071, 0.0])   # Using MARG
        # print ("Madgwick filter: ", madgwick.Q)

    def test_viewer(self):
        model = mujoco.MjModel.from_xml_path(model_path)
        self.assertIsNotNone(model)

        data = mujoco.MjData(model)
        self.assertIsNotNone(data)

        # madgwick = Madgwick()
        # # self._gravity_quat = np.array([0.7071, 0.0, 0.7071, 0.0])
        # gravity_quat = np.array([0.7071, 0.0, 0.7071, 0.0])

        # set initial state
        mujoco.mj_resetData(model, data)

        with mujoco.viewer.launch_passive(model, data) as viewer:
            # Close the viewer automatically after 30 wall-seconds.
            start = time.time()

            while viewer.is_running() and time.time() - start < 600:
                step_start = time.time()
                gyr = np.array(data.sensordata[0:3])
                acc = np.array(data.sensordata[3:6])
                mag = np.array(data.sensordata[6:9])
                print (f"Gyr: {gyr}")
                print (f"Acc: {acc}")
                print (f"Mag: {mag}")
                # gravity_quat = madgwick.updateMARG(gravity_quat, gyr=gyr,
                # acc=acc, mag=mag).flatten()
                # print (f"Gravity Quat: {gravity_quat}")

                # mj_step can be replaced with code that also evaluates
                # a policy and applies a control signal before stepping the physics.
                mujoco.mj_step(model, data)

                # Example modification of a viewer option: toggle contact points
                # every two seconds.
                with viewer.lock():
                    viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(
                        data.time % 2
                    )

                # Pick up changes to the physics state, apply perturbations,
                # update options from GUI.
                viewer.sync()

                # Rudimentary time keeping, will drift relative to wall clock.
                time_until_next_step = model.opt.timestep - (time.time() - step_start)
                if time_until_next_step > 0:
                    time.sleep(time_until_next_step)


