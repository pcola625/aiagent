from functions.get_files_info import get_files_info

# run tests

test_cases = [["calculator", "."],
              ["calculator", "pkg"],
              ["calculator", "/bin"],
              ["calculator", "../"],
             ]

for test in test_cases:
    print(f"Result for '{test[1]}' directory:")
    print(f"{get_files_info(test[0],test[1])}")

 

