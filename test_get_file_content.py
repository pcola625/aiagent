from functions.get_file_content import get_file_content

# run tests

test_cases = [["calculator", "lorem.txt"],
              ["calculator", "gorem.txt"],
              ["calculator", "../functions/get_file_content.py"],
              ["..", "../functions/get_file_content.py"],
              ["calculator", "../functions/shjit_file_copntet.py"],
              ["calculator/../functions","get_file_content.py"],
              ["calculator", "main.py"],
              ["calculator", "pkg/calculator.py"],
              ["calculator", "/bin/cat"], # (this should return an error string)
              ["calculator", "pkg/does_not_exist.py"],
             ]

for test in test_cases:
    print(f"Result for '{test[1]}' directory: {test[0]} ")
    print(f"{get_file_content(test[0],test[1])}")

 

