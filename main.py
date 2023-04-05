def shift_left(value):
    result = value[1:]
    result.append("0")
    return result


def complement(value):
    result = []
    invert = False
    for i in reversed(value):
        if i == "0" and invert is False:
            result.append("0")
        elif i == "1" and invert is False:
            invert = True
            result.append("1")
        elif i == "1":
            result.append("0")
        else:
            result.append("1")
    result.reverse()
    return result


def list_addition(first_value, second_value, bits=8):
    summary = ["0" for _ in range(bits)]
    carry: int = 0
    for i in range(bits - 1, -1, -1):
        if first_value[i] == "0" and second_value[i] == "0" and carry == 0:
            summary[i] = "0"
            carry = 0
        elif first_value[i] == "0" and second_value[i] == "0" and carry == 1:
            summary[i] = "1"
            carry = 0
        elif first_value[i] == "0" and second_value[i] == "1" and carry == 0:
            summary[i] = "1"
            carry = 0
        elif first_value[i] == "0" and second_value[i] == "1" and carry == 1:
            summary[i] = "0"
            carry = 1
        elif first_value[i] == "1" and second_value[i] == "0" and carry == 0:
            summary[i] = "1"
            carry = 0
        elif first_value[i] == "1" and second_value[i] == "0" and carry == 1:
            summary[i] = "0"
            carry = 1
        elif first_value[i] == "1" and second_value[i] == "1" and carry == 0:
            summary[i] = "0"
            carry = 1
        elif first_value[i] == "1" and second_value[i] == "1" and carry == 1:
            summary[i] = "1"
            carry = 1
    return summary


def float_to_binary(value: float, bit_number: int = 16):
    if value < 0:
        minus_bit = "1"
        value *= -1
    else:
        minus_bit = "0"
    int_part = int(value)
    float_part: float = value - float(int_part)
    result: str = int_to_binary(int_part)[1:]
    if "1" not in result:
        result = minus_bit + "0."
    else:
        result = minus_bit + result[result.find("1"):] + "."
    for i in range(bit_number - len(result) - 1):
        float_part *= 2
        if int(float_part) == 0:
            result += "0"
        else:
            result += "1"
        float_part = float_part - float(int(float_part))
    return result


def to_decimal_value(binary_value: str) -> int:
    number: int = 0
    for i in range(1, len(binary_value)):
        number += 2 ** (len(binary_value) - 1 - i) * int(binary_value[i])
    if int(binary_value[0]) == 0:
        return number
    else:
        return -number


def binary_greater(first_value: str, second_value: str) -> bool:
    first_example, second_example = exponent(first_value), exponent(second_value)
    return first_example > second_example


def int_to_binary(value: int, bits: int = 16) -> str:
    result: str = ""
    if value < 0:
        minus_bit = "1"
        value *= -1
    else:
        minus_bit = "0"
    while value != 0:
        result = str(value % 2) + result
        value = value // 2
    result = minus_bit + result
    result = result[:1] + "0" * (bits - len(result)) + result[1:]
    return result


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


def division(dividend, divisor):
    if divisor == '0':
        raise Exception("Divisor cannot be zero.")
    else:
        dividend = get_binary(dividend)
        if len(dividend) < 8:
            dividend.reverse()
            for i in range(0, 8 - len(dividend)):
                dividend.append("0")
            dividend.reverse()
        divisor = get_binary(divisor)
        if len(divisor) < 8:
            divisor.reverse()
            for i in range(0, 8 - len(divisor)):
                divisor.append("0")
            divisor.reverse()
        bytes_values = ["0", "0", "0", "0", "0", "0", "0", "0"]
        first_value = divisor
        second_value = dividend
        for i in range(8):
            complemented_second_value = bytes_values + second_value
            temp_value = shift_left(complemented_second_value)
            bytes_values = temp_value[:8]
            second_value = temp_value[8:]
            bytes_values = list_addition(bytes_values, complement(first_value))
            if bytes_values[0] == "1":
                second_value[-1] = "0"
                bytes_values = list_addition(bytes_values, first_value)
            else:
                second_value[-1] = "1"
        return "".join(second_value)


