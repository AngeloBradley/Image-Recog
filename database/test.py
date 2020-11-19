# d = {'a':0}
# d['b']

# import dis

# def a():
#     a = [1,2,3,4,5]
#     5 in a
#     6 in a

# def b():
#     b = (1,2,3,4,5)
#     5 in b
#     6 in b

# print('list method disassembled')
# dis.dis(a)
# print()

# print('tuple method disassembled')
# dis.dis(b)

# ''' assigning is faster but the instructions for searching for
# items in the structure and searching for items that are not are
# the same
# '''

import dis

def a():
    a = (1,2,3)
    new_a_temp = [x for x in a]
    new_a_temp.append(4)
    a = tuple(new_a_temp)


def b():
    a = [1,2,3]
    a.append(4)

print("assembly for 'adding value to tuple' by creating new tuple")
dis.dis(a)
print()

print("assembly for appending item to list")
dis.dis(b)