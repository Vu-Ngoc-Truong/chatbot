#!/usr/bin/env python3

text_test = """Cá kho là món ăn truyền thống của Việt Nam, được làm từ cá phi lê hoặc cá lóc thường được ướp với nước mắm, đường, tỏi, hành, ớt và nấu chín trong nồi đất. Sau đây là nguyên liệu cơ bản để làm món cá kho:

500g cá phi lê hoặc cá lóc
3-4 muỗng canh nước mắm
2-3 muỗng canh đường
2-3 tép tỏi băm nhuyễn
1 củ hành tím băm nhuyễn
1-2 trái ớt đỏ băm nhuyễn hoặc cắt nhỏ
1 thìa cà phê nước mắm
1 thìa cà phê dầu ăn
1/2-1 cốc nước lọc
Cách mạng 4.0
Ngọn núi cao 6.354 mét
Lưu ý: Nguyên liệu trên chỉ là nguyên liệu cơ bản để làm món cá kho, tùy theo khẩu vị mỗi người có thể thêm bớt gia vị để tạo ra món ăn phù hợp với sở thích."""

# def count_up_to(n):
#     count = 1
#     while count <= n:
#         yield count
#         count += 1

# num = count_up_to(5)
# print(type(num))
# print(list(num))

def process_string(string):
    result = ""
    for char in string:
        if char in ".!?:;\n":
            result = result + char
            return result
        else:
            result = result + char
    return ""

result = ""
last_len= len(result)
count = 5
last_event_msg = ""
last_len_msg = len(last_event_msg)
while True :
    # user_input = input("Nhập vào một chuỗi: ")
    count +=5
    if count >= len(text_test):
        count = len(text_test) -1
    if count < len(text_test):
        user_input = text_test[:count]

    if ("exit" in user_input):
        break

    # result = result + process_string(user_input[last_len:])
    # if last_len < len(result):
    #     last_len = len(result)
        # print("Kết quả: ", result)

    full_event_message = user_input
    if len(full_event_message) > last_len_msg:
        chunk = full_event_message[last_len_msg:]
        last_event_msg = last_event_msg + process_string(chunk)
        current_len_msg = len(last_event_msg)
        if last_len_msg < current_len_msg:
            chunk = full_event_message[last_len_msg:current_len_msg]
            last_len_msg = current_len_msg
            print("#$___",chunk)
        # If finish answer
        if count == len(text_test) -1:
            print("$EoF_",chunk)
    if count >= len(text_test) -1:
        break
