import argparse

def replace_strings(file_in_name, file_out_name, original_strings, replacement_strings):
    print(original_strings, replacement_strings)
    if len(original_strings) != len(replacement_strings):
        raise Exception('Lists of different lenghts, you got a problem here my man')

    data = read_data(file_in_name)
    for i in range(len(original_strings)):
        data = data.replace(original_strings[i], replacement_strings[i])

    write_data(file_out_name, data)

def read_data(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
    return data

def write_data(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_in_name', '-fi', help='REQUIRED: The name of your file to read, you need this buddy.', type=str, required=True)
    parser.add_argument('--file_out_name', '-fo', help='REQUIRED: The name of your file to write, you need this buddy.', type=str, required=True)
    parser.add_argument('--original_strings', '-o', help='REQUIRED: The list of template strings in the control file.', nargs='*', type=str, required=True)
    parser.add_argument('--replacement_strings', '-r', help='REQUIRED: The list of strings to replace template strings.', nargs='*', type=str, required=True)
    args = parser.parse_args()

    replace_strings(args.file_in_name, args.file_out_name, args.original_strings, args.replacement_strings)

if __name__ == '__main__':
    main()
