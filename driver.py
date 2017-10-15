import json
import os
from speech_scraper import save_remarks

def main():
    clinton_remarks_test = []
    clinton_remarks_train = []
    obama_remarks_test = []
    obama_remarks_train = []
    filenames = {'clinton_remarks_test': clinton_remarks_test,
                'clinton_remarks_train': clinton_remarks_train,
                'obama_remarks_test': obama_remarks_test,
                'obama_remarks_train': obama_remarks_train}

    exists = True
    for key, _ in filenames.items():
        if (not os.path.isfile('./' + key)):
            exists = False

    if (not exists):
        save_remarks()

    for key, value in filenames.items():
        with open(key) as json_file:
            value = json.load(json_file)

    with open('clinton_remarks_train') as json_file:
        clinton_remarks_train = json.load(json_file)
    with open('obama_remarks_train') as json_file:
        obama_remarks_train = json.load(json_file)

    print(len(clinton_remarks_train))
    print(len(obama_remarks_train))
    print(obama_remarks_train[0])

if __name__ == '__main__':
    main()
