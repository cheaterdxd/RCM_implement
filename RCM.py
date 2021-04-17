from random import randint
from math import ceil
# khoi tao 1 hinh anh gia(fake) voi kich thuoc thoa man duoc do dai data can giau
def gen_random_matrix(pixel_size,data_len):
    pic_gen = []
    max_value = pow(2,8)
    for i in range(0,data_len+1):
        a_pixel = []
        for j in range(int(pixel_size/8)):
            a_pixel.append(randint(0,max_value))
        pic_gen.append(a_pixel)
    return pic_gen

def print_binary_of_pic(pic):
    for i in pic:
        s = ""
        for j in i:
            s += (int_to_8_bit(j)) + " "
        print(s)

def tranfome_pair_pixel(a,b):
    a_x = 2*(a) - (b)
    b_x = 2*(b) - (a)
    return (a_x,b_x)

def checkRCM(pixel_a:int, pixel_b:int, pixel_size=8)->bool:
    # max_value = pow(2,pixel_size)-1
    a_x,b_x = tranfome_pair_pixel(pixel_a,pixel_b)
    if(a_x>=0 and a_x<=255):
        if(b_x>=0 and b_x<=255):
            return True
    return False 

def lsb_of(x:int)->int:
    return (x%2)

def string_to_binary_string(string):
    s = ''
    for i in string:
        s += bin(ord(i))[2:].rjust(8,'0')
    return s

def int_to_8_bit(number):
    return bin(number)[2:].rjust(8,'0')

def pixel_to_int(pixel_list:list):
    s = ''
    for i in pixel_list:
        s += int_to_8_bit(i)
    # print(s)
    return int(s,2)

def int_to_pixel(int_pixel,pixel_size):
    '''
    chuyển 
    '''
    pixel_list = []
    s = bin(int_pixel)[2:].rjust(pixel_size,'0')
    for i in range(0,pixel_size,8):
        pixel_list.append(int(s[i:i+8],2))
    return pixel_list

def append_pair_data(a,b,pic):
    '''
    đưa cặp bytes vào ảnh
    '''
    pic.write(a.to_bytes(1,byteorder='little'))
    pic.write(b.to_bytes(1,byteorder='little'))

