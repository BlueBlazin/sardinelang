from .nodes import *
from .token import TokenType


class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.current = 0

  def parse(self):
    statements = []
    while not self._at_end():
      statements.append(self._parse_declaration())
    return statements

  def _parse_declaration(self):
    if self._match(TokenType.DEC): 
      return self._parse_var_declaration()
    if self._match(TokenType.DEF):
      return self._parse_fun_definition()
    return self._parse_statement()

  def _parse_var_declaration(self):
    name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")
    initializer = None

    if self._match(TokenType.EQUAL):
      initializer = self._parse_exp()
    self._consume(TokenType.NEWLINE, "Expect newline after variable declaration.")
    return VarDec(name, initializer)

  def _parse_fun_definition(self):
    name = self._consume(TokenType.IDENTIFIER, "Expect name after 'def'.")
    self._consume(TokenType.LEFT_PAREN, "Expect '(' after name.")
    parameters = []
    if not self._check(TokenType.RIGHT_PAREN):
      while True:
        parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name."))
        if not self._match(TokenType.COMMA): break
    self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

    self._consume(TokenType.DO, "Expect 'do' before body.")
    body = self._parse_block()
    return FunctionDefinition(name, parameters, body)

  def _parse_statement(self):
    if self._match(TokenType.PRINT):
      return self._parse_print()
    if self._match(TokenType.DO):
      return self._parse_block()
    if self._match(TokenType.IF):
      return self._parse_if_stmt()
    if self._match(TokenType.RETURN):
      return self._parse_return_stmt()
    return self._parse_exp_stmt()

  def _parse_print(self):
    expr = self._parse_exp_stmt()
    return Print(expr)

  def _parse_block(self):
    statements = []
    while not self._check(TokenType.END):
      statements.append(self._parse_declaration())
    self._consume(TokenType.END, "Expect 'end' after block.")
    return Block(statements)

  def _parse_if_stmt(self):
    condition = self._parse_exp()
    then_branch = self._parse_statement()
    else_branch = None
    if self._match(TokenType.ELSE):
      else_branch = self._parse_statement()
    return If(condition, then_branch, else_branch)

  def _parse_return_stmt(self):
    keyword = self._previous()
    value = None
    if not self._check(TokenType.NEWLINE):
      value = self._parse_exp()
    self._consume(TokenType.NEWLINE, "Expect newline after return.")
    return Return(keyword, value)

  def _parse_exp_stmt(self):
    expr = self._parse_exp()
    self._consume(TokenType.NEWLINE, "Expect newline after expression.")
    return Expression(expr)

  def _parse_exp(self):
    return self._parse_assignment()

  def _parse_assignment(self):
    expr = self._parse_logical_or()

    if self._match(TokenType.EQUAL):
      equals = self._previous()
      value = self._parse_assignment()
    
      if not isinstance(expr, Variable):
        # TODO: raise error
        pass
      name = expr.name
      return VarAssign(name, value)
    return expr

  def _parse_logical_or(self):
    exp = self._parse_logical_and()
    while self._match(TokenType.OR):
      operator = self._previous()
      right = self._parse_logical_and()
      exp = Logical(exp, operator, right)
    return exp

  def _parse_logical_and(self):
    exp = self._parse_equality()
    while self._match(TokenType.AND):
      operator = self._previous()
      right = self._parse_equality()
      exp = Logical(exp, operator, right)
    return exp

  def _parse_equality(self):
    exp = self._parse_comparison()
    while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator = self._previous()
      right = self._parse_comparison()
      exp = Binary(exp, operator, right)
    return exp

  def _parse_comparison(self):
    exp = self._parse_addition()
    while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator = self._previous()
      right = self._parse_addition()
      exp = Binary(exp, operator, right)
    return exp

  def _parse_addition(self):
    exp = self._parse_multiplication()
    while self._match(TokenType.PLUS, TokenType.MINUS):
      operator = self._previous()
      right = self._parse_multiplication()
      exp = Binary(exp, operator, right)
    return exp

  def _parse_multiplication(self):
    exp = self._parse_unary()
    while self._match(TokenType.STAR, TokenType.SLASH):
      operator = self._previous()
      right = self._parse_unary()
      exp = Binary(exp, operator, right)
    return exp

  def _parse_unary(self):
    if self._match(TokenType.NOT, TokenType.MINUS):
      operator = self._previous()
      right = self._parse_unary()
      return Unary(operator, right)
    return self._parse_function_call()

  def _parse_function_call(self):
    expr = self._parse_primary()
    while True:
      if self._match(TokenType.LEFT_PAREN):
        expr = self._finish_call(expr)
      else:
        break
    return expr

  def _finish_call(self, callee):
    arguments = []
    if not self._check(TokenType.RIGHT_PAREN):
      while True:
        arguments.append(self._parse_exp())
        if not self._match(TokenType.COMMA): break
    
    paren = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
    return FunctionCall(callee, paren, arguments)

  def _parse_primary(self):
    if self._match(TokenType.TRUE):
      return Literal(True)
    if self._match(TokenType.FALSE):
      return Literal(False)
    if self._match(TokenType.NONE):
      return Literal(None)
    if self._match(TokenType.NUMBER, TokenType.STRING):
      return Literal(self._previous().value)
    if self._match(TokenType.IDENTIFIER):
      return Variable(self._previous())
    if self._match(TokenType.LEFT_PAREN):
      expr = self._parse_exp()
      self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)


  # helpers
  def _check(self, token_type):
    if self._at_end():
      return False
    return self.tokens[self.current].type == token_type

  def _consume(self, token_type, message):
    if self._at_end() or self.tokens[self.current].type != token_type:
      # TODO: throw error
      pass
    tok = self.tokens[self.current]
    self.current += 1
    return tok

  def _previous(self):
    # returns previous token
    return self.tokens[self.current-1]

  def _match(self, *token_types):
    # returns True and increments current if current tokens type matches one of the token_types
    if self._at_end():
      return False

    for token_type in token_types:
      if self.tokens[self.current].type == token_type:
        self.current += 1
        return True
    return False

  def _at_end(self):
    return self.current == len(self.tokens)