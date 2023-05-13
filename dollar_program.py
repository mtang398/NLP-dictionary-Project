import re
import pandas as pd

train_txt = "C:/Users/mstan/project/NLP_HW/all-OANC.txt"
test_txt = "C:/Users/mstan/project/NLP_HW/test_dollar_phone_corpus.txt"

with open(test_txt, "r", encoding = 'utf-8') as f:
	txt = f.readlines()

whole_txt = "".join(txt)

pattern1 = r'\$[0-9\.,]+\s+dollars?|\$[0-9\.,]+\s+cents?|\$[0-9\.,]+\s+cent?|\$[0-9\.,]+\s+dollar?|\$[0-9\.,]+\s+million?|\$[0-9\.,]+\s+billion?|\$[0-9\.,]+' # Search for $ xxx such as $6.57
pattern2 = r"[0-9\.,]+\s+dollar|[0-9\.,]+\s+cent|[0-9\.,]+\s+dollars|[0-9\.,]+\s+cents|[0-9\.,]+\s+million|[0-9\.,]+\s+billion" # search for number followed by words “dollar”, “dollars”, “cent”, “cents" and etc.
pattern3 = r"\b([Aa]|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|[Ss]even|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|[Hh]undred|[Tt]housand|million|billion|quarter|half)\b\s+\s*(dollars|cents|dollar|cent)"
def extract_dollar(string):
    dollar_regex1 = re.compile(pattern1)
    dollar_regex2 = re.compile(pattern2)
    dollar_regex3 = re.compile(pattern3)
    
    dollar_numbers1 = re.findall(dollar_regex1, string)
    dollar_numbers2 = re.findall(dollar_regex2, string)
    dollar_numbers3 = re.findall(dollar_regex3, string)
    dollar_numbers3_true = []
    for x in dollar_numbers3:
        a = list(x)
        a.insert(1, ' ')
        dollar_numbers3_true.append(''.join(a))
    return [dollar_numbers1, dollar_numbers2, dollar_numbers3_true]

dollars = extract_dollar(whole_txt)
print(dollars)
mystring = ''
for x in dollars:
    for y in x:
        mystring += y + '\n'

with open('C:/Users/mstan/project/NLP_HW/dollar_output.txt', 'w') as f:
    f.write(mystring)