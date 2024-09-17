from time import perf_counter

def bin64_to_str(bin64):
    return str(bin(bin64))[2:].zfill(64)

def bsf(bin64):
    s = bin64_to_str(bin64)
    for idx in range(64):
        if s[idx] == "1":
            return idx
    return None

def bsr(bin64):
    s = bin64_to_str(bin64)
    for idx in range(63, -1, -1):
        if s[idx] == "1":
            return idx
    return None

def mffs(x):
    """Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
    return 63 - ((x&-x).bit_length()-1)

def mffsr(x):
    return 63 - (x.bit_length() - 1)

n = 71776119061217280
N = 10000

print("\nBIT SCAN REVERSE\n")
stime = perf_counter()
print(bsr(n))
for _ in range(N):
    _ = bsr(n)
print(t1 := (perf_counter() - stime) / N)

stime = perf_counter()
print(mffs(n))
for _ in range(N):
    _ = mffs(n)
print(t2 := (perf_counter() - stime) / N)
print(t1 / t2)

print("\nBIT SCAN FORWARD\n")
stime = perf_counter()
print(bsf(n))
for _ in range(N):
    _ = bsf(n)
print(t1 := (perf_counter() - stime) / N)

stime = perf_counter()
print(mffsr(n))
for _ in range(N):
    _ = mffsr(n)
print(t2 := (perf_counter() - stime) / N)
print(t1 / t2)