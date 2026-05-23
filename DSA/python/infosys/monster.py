def solution(monsters: int, exp: int, power: list, bonus: list):
    a = sorted(zip(power, bonus))
    count = 0

    for p,b in a:
        print(p, " ", b)
        if exp>=p:
            count += 1
            exp += b
        else:
            break

    return count


if __name__ == "__main__":
    n = int(input())
    exp = int(input())
    power = [int(input()) for _ in range(n)]
    bonus = [int(input()) for _ in range(n)]

    print(solution(n, exp, power, bonus))
