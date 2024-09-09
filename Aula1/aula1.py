from z3 import *

# initializations
survey, lic, ABtesting, statistics, qa, adv_lic, basic_lic, basic_qa, multimedia_qa = Bools('survey lic ABtesting statistics qa adv_lic basic_lic basic_qa multimedia_qa')

features = [survey, lic, ABtesting, statistics, qa, adv_lic, basic_lic, basic_qa, multimedia_qa]


s = Solver()

# constraints

s.add(survey)

s.add(survey == lic)

s.add(Implies(ABtesting, survey))

s.add(Implies(statistics, survey))

s.add(survey == qa)

s.add(Implies(ABtesting, statistics))

s.add(Not(And(ABtesting, basic_lic)))

s.add(Or(adv_lic, basic_lic) == lic)
s.add(Not(And(adv_lic, basic_lic)))

s.add(Or(basic_qa, multimedia_qa) == qa)

s.add(Not(And(basic_lic, multimedia_qa)))

# 1)
print("\nEx1: Void or Non Void")
if s.check() == sat:
    print("non void")
else:
    print("void")


# 2)
print("\nEx2: How many variants exists?")
s.push()
i = 0
while s.check() == sat:
    i += 1
    m = s.model()
    p = []
    for f in features:
        if is_true(m[f]):
            p.append(f)
            #print(f.decl().name(),end=" ")
        else:
            p.append(Not(f))
    s.add(Not(And(p)))
print("There are " + str(i) + " possible products!")
s.pop()

# 3)
print("\nEx3: If AB testing was mandatory what would be the core features?")
s.push()
s.add(survey == ABtesting)

for f in features:
  s.push()
  s.add(Not(f))
  if s.check() == unsat:
    print("Feature " + f.decl().name() + " is core!")
  s.pop()
  
s.pop()

# 4)

print("\nEx4: If AB testing was mandatory what would be the dead features?")
s.push()
s.add(Implies(basic_qa, ABtesting))

for f in features:
  s.push()
  s.add(f)
  if s.check() == unsat:
    print("Feature " + f.decl().name() + " is dead!")
  s.pop()
  
s.pop()