def convert_to_floating_point(number: (int, float)):
    if number == 0:
        return ["0"] + list("01111111") + list("0" * 23)
    if number < 0:
        sign = "1"
    else:
        sign = "0"
    if isinstance(number, int):
        binary_number = int_to_binary(number)[1:]
        digit_order: int = len(binary_number) - (binary_number.find("1") + 1)
    else:
        binary_number = float_to_binary(number, bit_number=32)[1:]
        digit_order = binary_number.find(".") - (binary_number.find("1") + 1)
        if digit_order < 0:
            digit_order += 1
        else:
            digit_order += 0
        binary_number_list: list = list(binary_number)
        binary_number_list.pop(binary_number_list.index("."))
        binary_number = "".join(binary_number_list)
    exponent = addition_two(127, digit_order)
    exponent = exponent[8:]
    mantissa = list(binary_number[binary_number.find("1"):])
    if len(mantissa) < 23:
        mantissa += ["0" for _ in range(23 - len(mantissa))]
    else:
        mantissa = mantissa[:23]
    return [sign] + exponent + mantissa


def move_the_mantissa(mantissa: list, mantissa_moves: int):
    if mantissa_moves == 0:
        return mantissa
    return ["0" for _ in range(mantissa_moves)] + mantissa[:-mantissa_moves]


def mantissa_sum(floating_first,
                 floating_second):
    first_exp, second_exp = exponent(floating_first[1:9]), exponent(floating_second[1:9])
    if first_exp > second_exp:
        order = floating_first[1:9]
    elif first_exp < second_exp:
        order = floating_second[1:9]
    else:
        order = floating_second[1:9]
    new_mantissa = list_addition(floating_first[9:], floating_second[9:], bits=23)
    if new_mantissa[:2] == ['0', '0'] or new_mantissa[:2] == ["0", "1"]:
        order = list_addition(["0", "0"] + order, list("0000000001"), bits=10)
        order = order[2:]
        new_floating_point = [floating_first[0]] + order + new_mantissa
        return new_floating_point
    new_mantissa = new_mantissa[1:] + ["0"]
    new_floating_point = [floating_first[0]] + order + new_mantissa
    return new_floating_point


def equal(first_value, second_value):
    return first_value == second_value


def normalizing(floating_first, floating_second):
    first_ex, second_ex = exponent(floating_first[1:9]), exponent(floating_second[1:9])
    diff = int_to_binary(abs(first_ex - second_ex))
    if binary_greater(floating_first[1:9], floating_second[1:9]):
        floating_second[1:9] = list_addition(["0", "0", "0"] + floating_second[1:9], diff, bits=11)[3:]
        floating_second[9:] = move_the_mantissa(floating_second[9:], abs(first_ex - second_ex))
    else:
        floating_first[1:9] = list_addition(["0", "0", "0"] + floating_first[1:9], diff, bits=11)[3:]
        floating_first[9:] = move_the_mantissa(floating_first[9:], abs(first_ex - second_ex))
    return floating_first, floating_second


def exponent(value):
    result = 0
    for i in range(len(value)):
        if value[i] == "1":
            result += 2 ** (len(value) - 1 - i)
        else:
            continue
    return result


