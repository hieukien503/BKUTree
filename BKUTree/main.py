from BKUTree import *

def func(key: K, value: V):
    print(f"<{key}, {value}>", end = ' ')

def main():
    bkuTree = BKUTree(5)
    for i in range(10):
        bkuTree.add(i, 3 * i + 10)

if __name__ == '__main__':
    main()
