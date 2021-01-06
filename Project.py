class Converter:
    def __init__(self, number):
        # I declared  the important variables here.
        self.number = number
        self.decimal_rep = None
        self.binary_rep = None
        self.dict1 = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
        self.main()

    def signed_transform(self):
        pass

    # To understand whether the floating point number denormalized or not.
    def is_denormalized(self, exponent):
        sum = 0
        for i in exponent:
            sum += int(i)
        if sum == 0:
            return True
        else:
            return False

    # To make it more organized I wrote this as a separate function.
    def calculate_mantissa_sum(self, mantissa):
        mantissa_sum = 0.0
        counter = -1
        for i in mantissa:
            holder = int(i) * (2 ** counter)
            mantissa_sum += holder
            counter -= 1
        return mantissa_sum

    # This is for converting decimal to binary.
    def decimal_to_binary(self, decimal):
        storage = ""
        counter = 0
        while True:
            if counter > 32:
                break
            reminder = int(decimal) % 2
            decimal = decimal / 2
            storage = storage + str(reminder)
            counter += 1
        return self.cleaner(storage[::-1])

    def cleaner(self, string):
        counter = 0
        for i in string:
            if i == "0":
                counter += 1
            else:
                return string[counter:]

    # This is a function that I used to execute right functions in the right moment.
    def converter(self, hex_number, type="0"):
        byte_num = int(len(hex_number))//2
        decimal_number = self.to_decimal(hex_number, 16, type)
        binary_number = self.decimal_to_binary(decimal_number)
        zero_num = "0" * (8*byte_num - len(binary_number))
        integer_32bit = zero_num + binary_number
        if type == "s":
            return self.to_decimal(integer_32bit, 2, "s")
        elif type == "u":
            return self.to_decimal(integer_32bit, 2, "u")
        elif type == "f":
            return self.floating_point_rep(integer_32bit, byte_num)
        else:
            print("You did something wrong!")

    # This function is for special situations.
    def special_sit(self, exponent, mantissa, sign):
        if exponent == "1" * len(exponent):
            if mantissa == "0" * len(mantissa):
                if sign == "1":
                    return "-oo"
                elif sign == "0":
                    return "+oo"
            else:
                return "NaN"
        if exponent == "0" * len(exponent):
            if mantissa == "0" * len(mantissa):
                if sign == "1":
                    return "-0"
                elif sign == "0":
                    return "+0"
        return exponent

     # I wrote this function to take second complement.
    def second_complement(self, binary_number):
        new_string = ""
        for i in binary_number:
            new_string += str(1 - int(i))

        storage = ""
        for i in range(1, len(new_string) + 1):
            holder = new_string[i * -1]
            if holder == "1":
                storage += "0"
            elif holder == "0":
                storage += "1"
                for j in range(i + 1, len(new_string) + 1):
                    storage += new_string[j * -1]
                break
        return storage[::-1]

    # This is the rounding function.
    def round(self, fraction):
        last_digit = "0"
        if len (fraction) < 14:
            return fraction

        if fraction[12] == "0":
            if fraction[13] == "0":
                holder = list(fraction)
                holder[12] = last_digit
                fraction = "".join(holder[:13])
                return fraction
            elif fraction[13] == "1":
                for i in range(13, len(fraction)):
                    if fraction[i] == "1":
                        last_digit = "1"
                        break
                holder = list(fraction)
                holder[12] = last_digit
                fraction = "".join(holder[:13])
                return fraction

            if fraction[12] == "1":
                if fraction[13] == "0":
                    fraction[12] = last_digit
                    return fraction
                elif fraction[13] == "1":
                    for i in range(13, len(fraction)):
                        if fraction[i] == "1":
                            last_digit = "1"
                            break
                    fraction[12] = last_digit
                    return fraction

    # This executes when a hex number converting to a floating point number.
    def floating_point_rep(self, binary, byte):
        exponent = 0
        if byte == 1:
            exponent = 4
        elif byte == 2:
            exponent = 6
        elif byte == 3:
            exponent = 8
        elif byte == 4:
            exponent = 8

        sign_bit = binary[0]
        bias = 2 ** (exponent - 1) - 1
        exponent_part = binary[1: (exponent) + 1]
        mantissa = binary[(exponent) + 1:]
        mantissa = self.round(mantissa)
        denormalized = self.is_denormalized(exponent_part)
        mantissa_sum = self.calculate_mantissa_sum(mantissa)
        # The part when we see if it is denormalized or normalized.
        if denormalized:
            e = 1 - bias
            decimal_rep = ((-1) ** float(sign_bit)) * (float(mantissa_sum)) * (2 ** (e))
        else:
            e = int(self.to_decimal(exponent_part, 2)) - bias
            decimal_rep = ((-1) ** float(sign_bit)) * (1 + float(mantissa_sum)) * (2 ** e)

        special_result = self.special_sit(exponent_part, mantissa, sign_bit)
        if special_result != exponent_part:
            decimal_rep = special_result

        return "%.5g" % decimal_rep

    # This will convert a hex or binary number to decimal.
    # If base number is 16 than hex, if it is 2 than it will convert from 2.
    def to_decimal(self, str_number, base_num, type="0"):
        base = base_num
        decimal = 0
        for i in range(1, len(str_number) + 1):
            holder = str_number[-1 * i]
            try:
                holder = int(holder)
            except:
                holder = self.dict1[holder.lower()]
            if str_number[0] == "1" and type.lower() == "s":
                if i == len(str_number):
                    holder *= -1

            piece = holder * (base ** (i - 1))
            decimal += piece
        return decimal

    # This is where I start everything.
    def main(self):
        number = object2.ask_for_hex()
        data_type = object2.ask_for_dtype()
        print(self.converter(number, data_type))

class TerminalUI:
    def __init__(self):
        self.dict1 = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
        self.list1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # If a hex number with odd len zero will be added to it's beggining.
    def add_zero(self, number):
        if len(str(number)) % 2 == 1:
            return ("{}" + number).format(0)
        else:
            return number

    # This function will ask for hexadecimal number and return it.
    def ask_for_hex(self):
        while True:
            a = 0
            print()
            hex_number = input("Enter a hexadecimal number: ")

            for i in hex_number:
                if i.lower() not in self.dict1 and i not in self.list1:
                    a = 1
                    print("This is not a hexadecimal number!")
                    break

            if a == 1:
                continue

            if len(hex_number) > 8:
                print("This number is more than 4bytes!")
                continue

            full_number = self.add_zero(hex_number)
            return full_number

    # This will ask user for data type input.
    def ask_for_dtype(self):
        while True:
            types = ["s", "u", "f"]
            data_type = input("Enter a data type: ")
            lower_data = data_type.lower()
            if lower_data not in types:
                print("Enter a valid data type! -> s, u, f")
                continue
            return lower_data

object2 = TerminalUI()
object1 = Converter(0x12368)
