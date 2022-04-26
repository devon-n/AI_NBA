# Import libs
import time
start_time = time.time()

import os
import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np


from stable_baselines.common.vec_env import DummyVecEnv, VecCheckNan
from stable_baselines.common.env_checker import check_env
from stable_baselines import PPO2, A2C
from stable_baselines.common.callbacks import EvalCallback

from Betting_env import BettingEnv

training = True

# Normalise rewards as well
# Try with stablebaselines3


results = pd.read_csv('./Scraping/Games and Stats.csv')
df = results.drop(['Date', 'Home', 'Visitor', 'Home PTS', 'Vis PTS', 'Home Points Dif', 'Home Win'], axis=1)
print('shape: ', results.shape)
results.drop(['Date', 'Home', 'Visitor'], axis=1, inplace=True)
df = df.astype(float)
# normed = (df-df.min())/(df.max()-df.min())

# Normalize data
for col in df.columns:
    df[col] = (df[col]-df[col].min()) / (df[col].max() - df[col].min())
df = df.round(10)


env = DummyVecEnv([lambda: BettingEnv(df, results, INITIAL_BALANCE=100)])

# env = VecCheckNan(env, raise_exception=True)
# check_env(env, warn=True)

eval_callback = EvalCallback(env, best_model_save_path='./logs/',
                             log_path='./logs/', eval_freq=500,
                             deterministic=True, render=False)

model = A2C('MlpPolicy', env, verbose=0)
# model = PPO2('MlpPolicy', env, verbose=0)

if training:
    model.learn(total_timesteps=10000000)

    save_path = os.path.join('Training', 'Saved Models', 'Betting_Model')
    model.save(save_path)

else:
    obs = env.reset()
    for i in range(5000):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
    #     env.render()

end_time = time.time()
total_time = end_time - start_time

print(round(total_time / 60 / 60), ' Hours ', round(total_time / 60), ' Minutes')

