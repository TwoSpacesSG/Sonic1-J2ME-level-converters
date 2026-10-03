import sys


def convert_genesis_to_j2me(input_paths, output_path):
    if len(input_paths) != 3:
        raise ValueError("Exactly 3 input files are required.")

    with open(output_path, "wb") as out_f:
        # Write the J2ME container header indicating 3 levels
        out_f.write(bytes([0x00, 0x00, 0x00, 0x03]))

        for path in input_paths:
            with open(path, "rb") as in_f:
                data = in_f.read()

            if len(data) < 2:
                raise ValueError(f"File {path} is too small to contain a header.")

            width = data[0]
            height = data[1]

            # Calculate the length of the trailing zero-byte footer (height + 2)
            footer_length = width + 2

            # Trim the footer if present
            if footer_length > 0 and len(data) > 2 + footer_length:
                data = data[:-footer_length]

            # Swap width (byte 0) and height (byte 1)
            swapped_data = bytes([height, width]) + data[2:]

            # Pad each byte with three 0x00 bytes before it
            padded_data = bytearray()
            for byte in swapped_data:
                padded_data.extend([0x00, 0x00, 0x00, byte])

            out_f.write(padded_data)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        convert_genesis_to_j2me(sys.argv[1:4], sys.argv[4])
    else:
        print(
            "Usage: python genesis_to_j2me.py <act1> <act2> <act3> <output_j2me>"
        )