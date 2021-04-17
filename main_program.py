from RCM import *
from sys import argv
def usage_exit():
    usage = '''Usage: python watermark.py encode <raw_picture> <watermark_text> <watermark_picture>
       python watermark.py decode <watermark_picture> <output_picture>'''
    print(usage)
    exit(0)
if len(argv) < 2:
    usage_exit()
if argv[1] == 'encode' :
    try:
        picture = argv[2]
        text = argv[3]
        water_mark_name = argv[4]
        print(f"picture: {picture}, text: {text}")
    except:
        usage_exit()
    embeded_data(picture,text,water_mark_name)
if argv[1] == 'decode' :
    try:
        watermark_picture = argv[2]
        output_picture = argv[3]
        print(f"picture: {watermark_picture} original : {output_picture}") 
    except:
        usage_exit()
    extract_data(watermark_picture,output_picture)


# with open("conmeo.bmp",'rb') as output:
#     output.read(100)
#     print(output.read(20))
# with open("conmeo.bmp",'r') as output:
#     # output.read(54)
#     print(output.read(54).encode())
