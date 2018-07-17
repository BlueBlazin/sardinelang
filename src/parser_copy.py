from .nodes import *
from .sardine import SardineLang
from .token import TokenType


class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.current = 0

  def parse(self):
    tree = self._parse_exp()
    return tree

  def _parse_exp(self):
    return self._parse_logical_or()

  def _parse_logical_or(self):
    exp = self._parse_logical_and()
    while self._match(TokenType.OR):
      right = self._parse_logical_and()
      exp = Logical(exp, TokenType.OR, right)
    return exp

  def _parse_logical_and(self):
    exp = self._parse_equality()
    while self._match(TokenType.AND):
      right = self._parse_equality()
      exp = Logical(exp, TokenType.AND, right)
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
    return self._parse_primary()

  def _parse_primary(self):
    if self._match(TokenType.TRUE):
      return Literal(True)
    if self._match(TokenType.FALSE):
      return Literal(False)
    if self._match(TokenType.NONE):
      return Literal(None)
    if self._match(TokenType.NUMBER, TokenType.STRING):
      return Literal(self._previous().value)
    if self._match(TokenType.LEFT_PAREN):
      expr = self._parse_exp()
      self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)


  # helpers
  def _consume(self, token_type, message):
    if self._at_end() or self.tokens[self.current].type != token_type:
      # TODO: throw error
      pass
    self.current += 1

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