def remove_header(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Remove the first line (header)
    lines = lines[1:]

    # Write the modified content to the output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(lines)
