import numpy as np
from stable_baselines3.common.callbacks import BaseCallback


class TensorboardCallback(BaseCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """

    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_positions = []

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        self.episode_positions = {
            "x_positions": [],
            "y_positions": [],
            "z_positions": [],
            "x_velocities": [],
            "y_velocities": [],
            "health_rewards": [],
            "forward_rewards": [],
            "control_costs": [],
            "pos_deviation_costs": [],
            "lateral_velocity_costs": [],
        }


    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: If the callback returns False, training is aborted early.
        """
        for env_idx in range(self.training_env.num_envs):
            info = self.locals['infos'][env_idx]
            self.episode_positions['x_positions'].append(info['x_position'])
            self.episode_positions['y_positions'].append(info['y_position'])
            self.episode_positions['z_positions'].append(info['z_position'])
            self.episode_positions['x_velocities'].append(info['x_velocity'])
            self.episode_positions['y_velocities'].append(info['y_velocity'])
            self.episode_positions['health_rewards'].append(info['health_reward'])
            self.episode_positions['forward_rewards'].append(info['forward_reward'])
            self.episode_positions['control_costs'].append(info['control_cost'])
            self.episode_positions['pos_deviation_costs'].append(info['pos_deviation_cost'])
            self.episode_positions['lateral_velocity_costs'].append(info['lateral_velocity_cost'])

        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        # print("005 - Rollout Ended")
        if self.episode_positions:
            x_values = np.array(self.episode_positions['x_positions'])
            self.logger.record('mean_episode/pos_x', np.mean(x_values))

            y_values = np.array(self.episode_positions['y_positions'])
            self.logger.record('mean_episode/pos_y', np.mean(y_values))

            z_values = np.array(self.episode_positions['z_positions'])
            self.logger.record('mean_episode/pos_z', np.mean(z_values))

            x_vel_values = np.array(self.episode_positions['x_velocities'])
            self.logger.record('mean_episode/vel_x', np.mean(x_vel_values))

            y_vel_values = np.array(self.episode_positions['y_velocities'])
            self.logger.record('mean_episode/vel_y', np.mean(y_vel_values))

            health_values = np.array(self.episode_positions['health_rewards'])
            self.logger.record('mean_episode/health_reward', np.mean(health_values))

            forward_values = np.array(self.episode_positions['forward_rewards'])
            self.logger.record('mean_episode/forward_reward', np.mean(forward_values))

            control_costs = np.array(self.episode_positions['control_costs'])
            self.logger.record('mean_episode/control_cost', np.mean(control_costs))

            pos_deviation_costs = np.array(self.episode_positions['pos_deviation_costs'])
            self.logger.record('mean_episode/pos_deviation_cost', np.mean(pos_deviation_costs))

            lateral_velocity_costs = np.array(self.episode_positions['lateral_velocity_costs'])
            self.logger.record('mean_episode/lateral_velocity_cost', np.mean(lateral_velocity_costs))

        self.episode_positions = {
            "x_positions": [],
            "y_positions": [],
            "z_positions": [],
            "x_velocities": [],
            "y_velocities": [],
            "health_rewards": [],
            "forward_rewards": [],
            "control_costs": [],
            "pos_deviation_costs": [],
            "lateral_velocity_costs": [],
        }
