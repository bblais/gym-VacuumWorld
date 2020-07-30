import gym
import gym_VacuumWorld
import numpy as np
from Game import Table


env = gym.make("VacuumWorld-v0",N=3)

Q=Table()
G=0
alpha = 0.618



for episode in range(1,1001):
    done = False
    G, reward = 0,0
    state = env.reset()

    if not state in Q:
        Q[state]=Table()
        for action in range(env.action_space.n):
            Q[state][action]=0.0


    while done != True:
            action = Q[state].argmax() #1
            state2, reward, done, info = env.step(action) #2

            if not state2 in Q:
                Q[state2]=Table()
                for action in range(env.action_space.n):
                    Q[state2][action]=0.0


            Q[state][action] += alpha * (reward + Q[state2].max() - Q[state][action]) #3
            G += reward
            state = state2   
    if episode % 50 == 0:
        print('Episode {} Total Reward: {}'.format(episode,G))