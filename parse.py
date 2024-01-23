#!/usr/bin/python3

# Candace Hernando
# Honor Pledge: I will neither give nor receive aid on this assessment


import re


# <SP> ::= the space or tab character
def SP(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
            return False, current_index
    # if elt is a space or the tab character, it is a SP
    if mfmessage[current_index] == " " or mfmessage[current_index] == "\t":
        return True

    # if it is not a space or tab character, it is NOT a SP
    else:
        return False

# <digit> ::= any one of the ten digits 0 through 9
def digit(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # trying turning elt into an integer
    try:
        int_try = int(mfmessage[current_index])
        # if it works, then elt is a digit
        return True

    # if it doesnt work, elt is NOT a digit
    except ValueError:
        return False


# <letter> ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
def letter(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # get current elt
    tester = mfmessage[current_index]

    # if it is an example of an alphabetical letter, it is a letter
    if tester.isalpha() == True:
        return True
    
    # if it is not, it is NOT a letter
    else:
        return False


# <special> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "." | "," | ";" | ":" | "@" | """
def special(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # get current elt
    tester = mfmessage[current_index]
    # returns True if elt is one of the following characters
    pattern = re.compile(r'[<>()\[\]\\.,;:@"]')

    # use the search function to check for a match
    match = pattern.search(tester)

    # returns True is there is no match, False if there is one
    return match is not None

# <char> ::= any one of the printable ASCII characters, but not any of <special> or <SP>
def char(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # if it is a special char or a space, it is NOT a character
    if special(mfmessage, current_index) == True or SP(mfmessage, current_index) == True:
        return False

    # get current elt
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    tester = mfmessage[current_index]

    # if the number rep of it is less than 128 (i.e. ASCII), it is a character
    if ord(tester) < 128:
        return True

    # if it is not ASCII, it is NOT a char
    else:
        return False


# <whitespace> ::= <SP> | <SP> <whitespace>
# returns error, updates index
def whitespace(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- whitespace")
        return False, current_index
    # if elt is a SP
    if SP(mfmessage, current_index) == True:
        # while the elt is a SP, keep going
        while SP(mfmessage, current_index) == True:
            current_index += 1
            if valid_index(mfmessage,current_index) != True:
                break
            continue
        # if elt starts with SP, it is a whitespace
        return True, current_index
    
    # if elt doesnt begin with a SP, it is NOT a whitespace
    else:
        print("ERROR -- whitespace")
        # return to parser
        return False, current_index
        
        
# <nullspace> ::= <null> | <whitespace>
def nullspace(mfmessage, current_index):
    # if elt (and beyond) is a whitespace, it is a nullspace
    if SP(mfmessage, current_index) == True:
        # while the elt is a SP, keep going
        while SP(mfmessage, current_index) == True:
            current_index += 1
            if valid_index(mfmessage,current_index) != True:
                break
            continue
        # if elt starts with SP, it is a whitespace
        return True, current_index

    # if not a space, then there is nothing there and elt is a nullspace
    return True, current_index
    # does not return false because could be nothing


# <CRLF> ::= the newline character
# returns error
def CRLF(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return True, current_index
    
    # if it is valid, it is NOT a CLRF
    else:
        print("ERROR -- CRLF")
        return False, current_index


# <let-dig> ::= <letter> | <digit>
def let_dig(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # if the elt is not a letter
    if letter(mfmessage, current_index) == False:
        # if the elt is also not a digit, it is NOT a let_dig
        if digit(mfmessage, current_index) == False:
            return False

    # if both arent False, it is a let_dig
    return True


# <let-dig-str> ::= <let-dig> | <let-dig> <let-dig-str>
# updates index
def let_dig_str(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # if elt is a let_dig
    if let_dig(mfmessage, current_index) == True:
        # keep going until elt is not a let_dig
        while let_dig(mfmessage, current_index) == True:
            current_index += 1
            if valid_index(mfmessage,current_index) != True:
                break
            continue
        # if at least one let_dig, it is a let_dig_str
        return True, current_index

    # if does not start with let_dig, it is NOT a let_dig_str
    else:
        return False, current_index


# <name> ::= <letter> <let-dig-str>
def name(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        return False, current_index
    # if elt is a letter
    if letter(mfmessage, current_index) == True:
        # if following elt (and beyond) is(are) a let_dig_str, elt is a name
        # go to next index
        current_index += 1
        if valid_index(mfmessage,current_index) != True:
            return False, current_index
        # test if elt is a Let_dig_str
        tester = let_dig_str(mfmessage, current_index)
        if  tester[0] == True:
            return True, tester[1]
        # if letter isnt followed by let_dig_str, NOT a name
        else:
            return False, tester[1]

    # if does not begin with a letter, it is NOT a name
    else:
        return False, current_index


# <element> ::= <letter> | <name>
# returns error
def element(mfmessage, current_index):
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- element")
        return False, current_index
    # if elt is not a letter
    if letter(mfmessage, current_index) == False:
        # if elt is also not a name, then it is NOT an element
        tester = name(mfmessage, current_index)
        if  tester[0] == False:
            # return to parser
            return False, tester[1]

    # if both are not False, then it is an element
    else:
        return True, current_index


# <string> ::= <char> | <char> <string>
# returns error, updates index
def string(mfmessage, current_index):
    str_cur = current_index
    # check if str_cur is a valid index
    # string error if not valid
    if valid_index(mfmessage,str_cur) != True:
        print("ERROR -- string")
        return False, str_cur
    # if it is a character
    if char(mfmessage, str_cur) == True:
        # while the elt is a character
        while char(mfmessage, str_cur) == True:
            str_cur += 1
            # check if next index is valid
            # if not valid, dont run through char again
            if valid_index(mfmessage,str_cur) != True:
                break
            continue
        # if there is at least 1 character, it is a string
        return True, str_cur

    # does not start with an character, it is NOT a string
    else:
        print("ERROR -- string")
        #return to parser
        return False, str_cur


# <domain> ::= <element> | <element> "." <domain>
def domain(mfmessage, current_index):
    # set temp var to hold current_index
    dom_cur = current_index
    # must begin with an element
    tester = element(mfmessage, dom_cur)
    if tester[0] == True:
        while element(mfmessage, dom_cur)[0] == True:
            # increase index
            dom_cur = element(mfmessage, dom_cur)[1] + 1
            if valid_index(mfmessage,dom_cur) != True:
                break
            # if elt is followed by ">", it is a domain
            if mfmessage[dom_cur] == ">":
                return True, dom_cur
            # if it is a "."
            if mfmessage[dom_cur] == ".":
                dom_cur += 1
                # followed by an element, continue
                if domain(mfmessage, dom_cur)[0] == True:
                    continue
                # not followed by an element, it is NOT a domain
                else:
                    return False, dom_cur
        # if begins with an element, it is a domain       
        return True, dom_cur

    # if it doesnt begin with an element, it is NOT a domain
    else:
        return False, tester[0]


# <local-part> ::= <string>
def local_part(mfmessage, current_index):
    # set temp var for current_index
    loc_cur = current_index
    # if elt is a string, it is a local_part
    tester = string(mfmessage, loc_cur)
    if tester[0] == True:
        return True, tester[1]

    # if elt is not a string, it is NOT a local_part    
    else:
        return False, tester[1]


# <mailbox> ::= <local-part> "@" <domain>
# returns error                              
def mailbox(mfmessage, current_index):
    # test if begins with a local_part
    tester = local_part(mfmessage, current_index)
    # set temp var for index
    mail_cur = tester[1]

    # if does not begin with local_part, it is NOT a mailbox
    if tester[0] == False:
        return False, mail_cur
    
    # check if mail_cur is valid
    # if string followed by invalid index, and returns invalid index to local_part to mailbox
    if valid_index(mfmessage,mail_cur) != True:
        print("ERROR -- mailbox")
        return False, mail_cur

    # if local_part is not followed by "@", it is NOT a mailbox
    if mfmessage[mail_cur] != "@":
        print("ERROR -- mailbox")
        # return to parser
        return False, mail_cur

    # increase index
    mail_cur += 1
    # elt will throw error if starts with invalid index
    elt_test = element(mfmessage, mail_cur)
    mail_cur = elt_test[1]

    # if next elt is not an element, it is NOT a mailbox
    if elt_test[0] != True:
        print("ERROR -- element")
        return False, mail_cur
    
    # test if it is followed by another domain
    # if mail_cur invalid, will send to element, which throws error
    tester_b = domain(mfmessage, mail_cur)
    mail_cur_b = tester_b[1]
    
    # if not followed by domain, it is NOT a mailbox
    if tester_b[0] == False:
        print("ERROR -- mailbox")
        # return to parser
        return False, mail_cur_b

    # if it is local_part, "@", domain, it is a mailbox
    return True, mail_cur_b


# <path> ::= "<" <mailbox> ">"
# returns error
def path(mfmessage, current_index):
    # if elt doesnt begin with <, it is NOT a path
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- path")
        return False, current_index
    if mfmessage[current_index] != "<":
        print("ERROR -- path")
        # return to parser
        return False, current_index

    current_index += 1
    # if the mailbox isnt true, should pass error in mailbox
    # if index invalid, local_part -> string -> throws error
    tester = mailbox(mfmessage, current_index)
    current_index = tester[1]

    if tester[0] == False:
        return False, current_index

    # if mailbox good but is followed by invalid index - path error
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- path")
        return False, current_index
    
    if tester[0] == True:
        # if elt doesnt end with >, it is NOT a path
        if mfmessage[current_index] != ">":
            print("ERROR -- path")
            # return to parser
            return False, current_index

    # if elt is "<", mailbox, ">", it is a path
    return True, current_index


# <reverse-path> ::= <path>
def reverse_path(mfmessage, current_index):
    # if it is not a path, should pass error in path
    # if current_index invalid, will pass error in path
    tester = path(mfmessage, current_index)
    if valid_index(mfmessage,tester[1]) != True:
        return False, tester[1]
    
    if tester[0] == True:
        # if the last elt is ">", then it is a reverse_path
        if mfmessage[tester[1]] == ">":
            current_index = tester[1]
            return True, current_index
        # if it is not, it is NOT a reverse_path
        else:
            return False, current_index
        
    # if it is not a path, it is NOT a reverse_path 
    else:
        return False, tester[1]


# check if valid index
def valid_index(mfmessage, current_index):
    len_mess = len(mfmessage)
    if current_index >= len_mess:
        return False
    if current_index < 0:
        return False
    else:
        return True


# <mail-from-cmd> ::= “MAIL” <whitespace> “FROM:” <nullspace> <reverse-path> <nullspace> <CRLF>
# returns error
def mail_from_cmd(mfmessage, current_index):
    # check for MAIL
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False
    
    if mfmessage[current_index] != "M":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "A":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "I":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "L":
        print("ERROR -- mail-from-cmd")
        return False

    # check for whitespace
    current_index += 1
    # whitespace will return error if index isnt valid
    test_white = whitespace(mfmessage, current_index)
    if  test_white[0] != True:
        return False

    # check for FROM:
    current_index = test_white[1]
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "F":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "R":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "O":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != "M":
        print("ERROR -- mail-from-cmd")
        return False
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    if mfmessage[current_index] != ":":
        print("ERROR -- mail-from-cmd")
        return False

# check for nullspace
    current_index += 1
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    test_nul = nullspace(mfmessage, current_index)
    if  test_nul[0] != True:
        return False

    # check for reverse_path
    current_index = test_nul[1]
    # if index invalid, reverse_path -> path throws error
    test_rev = reverse_path(mfmessage, current_index)
    if  test_rev[0] != True:
        return False

    # check for nullspace
    current_index = test_rev[1]
    if valid_index(mfmessage,current_index) != True:
        print("ERROR -- mail-from-cmd")
        return False, current_index
    # if last elt is ">", it is a mail_from_cmd
    if mfmessage[current_index] != ">":
        return False
    test_nulb = nullspace(mfmessage, current_index)

# check for CRLF
    current_index = test_nulb[1] + 1
    if valid_index(mfmessage, current_index) == True:
        print("ERROR -- CRLF")
        return False

    # if passes all these tests, it is a valid mail_from_cmd
    return True


def main():
     try:
        # reading lines from standard input until EOF (ctrl + D on Linux)
        while True:
            # read a line from standard input
            line = input()
            
            # break the loop if EOF is reached
            if not line:
                break
            
            current_index = 0
            mfmessage = line
            print(line)

            # check if it is a valid address
            if mail_from_cmd(mfmessage, current_index) == True:
                print("Sender ok")
     except EOFError:
        return


if __name__ == "__main__":
    main()
