def bit_stuff(data):
    flag = '01111110'  # Frame flag
    stuffed_data = flag  # Start with the flag

    count = 0  # To count consecutive '1's
    for bit in data:
        stuffed_data += bit
        if bit == '1':
            count += 1
            # After 5 consecutive '1's, insert a '0'
            if count == 5:
                stuffed_data += '0'  # Insert the '0' after the 5th '1'
                count = 0  # Reset the count
        else:
            count = 0  # Reset the count if a '0' is encountered

    stuffed_data += flag  # Add flag at the end
    return stuffed_data


def bit_destuff(stuffed_data):
    flag = '01111110'  # Frame flag
    data_without_flags = stuffed_data[len(flag):-len(flag)]  # Remove the flags

    destuffed_data = ""
    count = 0  # To count consecutive '1's

    # Traverse through the stuffed data and remove the stuffed '0's
    i = 0
    while i < len(data_without_flags):
        destuffed_data += data_without_flags[i]
        if data_without_flags[i] == '1':
            count += 1
            # Skip the stuffed '0' after 5 consecutive '1's
            if count == 5 and i + 1 < len(data_without_flags) and data_without_flags[i + 1] == '0':
                i += 1  # Skip the stuffed '0'
                count = 0  # Reset the count after destuffing
        else:
            count = 0  # Reset count on '0'
        i += 1

    return destuffed_data


def main():
    # Input from the user
    user_data = input("Enter the data message (in bits, e.g., '101110111011'): ").strip()
    frame_size = int(input("Enter the size of each frame (e.g., 8): ").strip())

    # Sender side: Bit Stuffing
    print("\nSender Side:")
    print(f"User Data: {user_data}")
    stuffed_data = bit_stuff(user_data)
    print(f"After Bit Stuffing: {stuffed_data}")

    # Simulate transmission (breaking the stuffed data into frames)
    print(f"\nData Sent in Frames (size {frame_size}):")
    for i in range(0, len(stuffed_data), frame_size):
        print(f"Frame: {stuffed_data[i:i + frame_size]}")

    # Receiver side: Bit Destuffing
    print("\nReceiver Side:")
    print(f"Data Received: {stuffed_data}")
    destuffed_data = bit_destuff(stuffed_data)
    print(f"After Bit Destuffing: {destuffed_data}")


if __name__ == "__main__":
    main()
