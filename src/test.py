a = input()

a = a.split()
a = map(scalar,a)
a = list(a)
print(type(a))
print(a[1])
def scalar(fator, vetor = []):
    ret