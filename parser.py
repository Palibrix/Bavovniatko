import re
import sys


def process_includes(content):
    include_pattern = r'^include::(.+)$'
    processed_lines = []

    # Include all data before assigning variables
    for line in content.splitlines():
        if re.match(include_pattern, line):
            include_path = line.strip().split('::')[1].strip()
            included_content = read_include_file(include_path)
            if included_content:
                processed_lines.extend(included_content.splitlines())
            else:
                print(f"Error: File {include_path} not found.")
                continue
        else:
            processed_lines.append(line)
    return '\n'.join(processed_lines)


def read_include_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


def replace_variables(_input_file, _output_file):
    # Read the entire contents of the input file
    with open(_input_file, 'r') as file:
        content = file.read()

    # Process includes before variable replacements
    content = process_includes(content)

    # Define a pattern to match the variable definitions
    var_pattern = r'----\n(.*?)----'
    var_definitions = re.search(var_pattern, content, flags=re.DOTALL).group(1)
    content = content.replace('----\n' + var_definitions + '----\n', '')
    var_dict = {}
    for line in var_definitions.split('\n'):
        if ':' in line:
            key, value = line.split(':')
            var_dict[key.strip()] = value.strip()

    # Replace variables in the content
    for placeholder, replacement in var_dict.items():
        content = re.sub('{{' + placeholder + '}}', replacement, content)

    # Write the modified content to the output file
    with open(_output_file, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        replace_variables(input_file, output_file)
