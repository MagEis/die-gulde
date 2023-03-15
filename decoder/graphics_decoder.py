import os
import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

file_name = sys.argv[1]

def decode_graphics(input_path: str, output_path: str):
    if input_path is None or output_path is None:
        raise ValueError("Input and output paths must be specified")

    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file not found")
    
    output_graphics_path = os.path.join(output_path, "graphics")

    if not os.path.exists(output_graphics_path):
        os.mkdir(output_path)
        os.mkdir(output_graphics_path)

    with open(input_path, "rb") as file:
        header_data = file.read(4)

        graphics_count = int.from_bytes(header_data, byteorder="little", signed=False)

        print(f"Found {graphics_count} graphics")

        graphics = []

        for i in range(graphics_count):
            graphics_header_data = file.read(84)
            graphics_name = graphics_header_data[:32].decode("ascii").strip("\x00")
            graphics_relative_start_address = int.from_bytes(graphics_header_data[48:52], byteorder="little", signed=False)
            graphics_width = int.from_bytes(graphics_header_data[80:82], byteorder="little", signed=False)
            graphics_height = int.from_bytes(graphics_header_data[82:84], byteorder="little", signed=False)

            print(f"Decoding {graphics_name} ({graphics_width}x{graphics_height}) at +{graphics_relative_start_address}")

            graphics.append({
                "name": graphics_name,
                "relative_start_address": graphics_relative_start_address,
                "width": graphics_width,
                "height": graphics_height
            })

        prev_addr = 0
        PBANK_OFFSET = 2117
        PIXEL_BYTE_SIZE = 3
        INC_X = 0
        INC_Y = 4
        for i in range(graphics_count):
            graphic = graphics[i]
            print(f"processing element: {graphics[i]}")
            if graphics[i]['relative_start_address'] != 0:
                prev_addr = graphic['relative_start_address']
            file.seek(prev_addr + PBANK_OFFSET  )
            random_data = file.read(4)
            value = struct.unpack('<I', random_data)[0]

            lost = file.read(7)
            lost = lost + file.read(15*PIXEL_BYTE_SIZE)
            print(lost)
            #file.seek(prev_addr + PBANK_OFFSET + 5+ 15*PIXEL_BYTE_SIZE)
            print(f"value = {value}")
            data = file.read((graphic['width'] +INC_X)* (graphic['height']+INC_Y) * PIXEL_BYTE_SIZE)
            result = np.frombuffer(data, dtype=np.ubyte)
            result = result.reshape((graphic['width']+INC_X, graphic['height']+INC_Y, PIXEL_BYTE_SIZE))
            if graphics[i]['width'] == 0 or graphic['height'] == 0:
                continue
            #plt.imshow(result)
            #plt.show()
            graphic_data = file.read(graphic["width"] * graphic["height"] * 3)
            if graphic['width'] == 0 or graphic['height'] == 0:
                continue
            plt.imshow(result)
            plt.show()
            #img = Image.frombytes(mode="RGB", size=(graphic["width"], graphic["height"]), data=graphic_data)

            #img.show()

            prev_addr = prev_addr + value   
            '''         
            file.seek(prev_addr + PBANK_OFFSET  )
            raw_data = file.read(value)

            filename = f'{output_path}/graphics/{graphic["name"]}.bmp'

            with open(filename, 'wb') as bmp_file:
                # wav_file.write(wav_header_data)
                bmp_file.write(raw_data)
            return'''


        '''for graphic in graphics:
            file.seek(graphic["relative_start_address"], os.SEEK_CUR)

            graphic_data = file.read(graphic["width"] * graphic["height"] * 3)

            img = Image.frombytes(mode="RGB", size=(graphic["width"], graphic["height"]), data=graphic_data)

            img.show()'''




if __name__ == "__main__":
    decode_graphics(file_name, "output")

######################
# old code by MagEis

'''
import sys
import struct
import numpy as np

import matplotlib.pyplot as plt

# Open the binary file in read mode
with open(file_name, 'rb') as file:

    header_data = file.read(4)
    header = {}
    header['count'] = struct.unpack('<I', header_data[:4])[0]

    print(f"found {header['count']} elements")

    elements = []

    for i in range(header['count']):
        element_data = file.read(84)
        element = {}
        element['name'] = element_data[:48].decode('ascii').rstrip('\x00')
        element['size_x'] = struct.unpack('<H', element_data[80:82])[0]
        element['size_y'] = struct.unpack('<H', element_data[82:84])[0]
        element['rel_start_addr'] = struct.unpack('<I', element_data[48:52])[0]

        print(element)
        elements.append(element)

    # rip off the data from the file
    prev_addr = 0
    PBANK_OFFSET = 2117
    PIXEL_BYTE_SIZE = 3
    INC_X = 0
    INC_Y = 4
    for i in range(header['count']):
        print(f"processing element: {elements[i]}")
        if elements[i]['rel_start_addr'] != 0:
            prev_addr = elements[i]['rel_start_addr']
        file.seek(prev_addr + PBANK_OFFSET  )
        random_data = file.read(4)
        value = struct.unpack('<I', random_data)[0]
        lost = file.read(7)
        lost = lost + file.read(15*PIXEL_BYTE_SIZE)
        print(lost)
        #file.seek(prev_addr + PBANK_OFFSET + 5+ 15*PIXEL_BYTE_SIZE)
        print(f"value = {value}")
        data = file.read((elements[i]['size_x'] +INC_X)* (elements[i]['size_y']+INC_Y) * PIXEL_BYTE_SIZE)
        result = np.frombuffer(data, dtype=np.ubyte)
        result = result.reshape((elements[i]['size_x']+INC_X, elements[i]['size_y']+INC_Y, PIXEL_BYTE_SIZE))
        if elements[i]['size_x'] == 0 or elements[i]['size_y'] == 0:
            continue
        plt.imshow(result)
        plt.show()
        prev_addr = prev_addr + value'''