from abc import ABCMeta, abstractproperty

class Error(metaclass=ABCMeta):
  @abstractproperty
  def type(self):
    raise NotImplementedError
  
  @abstractproperty
  def line(self):
    raise NotImplementedError

  @abstractproperty
  def token(self):
    raise NotImplementedError

  @abstractproperty
  def message(self):
    raise NotImplementedError


class SardineSyntaxError(Error):
  type, line, token, message = None, None, None, None
  def __init__(self, type, line, raw_token, message=''):
    self.type = type
    self.line = line
    self.token = raw_token
    self.message = message


def error(e):
    print(e.type + ": " + "One line " + str(e.line) + ", at '" + e.token + "'. " + e.message)



class ReturnInterrupt(Exception):
  def __init__(self, value, *args, **kwargs):
    super(Exception, self).__init__(*args, **kwargs)
    self.value = value


if __name__ == "__main__":
  e = SardineSyntaxError("SyntaxError", 1, '')
  print(e.type)