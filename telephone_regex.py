import re
import pandas as pd

train_txt = "C:/Users/mstan/project/NLP_HW/all-OANC.txt"
test_txt = "C:/Users/mstan/project/NLP_HW/test_dollar_phone_corpus.txt"

with open(test_txt, "r", encoding = 'utf-8') as f:
	txt = f.readlines()

whole_txt = "".join(txt)

pattern1 = r"\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b" # With or without dashes (when without dashes, has a space in middle)
pattern2 = r"\(\d{3}\)[\s-]?\d{3}[\s-]?\d{4}" # With parrenthesis
 
def extract_phone_number(string):
    phone_regex1 = re.compile(pattern1)
    phone_regex2 = re.compile(pattern2)
    
    phone_numbers1 = re.findall(phone_regex1, string)
    phone_numbers2 = re.findall(phone_regex2, string)
    return [phone_numbers1, phone_numbers2]

numbers = extract_phone_number(whole_txt)
mystring = ''
for x in numbers:
    for y in x:
        if (re.findall('\n', y)) == []:
            mystring += y + '\n'

with open('C:/Users/mstan/project/NLP_HW/telephone_output.txt', 'w') as f:
    f.write(mystring)