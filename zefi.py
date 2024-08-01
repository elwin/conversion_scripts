def how_much_water(height):
    water = 0

    for i in range(max(height) + 1):  # 0, 1, 2, 3

        seen_left_stone = False
        current_water = 0
        for current_height in height:  # 0
            if current_height > i:
                seen_left_stone = True
                water += current_water
                current_water = 0

            if seen_left_stone and current_height <= i:
                current_water += 1

    return water


def how_much_water_faster(height):
    left = get_max_vector(height)
    right = list(reversed(get_max_vector(reversed(height))))
    min_vec = get_min_of_two(left, right)
    water_vec = subtract(min_vec, height)  # todo: abs?

    return sum(water_vec)


def get_max_vector(height):
    max_height = 0
    out = []
    for cur_height in height:
        max_height = max(max_height, cur_height)
        out.append(max_height)

    return out


# a - b
def subtract(a, b):
    out = []
    for i, _ in enumerate(a):
        out.append(a[i] - b[i])

    return out


def get_min_of_two(a, b):
    out = []
    for i, _ in enumerate(a):
        out.append(min(a[i], b[i]))

    return out


def main():
    waters = [
        [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],
        [4, 2, 0, 3, 2, 5],
        [0, 1, 0, 1, 0],
        [0, 0, 0],
        [1, 1, 1],
        [0, 2, 0],
    ]
    for height in waters:
        print(how_much_water(height), how_much_water_faster(height))


if __name__ == '__main__':
    main()
