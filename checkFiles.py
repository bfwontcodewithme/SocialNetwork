a = 0

with open("student_output.txt", "rb") as f:
    a = f.read()

b = 0

with open("output.txt","rb") as f:
    b=f.read()

print(a[200:400])
print(b[200:400])
print(f'la = {len(a)}, lb = {len(b)}')