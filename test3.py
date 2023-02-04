def string_to_rgb(input_string):
    # Hash the input string to a 32-bit integer
    hash_value = hash(input_string) & 0xffffffff
    # Convert the 32-bit integer to 3 8-bit integers representing R, G, and B
    r = (hash_value >> 16) & 0xff
    g = (hash_value >> 8) & 0xff
    b = hash_value & 0xff
    return (r, g, b)

input_string = "hello world"
rgb_value = string_to_rgb(input_string)
print("RGB value for string '{}': {}".format(input_string, rgb_value))