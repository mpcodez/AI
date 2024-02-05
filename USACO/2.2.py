def solve_test_case(N, cows):
    hay_count = {}
    for hay in cows:
        if hay not in hay_count:
            hay_count[hay] = 1
        else:
            hay_count[hay] += 1

    half_threshold = (N // 2) + 1
    possible_hays = []
    for hay, count in hay_count.items():
        if count >= half_threshold:
            possible_hays.append(hay)

    if len(possible_hays) == 0:
        return [-1]
    else:
        return sorted(possible_hays)

def main():
    T = int(input().strip())

    for _ in range(T):
        N = int(input().strip())
        cows = list(map(int, input().strip().split()))
        result = solve_test_case(N, cows)
        print("=========>", " ".join(map(str, result)))

if __name__ == "__main__":
    main()
