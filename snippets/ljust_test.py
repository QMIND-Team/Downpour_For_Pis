
def main():
    # to_send_raw = "akjsdjfaksjdflkasjflkajsdf;lkajsdflkajsd;lkfjasdl;kfjalk;sdfja;lkdsfj"
    # to_send_bytes = to_send_raw.encode('UTF-8')

    int_to_send = 128000000

    size_of_int_to_send = int_to_send.__sizeof__()
    print(size_of_int_to_send)

    # print(len(encoded_str))

    # to_send_bytes = bytes(to_send_raw)

    # print(bin(to_send_bytes))
    # to_send = '00' + bin(to_send_bytes)[2:].rjust(30,'0')

    # print(to_send)
    # length = len(to_send)
    # print(length)

    # print(int(to_send))


if __name__ == '__main__':
    main()
    