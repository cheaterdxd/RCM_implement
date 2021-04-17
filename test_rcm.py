# from math import ceil,floor
# a = 40
# b = 60
# ax = (2*a-b)
# bx = (2*b-a)
# tempa = ax
# tempb = bx
# print(f"a:{a}\nb:{b}\ntranform :\n ax:{ax}\nbx:{bx}")
# print("giau tin : bit 0")
# if(ax%2==0):
#     ax+=1
# if(bx%2==1):
#     bx-=1
# print(f"ax:{ax}\nbx:{bx}")

# print("giau tin : bit 1")
# if(tempa%2==0):
#     tempa+=1
# if(tempb%2==0):
#     tempb+=1
# print(f"ax:{tempa}\nbx:{tempb}")


# print("===================== start reform ========================")
# if(tempa%2==1):
#     tempa-=1
# if(tempb%2==1):
#     tempb-=1

# # lsb(a',b') = (0,0)
# if(ax%2==1):
#     ax-=1
# if(bx%2==1):
#     bx-=1

# a1 = ceil((2*ax+bx)/3)

# b1 = ceil((2*bx+ax)/3)
# print(f"reform :\na:{a1}\nb:{b1}")

# a2 = ceil((2*tempa+tempb)/3)

# b2 = ceil((2*tempb+tempa)/3)
# print(f"reform :\na:{a2}\nb:{b2}") 


# with open("conmeo.bmp","rb") as inputf, open("copy_conmeo.bmp","wb") as outf:
#     conten_a = inputf.read(54)
#     outf.write(conten_a)
#     while True:
#         byte_i = inputf.read(1)
#         a = int.from_bytes(byte_i,'little')^1
#         if(byte_i == b''):
#             break 
#         outf.write(a.to_bytes(1,byteorder='little'))

# a = open("a.txt",'rb+')
# idx = 2
# a_content = a.read()
# new_content = a_content[0:idx]+b'l'+a_content[idx+1:]
b = open("b.txt","wb+")
b.seek(0,0)
a = b.read(5)
sua = b.read(1)
r = b.read()
content = a+sua+r
b.seek(0,0)
b.write(content)
# a.close()
b.close()