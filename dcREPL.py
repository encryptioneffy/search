'''
    main for query so users can input a word they want to search for
'''
if __name__ == "__main__": 
    while True:
        user_input = input(">>search")
        if user_input == ":quit":
            break
        print(user_input.upper())
        