def poly_to_bit(polynomial):
    terms = polynomial.replace(" ", "").split('+')
    lst = [0] * 32
    max_index = 0
    for term in terms:
        if term == '1':
            lst[0] = 1
        elif term == 'x':
            lst[1] = 1
            max_index = max(max_index, 1)
        else:
            x = term[1:]
            if x.isdigit() and 1 <= int(x) <= 32:
                lst[int(x) - 1] = 1
                max_index = max(max_index, int(x))
            else:
                raise ValueError(f"Invalid polynomial term: {term}")
    bit_string = ''.join(map(str, lst[::-1])).lstrip('0')
    return bit_string, max_index

def crc(user_data, divisor):
    divisor = list(map(int, divisor))  # Convert divisor to list of integers
    user_data = list(map(int, user_data))
    for i in range(len(divisor) - 1):
        user_data.append(0)
    dividend = user_data[:]
    pick = len(divisor)
    temp = dividend[0:pick]
    while pick < len(dividend):
        if temp[0] == 1:
            temp = [temp_bit ^ divisor_bit for temp_bit, divisor_bit in zip(temp, divisor)]
        else:
            temp = [temp_bit ^ 0 for temp_bit in temp]
        temp.append(dividend[pick])
        temp.pop(0)
        pick += 1
    if temp[0] == 1:
        temp = [temp_bit ^ divisor_bit for temp_bit, divisor_bit in zip(temp, divisor)]
    else:
        temp = [temp_bit ^ 0 for temp_bit in temp]
    remainder = ''.join(map(str, temp[1:]))
    return remainder

user_data = input("Enter the user data: ")
crc_list = [
    'x8+x2+x+1',
    'x10+x9+x5+x4+x2+1',
    'x16+x12+x5+1',
    'x32+x26+x23+x22+x16+x12+x11+x10+x8+x7+x5+x4+x2+x+1'
]

for crc_poly in crc_list:
    polynomial = crc_poly
    bit, Max = poly_to_bit(polynomial)
    rem = crc(user_data, bit)
    codeword = user_data + rem

    print(f"CRC-{Max}")
    print("\nSENDER SIDE")
    print("-------------")
    print("User data: ", user_data)
    print("Polynomial: ", polynomial)
    print("Divisor: ", bit)
    print("CRC (Remainder): ", rem)
    print("Codeword: ", codeword)

    print("\nRECEIVER SIDE")
    print("-------------")

    # Case 0: Received codeword is the same
    print("\nCASE 0")
    print("Received codeword: ", codeword)
    print("Divisor: ", bit)
    rem = crc(codeword, bit)
    print("Syndrome: ", rem)
    if rem == '0' * (len(bit) - 1):
        print(f"The received codeword {codeword} is accepted")
    else:
        print(f"The received codeword has an error, {codeword} is discarded")

    # Case 1: Introduce an error in the codeword
    print("\nCASE 1")
    new_codeword = codeword.replace("0", "1", 1)  # Flip the first '0' bit
    print("Received codeword: ", new_codeword)
    print("Divisor: ", bit)
    rem = crc(new_codeword, bit)
    print("Syndrome: ", rem)
    if rem != '0' * (len(bit) - 1):
        print(f"The received codeword has an error, {new_codeword} is discarded")
    else:
        print(f"The received codeword {new_codeword} is accepted")

    print("----------------------------------------------------------------------")
