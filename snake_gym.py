import gym
from gym.envs.classic_control import rendering
import numpy as np
from gym.utils import play
from gym import spaces
from gym import error, spaces, utils
from gym.utils import seeding
from snake import Env, SnakeState
import time
import cv2


KEYWORD_TO_KEY = {
    (ord('j'), ): 1,
    (ord('l'), ): 2,
}

action_map = {
    0: None,
    1: 'left',
    2: 'right'
}

reward_map = {
    SnakeState.OK: 0,
    SnakeState.ATE: 1,
    SnakeState.DED: -1,
    SnakeState.WON: 1
}


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    def __init__(self, gs=10, main_gs=10, num_fruits=10, action_map=None):
        super(SnakeEnv, self).__init__()
        self.env = Env(gs, main_gs=main_gs, num_fruits=num_fruits)
        self.viewer = None
        self.action_map = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right'
        }
        if action_map is not None:
            self.action_map = action_map

        self.action_space = spaces.Discrete(len(self.action_map.keys()))
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.env.gs, self.env.gs, 3),
            dtype=np.uint8)

    def step(self, action):
        enum = self.env.update(self.action_map[action])

        # if enum != SnakeState.DED:
        rew = reward_map[enum]
        # else:
        #     rew = reward_map[enum]*(self.env.gs**2)

        # rew /= (self.env.gs**2)

        is_done = (enum in [SnakeState.DED, SnakeState.WON])
        info_dict = {}
        if is_done:
            info_dict['score'] = len(self.env.snake.tail)

        return self.env.to_image(), rew, is_done, info_dict

    def reset(self):
        self.env.reset()
        return self.env.to_image()

    def render(self, mode='human', close=False):
        im = self.env.to_image()
        if mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer(maxwidth=640)
                self.viewer.height = 640
                self.viewer.width = 640

            im = cv2.resize(im, (640, 640), interpolation=0)
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

            self.viewer.imshow(im)
            # time.sleep(0.05)
            return self.viewer.isopen
            # return im
        elif mode == 'jack':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer(maxwidth=640)
                self.viewer.height = 640
                self.viewer.width = 640

            self.viewer.imshow(cv2.resize(self.env.to_image(), (640, 640), interpolation=0))
            return self.viewer.isopen
        else:
            return cv2.cvtColor(cv2.resize(im, (640*2, 640*2), interpolation=0), cv2.COLOR_GRAY2BGR)

try:
    gym.envs.register(id="snakenv-v0", entry_point='snake_gym:SnakeEnv')
except Exception:
    print('already done?')

if __name__ == '__main__':
    action_map = {
        0: None,
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right'
    }

    KEYWORD_TO_KEY = {
        (ord('i'), ): 1,
        (ord('j'), ): 3,
        (ord('k'), ): 2,
        (ord('l'), ): 4,
    }

    def callback(obs_t, obs_tp1, action, rew, done, info):
        try:
            callback.rew += rew
        except Exception:
            callback.rew = rew
        print(callback.rew)

    env = gym.make('snakenv-v0', gs=20, main_gs=40, action_map=action_map)
    play.keys_to_action = KEYWORD_TO_KEY
    play.play(env, fps=15, keys_to_action=KEYWORD_TO_KEY, callback=callback)
