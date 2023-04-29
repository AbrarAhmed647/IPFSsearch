import sys
import json
import re
import os

###----------------------------README----------------------------------------###

# Dependency
    # File requires inverted_index.json file to be reachable and instantiated
        # with "{}"
    # File requires importing four modules shown above
# Tokenizatoin
    # .lower()
    # With import re I am splitting sentences into words and not including the
        # punctuation marks or other non-letter symbols
# Ordering
    # list of touples is order by highest frequency
# JSON format
    # # {keyword: [(cid, frequence), (cid2, frequence)]}
# Future works
    # when dumping new inverted_index, make it so system knows what has already
        # been sent to global index and doesn't include it in json
    # for performance improvement dump into json half way to index building so
        # lower pressure on memory
    # we could cover more file types, not just docx
# CONSIDERATIONS
    # When running script, the file path of file that will be scrapped must be
        # supplied
    # when moving this script around, how do we "pip install docx2txt"
        # automatically
    # right now the CID is word docx file name -> should be changed to CID
# Problems
    # word parser splits words like don't into don and t.



###--------------------------Declare-Method----------------------------------###

def inverted_index_builder(cid, keywords):
    for x in keywords:
        word = x.lower()
        if word not in inverted_index.keys():
            inverted_index[word] = [(cid, 1)]
        else:
            list_of_touples = inverted_index[word]
            exists = 0
            touple_count = 0
            for touple in list_of_touples:
                if touple[0] == cid:
                    exists = 1
                    break
                touple_count += 1
            if not exists:
                list_of_touples.append((cid, 1))
            else:
                list_of_touples[touple_count] = (list_of_touples[touple_count][0], list_of_touples[touple_count][1] + 1)
                while touple_count > 0:
                    if list_of_touples[touple_count][1] > list_of_touples[touple_count - 1][1]:
                        former = list_of_touples[touple_count - 1]
                        list_of_touples[touple_count - 1] = (list_of_touples[touple_count][0], list_of_touples[touple_count][1])
                        list_of_touples[touple_count] = former
                    touple_count -= 1
            inverted_index[word] = list_of_touples



###---------------------------START------------------------------------------###

# verify that only one argument was supplied
if len(sys.argv) != 2:
    print(f"More than two arguments were supplied to Python Script: {sys.argv[0]}")
    sys.exit(1)

# Get the array
array_with_files = sys.argv[1]

# convert argument to a list of dictionaries
array_with_files = json.loads(array_with_files)

# print(type(array_with_files))
# print(type(array_with_files[0]))


#######--------------------------Open-JSON-----------------------------------###

# with open('/Users/junweili/Desktop/Project_Github/Centralized-SE-for-IPFS/IPFS-Full-Stack-main/IPFS_Backend/controllers/index/inverted_index.json', 'r') as index:
#     inverted_index = json.load(index)

file_path = os.path.join(os.path.dirname(__file__), 'index', 'inverted_index.json')
with open(file_path, 'r') as index:
    inverted_index = json.load(index)


###--------------------Parsing-into-keywords-&-Index-Building----------------###

# traverse array and get name and keywords for all files
# parse keywords
# call index builder function for all files



for i in array_with_files:
    file_name = i[list(i.keys())[0]]
    keywords = re.findall(r'\b\w+\b', i[list(i.keys())[1]])
    inverted_index_builder(file_name, keywords)




###------------------------Dump-into-JSON------------------------------------###

with open(file_path, 'w') as index:
    json.dump(inverted_index, index)



