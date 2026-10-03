import sys


def convert_j2me_to_genesis(input_path, output_paths):
    if len(output_paths) != 3:
        raise ValueError("Exactly 3 output file paths are required.")

    with open(input_path, "rb") as in_f:
        data = in_f.read()

    # Remove 3-byte 0x00 padding from every 4-byte chunk
    unpadded_data = bytearray()
    for i in range(4, len(data), 4):
        unpadded_data.append(data[i + 3])

    # Extract individual levels based on header dimensions (width * height + header_size)
    offset = 0
    for out_path in output_paths:
        if offset + 2 > len(unpadded_data):
            raise ValueError("Corrupted J2ME data: premature end of file.")

        # In J2ME format, byte 0 is height, byte 1 is width
        height = unpadded_data[offset]
        width = unpadded_data[offset + 1]

        # Calculate total bytes for this level (2-byte header + grid size)
        level_size = 1 + (width * height + height)
        level_bytes = unpadded_data[offset : offset + level_size]

        # Swap width and height back for Genesis format
        genesis_level = bytes([width, height]) + level_bytes[2:]

        with open(out_path, "wb") as out_f:
            out_f.write(genesis_level)

        offset += level_size


if __name__ == "__main__":
    # Example usage:
    # python j2me_to_genesis.py zone_j2me.bin act1.bin act2.bin act3.bin
    if len(sys.argv) == 5:
        convert_j2me_to_genesis(sys.argv[1], sys.argv[2:5])
    else:
        print(
            "Usage: python j2me_to_genesis.py <input_j2me> <act1_out> <act2_out> <act3_out>"
        )