def embeded_data(pic,data_hide:str, water_mark_pic):
    is_success = False
    '''
    watermark data hide to pic
    '''
    '''
    bc1: tinh do dai cua du lieu watermark
    bc2: cong bit do dai vao dau thong tin watermark
    bc3: chen watermark vao theo lsb
    '''
    with open(pic,'rb') as pic, open(water_mark_pic, "wb") as out_file: # copy 54 bytes header
        header = pic.read(54) # write 54 byte header
        out_file.write(header)
        idx_of_hide = 0                                 # index của bit dữ liệu được giấu
        hide_in_binary = int_to_8_bit(len(data_hide))+ string_to_binary_string(data_hide) # chuyển dữ liệu được giấu sang dạng binary
        print(hide_in_binary)
        while True:           # lặp pixel theo cặp
            a = pic.read(1)     # read byte 1
            b = pic.read(1)     # read byte 2
            if a == b"":
                break
            print(f'a : {a} and b: {b}')
            # print(f"xet {a}:{int_value_a} va {b} ")
            if(idx_of_hide==len(hide_in_binary)):       # nếu giấu hết thì dừng duyệt pixel
                # append_pair_data(int_value_a,int_value_b,out_file)
                is_success=True
                out_file.write(a)
                out_file.write(b)
                break
            
            int_value_a = int.from_bytes(a,'little')
            int_value_b = int.from_bytes(b,'little')
            if(checkRCM(int_value_a,int_value_b)==True): # kiểm tra có thuộc vùng RCM
                print(f"dau bit {hide_in_binary[idx_of_hide]}")
                if(int_value_a%2==1 and int_value_b%2==1): # TH2 lsb(a,b) == (1,1)             
                    int_value_a -= 1
                    if(int(hide_in_binary[idx_of_hide],10)==0): # nếu bit watermark là bit 0 thì trừ lsb(b), còn không thì giữ nguyên 
                        int_value_b -= 1 # boi vi lsb(b) = 1
                    # append_pair_data(int_value_a,int_value_b,out_file)
                    out_file.write(int_value_a.to_bytes(1,byteorder='little'))
                    out_file.write(int_value_b.to_bytes(1,byteorder='little'))
                    print(f"ghi {a}:{int_value_a} va {int_value_b} ")
                else: # TH 1                
                    a_x,b_x = tranfome_pair_pixel(int_value_a,int_value_b)
                    if(a_x%2==0):       # set lsb(a) == 1
                        a_x +=1
                    if(b_x%2==0 and hide_in_binary[idx_of_hide]=="1"):
                        b_x+=1
                    if(b_x%2==1 and hide_in_binary[idx_of_hide]=="0"):
                        b_x-=1
                    # append_pair_data(a_x,b_x,out_file)
                    out_file.write(a_x.to_bytes(1,byteorder='little'))
                    out_file.write(b_x.to_bytes(1,byteorder='little'))
                    print(f"ghi {a}:{a_x} va {b_x} ")
                    print(f"tranform {a_x} va {b_x} ")  # in ra a . b sau khi đổi dạng theo công thức
            else: # Th3 : không lưu data hide mà hide_data += lsb(a)
                # set lsb(a) == 0              
                if(int_value_a%2==1):           
                    int_value_a -= 1
                    hide_in_binary += '1'       # lưu bit ban đầu của lsb(a) vào chuỗi hide
                else:
                    hide_in_binary += '0'       
                # append_pair_data(int_value_a,int_value_b,out_file)
                out_file.write(int_value_a.to_bytes(1,byteorder='little'))
                out_file.write(int_value_b.to_bytes(1,byteorder='little'))
                print(f"ghi {a}:{int_value_a} va {int_value_b} ")
                idx_of_hide -= 1
            # process next bit of hide data
            idx_of_hide+=1                      # tăng index của datahide lên 1 => tiépe tục mã hoá bit tiếp theo
        # while True:
        #     remain_byte = pic.read(1)
        #     if(remain_byte == b''):
        #         break
        #     out_file.write(remain_byte)
        if(is_success==False):
            print("++++++++++++++++ ERROR +++++++++++++++\nKhông thể thuỷ vân ảnh này")
        else:
            print(f"++++++++++++++++ SUCCESS ++++++++++++++\nBức ảnh đã được thuỷ vân,ảnh ra: {water_mark_pic}")
        remain_byte = pic.read()
        out_file.write(remain_byte)
        #done

def rcm_extract(a:int,b:int):
    '''
    a: bit a\n
    b: bit b\n
    return (bit_w (string type),a_ori,b_ori,true/false bit for th3)
    '''
    bit_w = ""
    print(f'xet a b : ({a} {b})')
    if(lsb_of(a)==1):
        bit_w = str(lsb_of(b))
        if(lsb_of(a)==1):
            a-=1
        if(lsb_of(b)==1):
            b-=1
        ori_a = ceil((2*a + b) / 3)
        ori_b = ceil((a + 2*b) / 3)
        return (bit_w,ori_a,ori_b,True)
    else:
        copy_of_a = a
        copy_of_b = b
        if(lsb_of(a)==0):
            a+=1
        if(lsb_of(b)==0):
            b+=1
        if(checkRCM(a,b)==True):
            bit_w = str(lsb_of(copy_of_b))
            return (bit_w,a,b,True)
        else:
            return (bit_w,copy_of_a,copy_of_b,False)

