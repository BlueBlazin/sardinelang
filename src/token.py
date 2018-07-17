from enum import Enum, auto

class TokenType(Enum):
  # single character tokens
  LEFT_PAREN = auto()
  RIGHT_PAREN = auto()
  DOT = auto()
  COMMA = auto() 
  STAR = auto()
  SLASH = auto()
  PLUS = auto()
  MINUS = auto()

  # one or two character tokens
  BANG_EQUAL = auto()
  EQUAL = auto()
  EQUAL_EQUAL = auto()
  GREATER = auto()
  GREATER_EQUAL = auto()
  LESS = auto()
  LESS_EQUAL = auto()

  # keywords
  AND = auto()
  OR = auto()
  NOT = auto() 
  DO = auto()
  END = auto()
  NONE = auto() 
  TRUE = auto()
  FALSE = auto()
  WHILE = auto() 
  FOR = auto()
  RETURN = auto()
  PRINT = auto()
  DEF = auto()
  DEC = auto()
  NEWLINE = auto()
  IF = auto()
  ELSE = auto()

  # literals
  IDENTIFIER = auto()
  STRING = auto()
  NUMBER = auto()
  
  EOF = auto()


class Token:
  def __init__(self, token_type: TokenType, raw_token: str, value, line: int):
    self.type = token_type
    self.raw_token = raw_token
    self.value = value
    self.line = line

  def __str__(self):
    return "<" + str(self.type) + ", " + "'" + self.raw_token + "'" + ">"