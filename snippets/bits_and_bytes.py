'''How to work with bits and bytes in python'''

test = "aklsjdf;alksjdf;alksdjfa;lk++sdjf"
test = test.encode('UTF-8')

length = len(test)
print(length)

length_in_bytes = length.to_bytes(4, 'big')
print(length_in_bytes)

length_again = int.from_bytes(length_in_bytes, 'big')
print(length_again)
