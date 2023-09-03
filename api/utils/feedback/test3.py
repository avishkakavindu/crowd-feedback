import re
import csv

with open('ebay_reviews_cleaned.csv', 'r') as file:
    reader = csv.reader(file)

    lst = []
    for row in reader:
        # print(row[1])
        predt = row[1]
        text = row[2]
        print(predt)

        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        newword = emoji_pattern.sub(r'', text+ "\t"+predt)  # no emoji
        n = newword.encode('ascii', 'ignore').decode('ascii')

        lst.append(n)

    # print(lst)
for line in lst:
    f = open("twt.tsv", "a")
    f.write(line + '\n')
    f.close()
