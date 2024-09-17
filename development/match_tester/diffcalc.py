from sys import argv

try:

    with open("testlogs/" + argv[1]) as f:
        nums1 = list(map(int, f.read().splitlines()))

    with open("testlogs/" + argv[2]) as f:
        nums2 = list(map(int, f.read().splitlines()))

    diffs = [(j - i) / i * 100 for i, j in zip(nums1, nums2)]
    print(f"Node reduction: {sum(diffs)/len(diffs):.2f}%")

except IndexError:
    print("not enough arguments")

except FileNotFoundError:
    print("file does not exist")