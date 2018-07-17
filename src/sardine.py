import sys
from .tokenizer import Tokenizer
from .parser import Parser
from .interpreter import Interpreter
from .nodes import *


class SardineLang:
  interpreter = Interpreter()

  def run(args):
    if len(args) > 1:
      print("Usage: python sardine.py [script]", file=sys.stderr)
    elif len(args) == 1:
      SardineLang.run_file(args[0])
    else:
      SardineLang.run_repl()

  def run_file(path):
    with open(path, 'r') as f:
      source = f.read() + '\n'
      tokenizer = Tokenizer(source)
      tokens = tokenizer.tokenize()
      parser = Parser(tokens)
      SardineLang.interpreter.interpret(parser.parse())

  def run_repl():
    while True:
      try:
        tokenizer = Tokenizer(input("> ") + '\n')
        parser = Parser(tokenizer.tokenize())
        SardineLang.interpreter.interpret(parser.parse())
      except (EOFError, KeyboardInterrupt):
        print("")
        sys.exit(0)


# if __name__ == "__main__":
#   SardineLang.run(sys.argv[1:])