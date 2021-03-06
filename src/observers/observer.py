import math
from abc import ABC, abstractmethod

class StateObserver(ABC):
  def __init__(self,
               params):
    self._params = params
    self._velocity_range = \
      self._params["ML"]["Observer"]["velocity_range",
      "Boundaries for min and max velocity for normalization",
      [0, 100]]
    self._theta_range = \
      self._params["ML"]["Observer"]["theta_range",
      "Boundaries for min and max theta for normalization",
      [0, 2*math.pi]]
    self._normalization_enabled = \
      self._params["ML"]["Observer"]["normalization_enabled",
      "Whether normalization should be performed",
      True]
    self._max_num_vehicles = \
      self._params["ML"]["Observer"]["max_num_agents",
      "The concatenation state size is the ego agent plus max num other agents",
      2]
    self._world_x_range = [-10000, 10000]
    self._world_y_range = [-10000, 10000]

  @abstractmethod
  def observe(self, observed_world):
    """Observes the world
    
    Arguments:
        world {bark.ObservedWorld} -- observed BARK world
        agents_to_observe {list(int)} -- ids of agents to observe
    
    Returns:
        np.array -- concatenated state array
    """
    pass
  
  def _select_state_by_index(self, state):
    """selects a subset of an array using the state definition
    
    Arguments:
        state {np.array} -- full state space
    
    Returns:
        np.array -- reduced state space
    """
    return state[self._state_definition]

  def reset(self, world):
    bb = world.bounding_box
    self._world_x_range = [bb[0].x(), bb[1].x()]
    self._world_y_range = [bb[0].y(), bb[1].y()]
    return world

  @property
  def observation_space(self):
    pass