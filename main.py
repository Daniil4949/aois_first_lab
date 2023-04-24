def moving_to_the_left(value):
    moving_value = value[1:]
    moving_value.append("0")
    return moving_value


def complementation(x):
    value = []
    flag = False
    for i in reversed(x):
        if i == "0" and not flag:
            value.append("0")
        elif i == "1" and not flag:
            flag = True
            value.append("1")
        elif i == "1":
            value.append("0")
        else:
            value.append("1")
    value.reverse()
    return value


def sum_with_lists(x, y, value_of_bits=8):
    summary = ["0" for _ in range(value_of_bits)]
    carry: int = 0
    for i in range(value_of_bits - 1, -1, -1):
        if x[i] == "0" and y[i] == "0" and carry == 0:
            summary[i] = "0"
            carry = 0
        elif x[i] == "0" and y[i] == "0" and carry == 1:
            summary[i] = "1"
            carry = 0
        elif x[i] == "0" and y[i] == "1" and carry == 0:
            summary[i] = "1"
            carry = 0
        elif x[i] == "0" and y[i] == "1" and carry == 1:
            summary[i] = "0"
            carry = 1
        elif x[i] == "1" and y[i] == "0" and carry == 0:
            summary[i] = "1"
            carry = 0
        elif x[i] == "1" and y[i] == "0" and carry == 1:
            summary[i] = "0"
            carry = 1
        elif x[i] == "1" and y[i] == "1" and carry == 0:
            summary[i] = "0"
            carry = 1
        elif x[i] == "1" and y[i] == "1" and carry == 1:
            summary[i] = "1"
            carry = 1
    return summary


def float_to_binary(x: float, n: int = 16):
    if x < 0:
        bit = "1"
        x *= -1
    else:
        bit = "0"
    int_ = int(x)
    float_res: float = x - float(int_)
    val: str = convert_from_number(int_)[1:]
    if "1" not in val:
        val = bit + "0."
    else:
        val = bit + val[val.find("1"):] + "."
    return get_float_part(val, float_res, n)


def get_float_part(res, float_res, val):
    for i in range(val - len(res) - 1):
        float_res *= 2
        if int(float_res) == 0:
            res += "0"
        else:
            res += "1"
        float_res = float_res - float(int(float_res))
    return res


def convert_to_number_format(x: str) -> int:
    val: int = 0
    for i in range(1, len(x)):
        val += 2 ** (len(x) - 1 - i) * int(x[i])
    if int(x[0]) == 0:
        return val
    else:
        return -val


def compare(x: str, y: str) -> bool:
    comp_x, comp_y = exponent(x), exponent(y)
    return comp_x > comp_y


def convert_from_number(result_val: int, n: int = 16) -> str:
    val: str = ""
    if result_val < 0:
        bit = "1"
        result_val *= -1
    else:
        bit = "0"
    while result_val != 0:
        val = str(result_val % 2) + val
        result_val = result_val // 2
    return make_full_number(val, bit, n)


def make_full_number(x, flag, val):
    x = flag + x
    x = x[:1] + "0" * (val - len(x)) + x[1:]
    return x


def get_binary(value_str):
    parts = value_str.split('.')
    int_part = int(parts[0])
    bin_int_part = []
    if int_part == 0:
        bin_int_part.append('0')
    if int_part != 0:
        while int_part != 0:
            bin_int_part.append(str(int_part % 2))
            int_part = int(int_part / 2)
        bin_int_part.reverse()
    return bin_int_part


def div(x, y):
    if y == '0':
        raise Exception("Divisor cannot be zero.")
    else:
        x = get_binary(x)
        if len(x) < 8:
            x.reverse()
            for i in range(0, 8 - len(x)):
                x.append("0")
            x.reverse()
        y = get_binary(y)
        if len(y) < 8:
            y.reverse()
            for i in range(0, 8 - len(y)):
                y.append("0")
            y.reverse()
        bytes_values = ["0", "0", "0", "0", "0", "0", "0", "0"]
        first_value = y
        second_value = x
        return dividing(first_value, second_value, bytes_values)


def dividing(x, y, n):
    for i in range(8):
        complemented_second_value = n + y
        temp_value = moving_to_the_left(complemented_second_value)
        n = temp_value[:8]
        y = temp_value[8:]
        n = sum_with_lists(n, complementation(x))
        if n[0] == "1":
            y[-1] = "0"
            n = sum_with_lists(n, x)
        else:
            y[-1] = "1"
    return "".join(y)


def float_(x: (int, float)):
    if x < 0:
        sign = "1"
    else:
        sign = "0"
    if isinstance(x, int):
        bin_ = convert_from_number(x)[1:]
        factor: int = len(bin_) - (bin_.find("1") + 1)
    else:
        bin_ = float_to_binary(x, n=32)[1:]
        factor = bin_.find(".") - (bin_.find("1") + 1)
        if factor < 0:
            factor += 1
        else:
            factor += 0
        list_bin_: list = list(bin_)
        list_bin_.pop(list_bin_.index("."))
        bin_ = "".join(list_bin_)
    return creating_float(bin_, factor, sign)


def creating_float(bin_, factor, flag):
    exponent_ = sum_of_two_values(127, factor)[8:]
    if factor == 0:
        exponent_ = ["0", "1", "1", "1", "1", "1", "1", "1"]
    m = list(bin_[bin_.find("1"):])
    if len(m) < 23:
        m += ["0" for _ in range(23 - len(m))]
    else:
        m = m[:23]
    return [flag] + exponent_ + m


def changing(m: list, n: int):
    return m if n == 0 else ["0" for _ in range(n)] + m[:-n]


