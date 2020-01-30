import json

class Test(object):
    def __init__(self, data=None):
        if data:
            self.__dict__ = json.loads(data)
        else:
            self.c = ""


def main():
    json_data = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'

    empty = Test()
    print(empty.c)
    test1 = Test(json_data)
    print(test1.c)

    # loaded_json = json.loads(json_data)

    # for x in loaded_json:
    #     print(str(x)+": "+str(loaded_json[x]))

    # print(json.dumps(parsed_json, indent = 4, sort_keys=True))    

if __name__ == '__main__':
    main()
    