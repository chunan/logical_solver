from logic_solver import *

def e1(get):
  return True

def e2(get):
  a1, a2 = [get(i - 1) for i in (1, 2)]
  return WithFalseMessage(PossiblyNe((a1, a2)))

def e3(get):
  a3 = get(2)
  return WithFalseMessage(PossiblyNe((a3, A)))

def test():
  solver = Solver([e1, e2, e3], num_options=2)
  solver.solve()


if __name__ == '__main__':
  test()