def addition_two(first_value, second_value, bits=16):
    result: list = []
    if first_value > 0 and second_value > 0:
        result = list_addition(to_straight_code(first_value), to_straight_code(second_value), bits=bits)
    elif first_value > 0 and second_value < 0:
        first_result, second_result = to_straight_code(first_value), to_straight_code(second_value)
        second_result = to_reverse_code(second_result)
        result = list_addition(first_result, second_result, bits=bits)
        if result[0] == "1":
            result = to_reverse_code(result)
    elif first_value < 0 and second_value > 0:
        first_result, second_result = to_straight_code(first_value), to_straight_code(second_value)
        first_result = to_reverse_code(first_result)
        result = list_addition(first_result, second_result, bits=bits)
        if result[0] == "1":
            result = to_reverse_code(result)
    elif first_value < 0 and second_value < 0:
        first_result, second_result = to_straight_code(first_value), to_straight_code(second_value)
        first_result, second_result = to_reverse_code(first_result), to_reverse_code(second_result)
        result = list_addition(first_result, second_result, bits=bits)
        if result[0] == "1":
            result = to_reverse_code(result)
    return result


def to_reverse_code(value: list):
    sign: str = [value[0]]
    result_list = ["0" for _ in range(len(value) - 1)]
    for index in range(len(value[1:])):
        if value[1:][index] == "0":
            result_list[index] = "1"
        elif value[1:][index] == "1":
            result_list[index] = "0"
    return list_addition(sign + result_list, to_straight_code(1), bits=16)


def multiplication(first_num, sec_num):
    answer = ["0" for _ in range(16)]
    if (first_num < 0) or (sec_num < 0):
        answer[0] = '1'
    if (first_num < 0) and (sec_num < 0):
        answer[0] = '0'
    first_num, sec_num = abs(int(first_num)), abs(int(sec_num))
    if abs(first_num * sec_num) > 32767:
        raise Exception("You are out of range")
    else:
        len_array = len(convert(sec_num))
        first_num, sec_num = to_straight_code(first_num), to_straight_code(sec_num)
        for i in range(len_array):
            additional_array = ['0' for i in range(16)]
            overload = 0
            for index in range(15):
                index = 15 - index
                additional_array[index] = int(sec_num[15 - i]) * int(first_num[index])
                first_additional_value, second_additional_value = int(answer[index - i]), int(additional_array[index])
                if first_additional_value + second_additional_value + overload < 2:
                    answer[index - i] = str(first_additional_value + second_additional_value + overload)
                    overload = 0
                elif first_additional_value + second_additional_value + overload == 2:
                    answer[index - i] = '0'
                    overload = 1
                else:
                    answer[index - i] = '1'
                    overload = 1
        return "".join(answer)


def convert(n, base_system=2, head_system=10):
    value = '0123456789'
    if isinstance(n, str):
        n = float(n, head_system)
    if n >= base_system:
        return convert(n // base_system, base_system) + value[n % base_system]
    else:
        return value[n]


def to_straight_code(number, bits=16):
    str_code = ["0" for i in range(bits)]
    if number < 0:
        number = abs(number)
        str_code[0] = "1"
    number = list(str(convert(number)))
    for item in range(len(number)):
        str_code[len(str_code) - (item + 1)] = number[len(number) - (item + 1)]
    return str_code


def test_addition(x, y) -> None:
    print("Addition")
    addition_two(x, y)


def test_subtraction(x, y) -> None:
    print("Subtraction")
    addition_two(x, -y)


def test_multiplication(x, y) -> None:
    print("Multiplication")
    result = multiplication(x, y)
    print(result)
    print(to_decimal_value(result))


def test_division(x, y) -> None:
    print("Division")
    result = (division(str(x), str(y)))
    print(division(str(x), str(y)))
    print(to_decimal_value(result))


def test_floating_point_addition(x, y) -> None:
    print("Floating point")
    floating_first = convert_to_floating_point(x)
    floating_second = convert_to_floating_point(y)
    floating_first, floating_second = normalizing(floating_first, floating_second)
    new_floating_point = mantissa_sum(floating_first, floating_second)
    print(new_floating_point)


test_addition(6, -12)
test_subtraction(3, 7)
test_multiplication(11, 21)
test_division(25, 7)
test_floating_point_addition(0.5, 5.5)
