import cv2
import numpy as np
import os

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(original_image_path, secret_data):
    # read the image
    original_image = cv2.imread(original_image_path)
    # maximum bytes to encode
    max_bytes = original_image.shape[0] * original_image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", max_bytes)
    if len(secret_data) > max_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    
    for row in original_image:
        for pixel in row:
            # convert RGB values to binary format
            red, green, blue = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(red[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(green[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(blue[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return original_image


def decode(encoded_image_path):
    print("[+] Decoding...")
    # read the image
    encoded_image = cv2.imread(encoded_image_path)
    binary_data = ""
    for row in encoded_image:
        for pixel in row:
            red, green, blue = to_bin(pixel)
            binary_data += red[-1]
            binary_data += green[-1]
            binary_data += blue[-1]

    # split by 8-bits
