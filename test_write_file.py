from functions.write_file_content import write_file_content

# run tests

test_cases = [["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
              ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
              ["calculator", "/tmp/temp.txt", "this should not be allowed"],
              ["calculator", "pkg/crap/morecrap/deepcrap.txt", "craptastic crap.txt"],
              ["..", "anybadthing/badthings.txt", "rm -rF *"],
              ["/", "anybadthing/badthings.txt", "rm -rF *"]
             ]

for test in test_cases:
    print(f"Result for '{test[1]}' directory: {test[0]} ")
    print(f"{write_file_content(test[0],test[1],test[2])}")

 

