def xor(a, b): 
    result = "" 
    n = len(b) 
    for i in range(1, n): 
        if a[i] == b[i]: 
            result += "0" 
        else: 
            result += "1" 
    return result 
 
 
def mod_div(dividend, divisor): 
    pick = len(divisor) 
    temp = dividend[:pick] 
    n = len(dividend) 
 
    while pick < n: 
        if temp[0] == '1': 
            temp = xor(divisor, temp) + dividend[pick] 
        else: 
            temp = xor('0' * pick, temp) + dividend[pick] 
        pick += 1 
 
    if temp[0] == '1': 
        temp = xor(divisor, temp) 
    else: 
        temp = xor('0' * len(temp), temp) 
 
    return temp 
 
 
def encoded_data(data, key): 
    l_key = len(key) 
    appended_data = data + '0' * (l_key - 1) 
    remainder = mod_div(appended_data, key) 
    codeword = data + remainder 
    print("Remainder:", remainder) 
    print("Encoded Data (data + remainder):", codeword) 
    return codeword 
 
 
def receiver(data, key): 
    curr = mod_div(data, key) 
    if "1" in curr: 
        print("There is some error in data.") 
    else: 
        print("Correct message received.") 
 
 
if __name__ == "__main__": 
    data = input("Enter the data to be sent (binary string): ") 
    key = input("Enter the key (binary string): ") 
 
    print("\nSender Side:") 
    encoded = encoded_data(data, key) 
 
    print("\nReceiver Side:") 
    receiver(encoded, key) 







# with polynomial
# def xordiv(tmp, d):
#     word = tmp[:len(d)]
#     i = len(d)

#     while i <= len(tmp):
#         if len(word) == len(d):
#             word = ''.join(
#                 '1' if (int(word[j]) ^ int(d[j])) else '0'
#                 for j in range(len(d))
#             )
#             f = word.find('1')
#             word = word[f:] if f != -1 else ""
#         else:
#             if i == len(tmp):
#                 break
#             word += tmp[i]
#             i += 1

#     if len(word) < len(d):
#         diff = len(d) - len(word) - 1
#         word = word + '0' * diff

#     return word


# def sender(data, d):
#     tmp = data + '0' * (len(d) - 1)
#     crc = xordiv(tmp, d)
#     print("CRC:", crc)
#     code = data + crc
#     print("Code word:", code)
#     return code


# def receiver(code, d):
#     return xordiv(code, d)


# def main():
#     print("Sender side:")
#     data = input("Enter Data word: ")
#     poly = input("Enter the Polynomial: ")

#     div = 0
#     n = 0
#     for char in poly:
#         if char.isdigit():
#             n = n * 10 + int(char)
#         elif char == '+':
#             div ^= (1 << n)
#             n = 0

#     if poly[-1] == '1':
#         div ^= 1

#     d = bin(div)[2:]

#     print("Divisor:", d)
#     code = sender(data, d)

#     print("Receiver side:")
#     print("Code word:", code)
#     tst = receiver(code, d)

#     print("Case 0: Without Error")
#     print("Divisor:", d)
#     print("Syndrome:", tst)

#     if '1' not in tst:
#         print("As syndrome contains all Zeroes, the code word is Accepted")
#     else:
#         print("As syndrome contains ones, the code word is Not Accepted")

#     # Introduce an error
#     code = list(code)
#     code[5] = '0' if code[5] == '1' else '1'
#     code = ''.join(code)
#     tst = receiver(code, d)

#     print("Case 1: With Error")
#     print("Divisor:", d)
#     print("Syndrome:", tst)

#     if '1' not in tst:
#         print("As syndrome contains all Zeroes, the code word is Accepted")
#     else:
#         print("As syndrome contains ones, the code word is Not Accepted")


# if _name_ == "_main_":
#     main()