def byte_stuffing(data):
    # Define the FLAG and ESC characters
    FLAG = "FLAG"
    ESC = "ESC"
    
    # Initialize the stuffed data with the FLAG at the start
    stuffed_data = [FLAG]
    
    # Iterate through the words in the data
    for word in data.split():
        if word == FLAG:
            # Add ESC before FLAG if FLAG is found in the data
            stuffed_data.extend([ESC, FLAG])
        elif word == ESC:
            # Add an extra ESC for each ESC in the data
            stuffed_data.extend([ESC, ESC])
        else:
            # Add the word as is
            stuffed_data.append(word)
    
    # Add the FLAG at the end
    stuffed_data.append(FLAG)
    
    # Join the list back into a string
    return " ".join(stuffed_data)

def byte_destuffing(data):
    # Define the FLAG and ESC characters
    FLAG = "FLAG"
    ESC = "ESC"
    
    # Remove the FLAG at the start and end
    words = data.split()
    if words[0] == FLAG:
        words = words[1:]
    if words[-1] == FLAG:
        words = words[:-1]
    
    # Initialize the destuffed data
    destuffed_data = []
    
    # Iterate through the words to remove stuffing
    i = 0
    while i < len(words):
        if words[i] == ESC:
            if i + 1 < len(words) and (words[i + 1] == FLAG or words[i + 1] == ESC):
                destuffed_data.append(words[i + 1])
                i += 2
            else:
                destuffed_data.append(words[i])
                i += 1
        else:
            destuffed_data.append(words[i])
            i += 1
    
    # Join the list back into a string
    return " ".join(destuffed_data)

# Get input from the user
data = input("Enter the sentence: ")

# Perform byte stuffing and destuffing
stuffed_data = byte_stuffing(data)
destuffed_data = byte_destuffing(stuffed_data)

# Display the results
print("\nSender Side:")
print(f"User Data: {data}")
print(f"Byte Stuffed: {stuffed_data}")

print("\nReceiver Side:")
print(f"Received Data: {stuffed_data}")
print(f"Byte Destuffed: {destuffed_data}")
