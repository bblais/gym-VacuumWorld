from gym.envs.registration import register

register(
  id='VacuumWorld-v0',
  entry_point='gym_VacuumWorld.envs:VacuumWorldEnv',
)