def result_floating_point(x,
                          y):
    x_exp, y_exp = exponent(x[1:9]), exponent(y[1:9])
    if x_exp > y_exp:
        order = x[1:9]
    elif x_exp < y_exp:
        order = y[1:9]
    else:
        order = y[1:9]
    created_m = sum_with_lists(x[9:], y[9:], value_of_bits=23)
    if created_m[:2] == ['0', '0'] or created_m[:2] == ["0", "1"]:
        return overflow(created_m, order, x)
    created_m = created_m[1:] + ["0"]
    created_float = [x[0]] + order + created_m
    return created_float


def overflow(new_m, order, floating_first):
    order = sum_with_lists(["0", "0"] + order, list("0000000001"), value_of_bits=10)
    order = order[2:]
    new_float = [floating_first[0]] + order + new_m
    return new_float


def equal(first_value, second_value):
    return first_value == second_value


def alignment(x, y):
    ex_1, ex_2 = exponent(x[1:9]), exponent(y[1:9])
    diff = convert_from_number(abs(ex_1 - ex_2))
    if compare(x[1:9], y[1:9]):
        y[1:9] = sum_with_lists(["0", "0", "0"] + y[1:9], diff, value_of_bits=11)[3:]
        y[9:] = changing(y[9:], abs(ex_1 - ex_2))
    else:
        x[1:9] = sum_with_lists(["0", "0", "0"] + x[1:9], diff, value_of_bits=11)[3:]
        x[9:] = changing(x[9:], abs(ex_1 - ex_2))
    return x, y


def exponent(value):
    result = 0
    for i in range(len(value)):
        if value[i] == "1":
            result += 2 ** (len(value) - 1 - i)
        else:
            continue
    return result


def sum_of_two_values(x, y, n=16):
    val: list = []
    if x > 0 and y > 0:
        val = sum_with_lists(straight(x), straight(y), value_of_bits=n)
    elif x > 0 and y < 0:
        val = negative_second_addition(x, y, n)
    elif x < 0 and y > 0:
        val = negative_first_addition(x, y, n)
    elif x < 0 and y < 0:
        val = negative_addition(x, y, n)
    return val


def negative_addition(x, y, n):
    x, y = straight(x), straight(y)
    x, y = rev(x), rev(y)
    val = sum_with_lists(x, y, value_of_bits=n)
    if val[0] == "1":
        val = rev(val)
    return val


def negative_first_addition(x, y, n):
    x, y = straight(x), straight(y)
    x = rev(x)
    val = sum_with_lists(x, y, value_of_bits=n)
    if val[0] == "1":
        val = rev(val)
    return val


def negative_second_addition(x, y, n):
    x, y = straight(x), straight(y)
    y = rev(y)
    val = sum_with_lists(x, y, value_of_bits=n)
    if val[0] == "1":
        val = rev(val)
    return val


def rev(x: list):
    flag: str = [x[0]]
    val = ["0" for _ in range(len(x) - 1)]
    for index in range(len(x[1:])):
        if x[1:][index] == "0":
            val[index] = "1"
        elif x[1:][index] == "1":
            val[index] = "0"
    return sum_with_lists(flag + val, straight(1), value_of_bits=16)


def multiplication(x, y):
    res = ["0" for _ in range(16)]
    if (x < 0) or (y < 0):
        res[0] = '1'
    if (x < 0) and (y < 0):
        res[0] = '0'
    x, y = abs(int(x)), abs(int(y))
    if abs(x * y) > 32767:
        raise Exception("You are out of range")
    else:
        len_ = len(convert(y))
        x, y = straight(x), straight(y)
        for i in range(len_):
            additional_array = ['0' for i in range(16)]
            overload = 0
            for index in range(15):
                index = 15 - index
                additional_array[index] = int(y[15 - i]) * int(x[index])
                first_additional_value, second_additional_value = int(res[index - i]), int(additional_array[index])
                if first_additional_value + second_additional_value + overload < 2:
                    res[index - i] = str(first_additional_value + second_additional_value + overload)
                    overload = 0
                elif first_additional_value + second_additional_value + overload == 2:
                    res[index - i] = '0'
                    overload = 1
                else:
                    res[index - i] = '1'
                    overload = 1
        return "".join(res)


def convert(n, base_system=2, head_system=10):
    value = '0123456789'
    if isinstance(n, str):
        n = float(n, head_system)
    if n >= base_system:
        return convert(n // base_system, base_system) + value[n % base_system]
    else:
        return value[n]


def straight(x, n=16):
    str_code = ["0" for _ in range(n)]
    if x < 0:
        x = abs(x)
        str_code[0] = "1"
    x = list(str(convert(x)))
    for item in range(len(x)):
        str_code[len(str_code) - (item + 1)] = x[len(x) - (item + 1)]
    return str_code


def main():
    print("Enter first int value")
    x = int(input())
    print("Enter second int value")
    y = int(input())
    print("Addition")
    val = sum_of_two_values(x, y)
    print(convert_to_number_format("".join(val)))
    print("Subtraction")
    val = sum_of_two_values(x, -y)
    print(convert_to_number_format("".join(val)))
    print("Multiplication")
    val = multiplication(x, y)
    print(val)
    print(convert_to_number_format(val))
    print("Division")
    val = (div(str(x), str(y)))
    print(div(str(x), str(y)))
    print(convert_to_number_format(val))
    print("Floating point")
    print("Enter first float value")
    x = float(input())
    print("Enter second float value")
    y = float(input())
    x = float_(x)
    y = float_(y)
    x, y = alignment(x, y)
    new_floating_point = result_floating_point(x, y)
    print(new_floating_point)


if __name__ == "__main__":
    main()
