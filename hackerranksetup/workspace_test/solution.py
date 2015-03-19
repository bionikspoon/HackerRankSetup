# coding=utf-8
def main():
    n = int(input())
    for _ in xrange(n):
        a, b = map(int, raw_input().split())
        result = a + b
        print result


if __name__ == "__main__":
    main()
