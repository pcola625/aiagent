from functions.run_python_file import run_python_file

# run tests
"""
run_python_file("calculator", "main.py") (should print the calculator's usage instructions)
run_python_file("calculator", "main.py", ["3 + 5"]) (should run the calculator... which gives a kinda nasty rendered result)
run_python_file("calculator", "tests.py") (should run the calculator's tests successfully)
run_python_file("calculator", "../main.py") (this should return an error)
run_python_file("calculator", "nonexistent.py") (this should return an error)
run_python_file("calculator", "lorem.txt") (this should return an error)
"""
test_cases = [["calculator", "main.py"],
              ["calculator", "main.py" , ["3 + 5"]],
              ["calculator", "tests.py"],
              ["calculator", "../main.py"],
              ["calculator", "nonexistent.py"],
              [ "calculator", "lorem.txt"],
             ]

for test in test_cases:
    print(f"Result for '{test[1]}' file:")
    if len(test) == 2:
        print(f"{run_python_file(test[0],test[1])}")
    elif len(test) == 3:
        print(f"{run_python_file(test[0],test[1],test[2])}")
    else:
        print("invalid number of arguments for testing")