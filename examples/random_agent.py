import gym
import gym_VacuumWorld

env = gym.make("VacuumWorld-v0",N=6)
observation = env.reset()
for _ in range(20):
    env.render()
    action = env.action_space.sample()  # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)

    print("AORDI:",action,"\n\n",observation,reward,done,info)
    print()
    if done:
        observation = env.reset()
env.close()

# pip install Box2D
