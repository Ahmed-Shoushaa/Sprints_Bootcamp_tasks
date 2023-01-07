def string_mutation(s, pos, char):
    # change string(immutable) into a LIST(mutable)
    s = list(s)
    # string mutation
    s[int(pos)] = char
    # create empty string
    string = ""
    # for loop to turn list into  a string
    for i in s:
        string += i
    print(string)


# function call
string_mutation("abracadabra", 5, "k")
