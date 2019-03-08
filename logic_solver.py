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
  """Finds variable values that satisfies all predicates.
  
  Given a set a variables X = (X1, X2, ..., Xn), each of which \in 
  {1, 2, ..., K} and a list of predicates P = (P1, P2, ..., Pm} where
  each Pi evaluates the truth value given X. Find all possible X's that
  satisfy P. Note that we assume n == m (num_predicates) and K = num_options.
  
  Predicates are implemented as function that takes a getter, which returns
  the value given the index of X. E.g.:
  
  def predicate1(getter):
    # Returns True if X1 == X2.
    return getter(0) == getter(1)  # Note that getter are 0-based.
    
  self.dependent is a map from predicate to indices in X indicating that
  the predicate only dependents on these indices in X. The dependency is
  evaluated by running the predicate, so the predicate function should
  have all its dependencies called before any condition clause. E.g.
  
  def predicate2(getter):
    # Returns True if X1 == X2 == X3.
    x1, x2, x3 = [getter(i) for i in (0, 1, 2)]
    return x1 == x2 and x2 == x3
  
  But not as follows:
  
  def bad_predicate2(getter):
    if getter(0) != getter(1) or getter(1) != getter(2):
      return False
    return True
  """

  def __init__(self, predicates, num_options):
    """Constructor.
    
    Args:
      predicates: (list of func(getter)->bool), each of which returns False when 
        the partial set of values (obatined via getter) violates the predicate,
        or return True otherwise.
      num_options: (int) number of possible values for each variable.
    """
    self.num_predicates = len(predicates)
    self.predicates = predicates[:]
    self.answers = [0] * self.num_predicates
    self.num_options = num_options
    self.dependent = [set() for _ in range(self.num_predicates)]
    self.letter = [' '] + [chr(65 + i) for i in range(self.num_options)] + ['$']

    for i, pred in enumerate(predicates):
      pred(functools.partial(self.add_dependent, i))

    print('Dependencies:')
    for i, dep in enumerate(self.dependent):
      print(' {}: {}'.format(i, dep))

  def add_dependent(self, predicate_index, value_index):
    """Special function to create dependent dict."""
    self.dependent[value_index].add(self.predicates[predicate_index])
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
