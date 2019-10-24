import sys

N = input()
sum = 0
for digit in N:
    sum += int(digit)

inc = 3 - sum % 3

for i in range(len(N)):
    if int(N[i]) + inc <= 9:
        print("INC =", inc, ", i =", i, ", old =", N[i],  end=" ", file=sys.stderr)
        d = int(N[i]) + inc
        while d + 3 <= 9:
            d += 3
        N = N[:i] + str(d) + N[i + 1:]
        print(", new =", d, file=sys.stderr)
        print(N)
        break
else:
    d = int(N[-1])
    print("DEC =", inc, file=sys.stderr)
    if inc == 1:
        d -= 2
    elif inc == 2:
        d -= 1
    else:
        d -= 3
    N = N[:-1] + str(d)
    print(N)
