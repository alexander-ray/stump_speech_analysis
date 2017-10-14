import json

def main():
    with open('clinton_remarks') as json_file:
        clinton_remarks = json.load(json_file)
    with open('obama_remarks') as json_file:
        obama_remarks = json.load(json_file)

    print(len(clinton_remarks))
    print(len(obama_remarks))
    print(obama_remarks[0])

if __name__ == '__main__':
    main()
