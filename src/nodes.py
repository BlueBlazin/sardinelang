from .token import *
from .sardine_function import SardineFunction
from copy import deepcopy
from .errors import ReturnInterrupt

#############################################################################################
# Expressions
#############################################################################################

class Expr:
  pass

class Binary(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr):
    self.left = left
    self.right = right
    self.operator = operator

  def evaluate(self, env):
    left = self.left.evaluate(env)
    right = self.right.evaluate(env)
    operator = self.operator.type

    if operator == TokenType.GREATER:
      return left > right
    if operator == TokenType.GREATER_EQUAL:
      return left >= right
    if operator == TokenType.LESS:
      return left < right
    if operator == TokenType.LESS_EQUAL:
      return left <= right
    if operator == TokenType.MINUS:
      return left - right
    if operator == TokenType.PLUS:
      return left + right
    if operator == TokenType.SLASH:
      return left / right
    if operator == TokenType.STAR:
      return left * right
    if operator == TokenType.BANG_EQUAL:
      return left != right
    if operator == TokenType.EQUAL_EQUAL:
      return left == right

  def __str__(self):
    return "( " + self.operator.raw_token + " " + str(self.left) + " " + str(self.right) + " )"


class Logical(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr):
    self.left = left
    self.right = right
    self.operator = operator

  def evaluate(self, env):
    left = self.left.evaluate(env)
    operator = self.operator.type
    if operator == TokenType.OR:
      if left: return left
    else:
      if not left: return left
    return self.right.evaluate(env)

  def __str__(self):
    return "( " + self.operator.raw_token + " " + str(self.left) + " " + str(self.right) + " )"


class Unary(Expr):
  def __init__(self, operator: Token, right: Expr):
    self.operator = operator
    self.right = right

  def evaluate(self, env):
    right = self.right.evaluate(env)
    operator = self.operator.type

    if operator == TokenType.NOT:
      return not right
    if operator == TokenType.MINUS:
      return -right

  def __str__(self):
    return "( " + self.operator.raw_token + " " + str(self.right) + " )"


class Literal(Expr):
  def __init__(self, value):
    self.value = value

  def evaluate(self, env):
    return self.value

  def __str__(self):
    return str(self.value) if not isinstance(self.value, str) else '"' + self.value + '"'


class Grouping(Expr):
  def __init__(self, expr: Expr):
    self.expr = expr

  def evaluate(self, env):
    return self.expr.evaluate(env)

  def __str__(self):
    return "( group " + str(self.expr) + " )"


class Variable(Expr):
  # for calling variables (print x)
  def __init__(self, name: Token):
    self.name = name

  def evaluate(self, env):
    return env.get(self.name)

  def __str__(self):
    return self.name.raw_token


class VarAssign(Expr):
  # for assigning (already declared) variables with new values (x = 2)
  def __init__(self, name: Token, value: Expr):
    self.name = name
    self.value = value

  def evaluate(self, env):
    value = self.value.evaluate(env)
    env.assign(self.name, value)
    return value

  def __str__(self):
    return "( assign " + self.name.raw_token + " " + str(self.value) + " )"


class FunctionCall(Expr):
  def __init__(self, callee: Expr, paren: Token, arguments):
    self.callee = callee
    self.paren = paren  # the closing parenthesis of the function call is stored for error reporting
    self.arguments = arguments

  def evaluate(self, env):
    callee = self.callee.evaluate(env)
    arguments = []
    for arg in self.arguments:
      arguments.append(arg.evaluate(env))
    
    if not isinstance(callee, SardineFunction):
      # TODO: raise runtime error
      pass
    
    if len(arguments) != callee.arity():
      # TODO: raise runtime error
      pass
    
    return callee(env, arguments)



#############################################################################################
# Statements
#############################################################################################

class Stmt:
  pass

class VarDec(Stmt):
  # for variable declarations (dec x = 1)
  def __init__(self, name: Token, initializer: Expr):
    self.name = name
    self.initializer = initializer

  def evaluate(self, env):
    value = None
    if self.initializer != None:
      value = self.initializer.evaluate(env)
    env.define(self.name.raw_token, value)
    return None

  def __str__(self):
    return "( dec " + self.name.raw_token + " " + str(self.initializer) + " )"


class Print(Stmt):
  def __init__(self, expr: Expr):
    self.expr = expr

  def evaluate(self, env):
    print(self.expr.evaluate(env))

  def __str__(self):
    return "( print " + str(self.expr) + " )"


class Expression(Stmt):
  def __init__(self, expr: Expr):
    self.expr = expr

  def evaluate(self, env):
    return self.expr.evaluate(env)

  def __str__(self):
    return str(self.expr)


class Block(Stmt):
  def __init__(self, statements):
    self.statements = statements

  def evaluate(self, env):
    outer_env = deepcopy(env.env)#deepcopy(env)
    for stmt in self.statements:
      stmt.evaluate(env)
    env.revert(outer_env)

  def __str__(self):
    return "( block " + " ".join(str(stmt) for stmt in self.statements) + " )"


class If(Stmt):
  def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
    self.condition = condition
    self.then_branch = then_branch
    self.else_branch = else_branch

  def evaluate(self, env):
    condition = self.condition.evaluate(env)
    if condition:
      self.then_branch.evaluate(env)
    elif self.else_branch:
      self.else_branch.evaluate(env)
    return None


class FunctionDefinition(Stmt):
  def __init__(self, name: Token, parameters, body):
    self.name = name
    self.parameters = parameters
    self.body = body

  def evaluate(self, env):
    function = SardineFunction(self)
    env.define(self.name.raw_token, function)
    return None


class Return(Stmt):
  def __init__(self, keyword: Token, value: Expr):
    self.keyword = keyword
    self.value = value

  def evaluate(self, env):
    value = self.value.evaluate(env) if self.value else None
    raise ReturnInterrupt(value)