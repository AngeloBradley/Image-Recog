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

# import dis

# def a():
#     a = (1,2,3)
#     new_a_temp = [x for x in a]
#     new_a_temp.append(4)
#     a = tuple(new_a_temp)


# def b():
#     a = [1,2,3]
#     a.append(4)

# print("assembly for 'adding value to tuple' by creating new tuple")
# dis.dis(a)
# print()

# print("assembly for appending item to list")
# dis.dis(b)

# import cv2
# import sys
# import base64
# import json

# orig_image = cv2.imread('cache/5ad38c9f-1dcf-47b8-b21b-97c171205cac.jpg')
# image_as_list = orig_image.tolist()
# image_as_bytes = orig_image.tobytes()
# image_as_base64= base64.b64encode(image_as_bytes)
# image_as_str_rep = json.dumps(image_as_list)

# print('ORIGNAL IMAGE: ')
# print('type: ', type(orig_image))
# print('length: ' + str(len(orig_image)))
# print('size:', sys.getsizeof(orig_image))
# print()

# print('IMAGE AS BYTES')
# print('type: ', type(image_as_bytes))
# print('length: ' + str(len(image_as_bytes)))
# print('size:', sys.getsizeof(image_as_bytes))
# print()

# print('IMAGE IN BASE64 FROM BYTES')
# print('type: ', type(image_as_base64))
# print('length: ' + str(len(image_as_base64)))
# print('size:', sys.getsizeof(image_as_base64))
# print()

# print('IMAGE AS LIST')
# print('type: ', type(image_as_list))
# print('length: ' + str(len(image_as_list)))
# print('size:', sys.getsizeof(image_as_list))
# print()

# print('IMAGE AS STRING REP OF LIST')
# print('type: ', type(image_as_str_rep))
# print('length: ' + str(len(image_as_str_rep)))
# print('size:', sys.getsizeof(image_as_str_rep))

# a = []

# for b in a:
#     print('blah')
#     print(b)