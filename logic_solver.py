import functools
import inspect
import numpy
import operator


A, B, C, D = 1, 2, 3, 4

# Helpers.

def WithFalseMessage(value):
  if not value:
    print('[Fail] {}'.format(inspect.stack()[1][3]))
  return value 


def PredicatesReduceAnd(predicates, getter):
  for pred in predicates:
    if not pred(getter):
      return False
  return True


def ReduceAnd(xs):
  return functools.reduce(lambda x, y: x and y, xs)


def ReduceOr(xs):
  return functools.reduce(lambda x, y: x or y, xs)


def PossiblyNe(xs):
  if len(xs) < 2:
    return False
  m = min(xs)
  M = max(xs)
  if m < M:
    return True
  if m == 0:
    return True
  return False


def PossiblyEq(xs):
  values = set(xs)
  values.discard(0)
  return len(values) == 1


class Solver(object):

  def __init__(self, predicates, num_options):
    self.num_predicates = len(predicates)
    self.predicates = predicates[:]
    self.answers = [0] * self.num_predicates
    self.num_options = num_options
    self.dependent = [[] for _ in range(self.num_predicates)]
    self.letter = [' '] + [chr(65 + i) for i in range(self.num_options)] + ['$']

    for i, pred in enumerate(predicates):
      pred(functools.partial(self.add_dependent, i))

    print('Dependencies:')
    for i, dep in enumerate(self.dependent):
      print(' {}: {}'.format(i, dep))

  def add_dependent(self, predicate_index, value_index):
    """Special function to create dependent dict."""
    self.dependent[value_index].append(self.predicates[predicate_index])
    return 0
 
  def get(self, value_index):
    return self.answers[value_index]

  def pretty_answers(self):
    return [self.letter[a] for a in self.answers]

  def solve(self):
    solutions = []
    value_index = 0
    while value_index >= 0:
      # Reach the bottom of the tree.
      if value_index >= self.num_predicates:
        solutions.append(self.pretty_answers())
        print('[SOLVED] answer={}'.format(self.pretty_answers()))
        value_index -= 1
        continue
      self.answers[value_index] += 1
      # All subtrees finished, back to previous level.
      if self.answers[value_index] > self.num_options:
        print('{} <<'.format(self.pretty_answers()))
        self.answers[value_index] = 0  # Reset values.
        value_index -= 1
        continue
      # Violate predicate, continue.
      if not PredicatesReduceAnd(self.dependent[value_index], self.get):
        print('{} SKIP'.format(self.pretty_answers()))
        continue
      print('{} >>'.format(self.pretty_answers()))
      value_index += 1

    print('Answers:')
    for i, ans in enumerate(solutions):
      print(' {}: {}'.format(i, ans))
    return solutions
