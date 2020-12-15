import z3
from real import *
import sys

def degree(poly):
  for i in range(len(poly) - 1, -1, -1):
    if poly[i] != 0:
      return i
  return 0

def match(a, b):
  if len(a) < len(b):
    return match(b, a)
  for i in range(len(a) - len(b)):
    b.append(0)
  return len(a)

def poly_add(a, b):
  n = match(a, b)
  c = [0] * n
  for i in range(n):
    c[i] = a[i] + b[i]
  return c

def poly_sub(a, b):
  return poly_add(a, [-x for x in b])

def poly_mul(a, b):
  da = degree(a)
  db = degree(b)
  c = [0] * (da + db + 1)
  for i in range(da + 1):
    for j in range(db + 1):
      c[i + j] = a[i] * b[j]
  return c

# borrowed from wikipedia (https://en.wikipedia.org/wiki/Polynomial_long_division)
def poly_div(n, d):
  match(n, d)
  dn = degree(n)
  dd = degree(d)
  q = [0] * dn
  r = n
  dr = degree(r)

  while dr >= 0 and dr >= dd:
    t = (dr - dd) * [0] + [r[dr] / d[dd]]
    q = poly_add(q, t)
    r = poly_sub(r, poly_mul(t, d))
    dr = degree(r)

  return q, r

x = z3.Real('x')

def make_expr(poly):
  def make_term(i):
    if poly[i] == 0:
      return None
    if i == 0:
      return poly[0]
    elif i == 1:
      return poly[1] * x
    else:
      return poly[i] * x ** i
  return sum([make_term(i) for i in range(len(poly)) if make_term(i) is not None])

def pretty(poly):
  def make_term(i):
    if poly[i] == 0:
      return None
    if i == 0:
      return str(poly[0])
    elif i == 1:
      return str(poly[1]) + 'x'
    else:
      return str(poly[i]) + 'x^' + str(i)
  return ' + '.join([make_term(i) for i in range(len(poly)) if make_term(i) is not None])

def irred(poly):
  if degree(poly) != 2:
    return False
  return poly[1] * poly[1] - 4 * poly[2] * poly[0] < 0

def main(source):
  poly = [int(x) for x in source.split()]
  roots = []

  print('solving 0 =', pretty(poly))

  while degree(poly) > 0 and not irred(poly):
    root = model_values(solve(make_expr(poly) == 0))['x']
    roots.append(root)
    poly, rem = poly_div(poly, [-float(root.as_decimal(20).strip('?')), 1])

  print('roots:', roots)
  if degree(poly) > 0:
    print('irreducible remainder:', pretty(poly))
    
if __name__ == '__main__':
  main(sys.stdin.read())
