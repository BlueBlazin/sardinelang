from .token import Token


class Environment:
  def __init__(self, outer):
    self.outer = outer
    self.env = dict()

  def revert(self, old_env):
    self.env = old_env

  def define(self, name: str, value):
    self.env[name] = value

  def get(self, name: Token):
    if name.raw_token in self.env:
      return self.env[name.raw_token]
    if self.outer:
      return self.outer.get(name)
    # TODO: raise runtime error

  def assign(self, name: Token, value):
    if name.raw_token in self.env:
      self.env[name.raw_token] = value
    if self.outer:
      self.outer.assign(name, value)
    # TODO: raise runtime error