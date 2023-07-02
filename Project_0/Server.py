import socket



with open ("Source_strings.txt", "r") as source_file:
    source_contents = source_file.read()

converted_contents = source_contents.swapcase()

with open ("results.txt", "w") as results_file:
    results_file.write(converted_contents)