def extract_data(water_mark_pic,original_pic):
    test_pic = open('conmeo.bmp','rb')
    data_bit = ""
    size_bit = ""
    wait_idx_list = []
    data_size = 0
    size_process = True
    data_process = False
    # with open(water_mark_pic,"rb") as w_pic, open(original_pic,'wb') as o_pic:
    w_pic = open(water_mark_pic,"rb")
    o_pic = open(original_pic,'wb')  
    # copy 54 byte header
    o_pic.write(w_pic.read(54))
    # leak 8 bit len data 
    while True:
        a = w_pic.read(1)
        b = w_pic.read(1)
        int_a = int.from_bytes(a,'little')
        int_b = int.from_bytes(b,'little')
        w_bit,ori_a,ori_b,is_th3 = rcm_extract(int_a,int_b)
        current_a_pos = o_pic.tell()
        test_pic.seek(current_a_pos)
        print(f"pic ori: {test_pic.read(2)}")
        if(is_th3 != False):
            print(f"reform bytes: {ori_a.to_bytes(1,byteorder='little')} {ori_b.to_bytes(1,byteorder='little')} ")
        o_pic.write(ori_a.to_bytes(1,byteorder='little'))
        o_pic.write(ori_b.to_bytes(1,byteorder='little'))
        if(is_th3 == False): # save idx to wait_list
            wait_idx_list.append(current_a_pos) # save a_failed position
            continue
        print(f"extract bit {w_bit} ")            
        if(size_process == True):
            if(len(size_bit)<8):
                size_bit += w_bit
            else:
                size_process = False
                data_size = int(size_bit,2)
                data_process = True
        if(data_process == True):
            if(len(data_bit) < data_size*8):
                data_bit += w_bit
            else: # tra lai cac bit cho wait_list
                current_pos = o_pic.tell()
                if(len(wait_idx_list)>0):
                    '''
                    copy vi tri cua
                    '''
                    if(o_pic.mode!='rb+'): # chuyển mode
                        o_pic.close()
                        o_pic = open(original_pic,'rb+')  
                    idx = wait_idx_list.pop(0)                    
                    o_pic.seek(idx,0) # read phần trước bit sai
                    a_sai = o_pic.read(1) # read bit sai
                    int_a_sai = int.from_bytes(a_sai,'little')
                    print(f'a sai : {int_a_sai}')
                    # cong với bit_w thành bit a đúng
                    print(f'w_bit: {type(w_bit)} {w_bit}')
                    a_dung = (int_a_sai+int(w_bit,10))
                    a_temp = a_dung.to_bytes(1,byteorder='little')
                    o_pic.seek(idx,0) # đến trước vị trí bit a sai
                    o_pic.write(a_temp) # viết đè bit a sai
                    o_pic.seek(current_pos,0)
                else:
                    o_pic.seek(o_pic.tell()-2)
                    o_pic.write(a)
                    o_pic.write(b)
                    break # stop
    o_pic.write(w_pic.read()) # copy all remain bytes
    o_pic.close()
    w_pic.close()
    ascii_version_of_data = int(data_bit,2)
    ascii_version_of_data = ascii_version_of_data.to_bytes((ascii_version_of_data.bit_length()+7)//8,"big").decode()
    print("====================== CHÚC MỪNG CÁC BẠN =========================")
    print(f'\tData extract in binary: {data_bit} \n\tdata size: {data_size}')
    print(f"\tDcscii string: {ascii_version_of_data}")
    print(f'\tSize bit {size_bit} = {data_size}')
    print("============================ HACKED! =============================")

"""
def extract_data(water_mark_pic,output_picture):
    '''
    bc1: trích xuất các bit mô tả độ dài data trước
    bc2: từ độ dài data bắt đầu trích xuất đủ các bit data hide
    bc3: sau khi trích xuất đủ các bit data hide, thì trích xuất các bit để phục hồi các pixel ở TH3. 
    bc4: kết thúc sau khi list các pixel đợi phục hồi có size = 0
    '''
    watermark_bit = ""          # chua cac bit watermark ban dau trich xuat ra duoc
    size_bit = ""               # chua cac bit mô tả do dai cua watermark
    size_of_data = 0            # do dai cua watermark ban dau, tinh dc tu size_bit
    count_extract_bit = 0       # tổng so luong bit extract ra được trong quá trình extract
    size_bit_process = True     # đánh dấu có đang trong quá trình tách các bit mô tả độ dài
    count_get_bit = 0           # đếm các bit thực sự của watermark : chỉ có tác dụng cho quá trình test
    wait_to_restore_pixel = []  # FIFO idx list of pixel in TH3
    fixed_size_for_loop = len(water_mark_pic) if (len(water_mark_pic)%2==0) else len(water_mark_pic)-1
    with open(water_mark_pic,"rb") as w_pic, open(output_picture,"wb") as o_pic:
        
        o_pic.write(w_pic.read(54))
        while True:
            a_x = w_pic.read(1)
            b_x = w_pic.read(1)
            int_a_x = int.from_bytes(a_x,'little')
            int_b_x = int.from_bytes(b_x,'little')

            if(len(size_bit)==7):
                ''' kiem tra qua trinh tach lay size bit'''
                size_of_data = int(size_bit,2)
                print(f"size of data hide {size_of_data}")
                size_bit_process = False

            if(size_bit_process == False and count_extract_bit == size_of_data*8 and len(wait_to_restore_pixel) == 0):
                # TH nay khong con bit nao de extract
                o_pic.write(int_a_x.to_bytes(1,byteorder='little'))
                o_pic.write(int_b_x.to_bytes(1,byteorder='little'))
                continue
            if(int_a_x % 2 == 1): # TH : lsb(a') == 1
                print(f"co bit")
                '''
                TH2 : if lsb(a') == 1, w = lsb(b'), lsb(a') = lsb(b') = 0, re-tranforms 
                '''
                count_get_bit +=1
                if(int_value_a%2==1):
                    if(size_bit_process==True):
                        size_bit += str(int_b_x%2)
                    else:
                        if(count_extract_bit<size_of_data*8):
                            watermark_bit += str(int_b_x%2)
                            count_extract_bit += 1 # tăng tiến số kí tự
                        elif len(wait_to_restore_pixel) >0:
                            restore_idx_pixel = wait_to_restore_pixel.pop(0)        # FIFO list, pop out first element of list
                            o_pic.seek(restore_idx_pixel,0)
                            a = o_pic.read(1) # read current a
                            o_pic.write((a+int_b_x%2).to_bytes(1,byteorder='little')) # write correct a
                            # original_pic[restore_idx_pixel] += str(int_value_b%2)   # vi trong TH3: lsb(a') == 0, just add int_value_a with extracted bit
                    original_a = int((2*int_a_x + int_b_x) / 3)
                    original_b = int((int_a_x + 2*int_b_x) / 3)
                    o_pic.write(original_a.to_bytes(1,byteorder='little'))
                    o_pic.write(original_b.to_bytes(1,byteorder='little'))
            else: # TH lsb(a') == 0
                temp_value_of_b = int_b_x                   # save original b watermark bit
                int_a_x += 1                                # set lsb(a') == 1
                if(int_b_x%2==0):                           # if lsb(b') == 0, set to 1
                    int_b_x +=1                             # set lsb(b') == 1
                if(checkRCM(int_a_x,int_b_x)==True):
                    '''
                    TH 1: if lsb(a') =0, set [ lsb(a') = 1 & lsb(b') = 1 ](*) => if(a' & b' thuoc RCM)==true ? [w = lsb(b') ] and (a,b) = (a',b') at (*) 
                    '''
                    if(size_bit_process==True):
                        size_bit += str(int_b_x%2)
                    else:
                        if(count_extract_bit<size_of_data*8):
                            watermark_bit += str(int_b_x%2)
                            count_extract_bit += 1 # tăng tiến số kí tự
                        elif len(wait_to_restore_pixel) >0:
                            restore_idx_pixel = wait_to_restore_pixel.pop(0)        # FIFO list, pop out first element of list
                            o_pic.seek(restore_idx_pixel,0)
                            a = o_pic.read(1) # read current a
                            o_pic.write((a+int_b_x%2).to_bytes(1,byteorder='little')) 
                            #vi trong TH3: lsb(a') == 0, just add int_value_a with extracted bit write correct a
                else:
                    '''xet TH3: neu a,b khong thuoc RCM
                    luu tru a vao list wait, gia tri cua b = gia tri ban dau
                    '''
                    int_b_x = temp_value_of_b
                    wait_to_restore_pixel.append(w_pic.tell()-2) # get position befor bit a
                    o_pic.write(int_a_x.to_bytes(1,byteorder='little'))
                    o_pic.write(int_b_x.to_bytes(1,byteorder='little'))
    
    ''' copy remain bytes'''
    o_pic.write(w_pic.read())
    return (o_pic,watermark_bit)

    print(" ============ fake pic ==============")              
    fake_pic = gen_random_matrix(8,64)
    print(fake_pic)
    # print_binary_of_pic(fake_pic)
    print(" ============ hide value ==============")
    data = 't'
    print(string_to_binary_string(data))
    print ("==========================================")
    watermark = embeded_data(fake_pic,data,8)
    print(watermark)
    # print_binary_of_pic(watermark)
    original_pic , watermark_bit = extract_data(watermark,8)
    print ("================Extract==========================")
    print(original_pic)
    print(fake_pic == original_pic)
    print(watermark_bit)
    print(number_to_binary_string(2))
    print(pixel_to_int([123,123]))
    data = [1,2,3,4,5,6,8,7,75,24,55]
    for i,k in zip(data[0::2], data[1::2]):
        print(str(i), '+', str(k), '=', str(i+k))
"""

     