chars = [chr(c) for c in range(ord('a'), ord('z')+1)]
chars += [str(d) for d in range(0, 10)]

with open("test.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(chars))

