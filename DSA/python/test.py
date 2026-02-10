bits = [1,0,1,0,0]
one_bit = False

for i in range(len(bits)):
    print(i)
    if bits[i] == 1 and not one_bit:
        i += 1
    elif bits[i] == 0:
        one_bit = True

print(one_bit)
