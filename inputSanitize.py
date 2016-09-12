#!/usr/bin/python

def sanitize(input_string):
    output_string =''
    for i in input_string:
        if i == '>':
            outputChar = '&gt;'
        elif i == '<':
            outputChar = '&lt;'
        elif i == "'":
            outputChar = '&quot;'
        elif i == '"':
            outputChar = '&quot;'
        else:
            outputChar = i
        output_string += outputChar
    print output_string
    return output_string

if __name__=='__main__':
    input_string = raw_input("Enter the string: ")
    sanitize(input_string)


