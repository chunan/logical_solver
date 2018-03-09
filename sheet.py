from logic_solver import *

def q1(get):
  return True


def q2(get):
  a2 = get(1)  # Please note that get is 0-based
  a5 = get(4)
  if a2 == 0 or a5 == 0:
    return True
  return WithFalseMessage((a2, a5) in [(A, C), (B, D), (C, A), (D, B)])


def q3(get):
  # Warning: we assume the order of filling is 1, ..., 10.
  a2, a3, a4, a6 = [get(i - 1) for i in (2, 3, 4, 6)]

  if a3 == 0:
    return True
  if a3 == A:
    return WithFalseMessage(a4 in (0, a2) and a6 in (0, a2))
  elif a3 == B:
    return WithFalseMessage(a2 == B and a4 in (0, B) and a6 in (0, A, C, D))
  elif a3 == C:
    return WithFalseMessage(a2 != C and a4 in (0, C) and a6 in (0, C))
  else:
    return WithFalseMessage(a2 == D and a4 in (0, A, B, C) and a6 in (0, D))
  

def q4(get):
  a1, a2, a4, a5, a6, a7, a9, a10 = [get(i - 1) for i in (1, 2, 4, 5, 6, 7, 9, 10)]

  if a4 == 0:
    return True

  pairs = [(a1, a5), (a2, a7), (a1, a9), (a6, a10)]

  possibly_correct = [PossiblyNe(p) for p in pairs]
  possibly_correct[a4 - 1] = PossiblyEq(pairs[a4 - 1])
  return WithFalseMessage(ReduceAnd(possibly_correct))


def q5(get):
  a4, a5, a7, a8, a9 = [get(i - 1) for i in (4, 5, 7, 8, 9)]
  if a5 == 0:
    return True
  targets = [a8, a4, a9, a7]
  possibly_correct = [PossiblyNe((a5, x)) for x in targets]
  possibly_correct[a5 - 1] = PossiblyEq((a5, targets[a5 - 1]))
  return WithFalseMessage(ReduceAnd(possibly_correct))


def q6(get):
  a2, a4, a1, a6, a3, a10, a5, a9, a8 = [get(i - 1) for i in (2, 4, 1, 6, 3, 10, 5, 9, 8)]
  if a6 == 0:
    return True
  pairs = [[a2, a4], [a1, a6], [a3, a10], [a5, a9]]
  possibly_correct = [PossiblyNe(p + [a8]) for p in pairs]
  possibly_correct[a6 - 1] = PossiblyEq(pairs[a6 - 1] + [a8])
  return WithFalseMessage(ReduceAnd(possibly_correct))


def q7(get):
  ans = [get(i) for i in range(10)]
  if ans[-1] == 0:
    return True

  count = [0] * 5
  for a in ans:
    count[a] += 1
  argmin = numpy.argmin(count[1:]) + 1
  a7 = ans[6]
  choices = {A: C, B: B, C: A, D: D}
  return WithFalseMessage(choices[a7] == argmin)


def q8(get):
  a8, a1, a7, a5, a2, a10 = [get(i - 1) for i in (8, 1, 7, 5, 2, 10)]
  if a8 == 0:
    return True

  def PossiblyA1Neighbor(x):
    if x == 0:
      return True
    return x in (a1 + 1, a1 - 1)

  def PossiblyNotA1Neighbor(x):
    if x == 0:
      return True
    return x not in (a1 + 1, a1 - 1)

  choices = (a7, a5, a2, a10)
  possibly_correct = [PossiblyA1Neighbor(a) for a in choices]
  possibly_correct[a8 - 1] = PossiblyNotA1Neighbor(choices[a8 - 1])
  return WithFalseMessage(ReduceAnd(possibly_correct))


def q9(get):
  a9, a1, a6, a5, a10, a2 = [get(i - 1) for i in (9, 1, 6, 5, 10, 2)]
  if a10 == 0:
    return True
  choices = {A: a6, B: a10, C: a2, D: a9}
  x = choices[a9]
  return WithFalseMessage((a1 == a6) != (x == a5))


def q10(get):
  ans = [get(i) for i in range(10)]
  if ans[-1] == 0:
    return True
  count = [0] * 5
  for a in ans:
    count[a] += 1
  del count[0]
  m = min(count)
  M = max(count)
  a10 = ans[9]
  choices = {A: 3, B: 2, C: 4, D: 1}
  return WithFalseMessage(M - m == choices[a10])



def main():
  solver = Solver([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                  num_options=4)
  solver.solve()


if __name__ == '__main__':
  main()
