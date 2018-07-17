from .environment import Environment

class Interpreter:
  def __init__(self):
    self.environment = Environment(None)

  def interpret(self, statements):
    for stmt in statements:
      stmt.evaluate(self.environment)