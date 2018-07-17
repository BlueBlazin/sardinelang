from .environment import Environment
from .errors import ReturnInterrupt


class SardineFunction:
  def __init__(self, definition):
    self.definition = definition

  def arity(self):
    return len(self.definition.parameters)

  def __call__(self, env, arguments):
    local_env = Environment(env)
    for i, argument in enumerate(arguments):
      local_env.define(self.definition.parameters[i].raw_token, argument)
    try:
      self.definition.body.evaluate(local_env)
    except ReturnInterrupt as r:
      return r.value
    return None