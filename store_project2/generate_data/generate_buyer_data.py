#یاد گرفتن ساخت دیتای رندوم. مثل یوزرنیم
# یاد گرفتن ساخت پسورد که شامل عدد و حرف و ....
#تکنیک تولید دیتای فیک
#و استفاده کزدن فایل کافینگ. ینی بیایم توی فایل کافینگم عدد مقدار دیتایی که میخوام تولید بشه رو تعیین کنم
#یاد گرفتن تکنیک ساخت دیتای رندوم یونیک
#داینامیک بودن ساخت و ایجاد دیتا


import random
import csv
import os  # برای بررسی وجود فایل

def generate_username(name_of_user):
    # Constraints
    minimum_capital_letter = 2
    minimum_special_char = 2
    minimum_digits = 2
    min_len_of_username = 8
    special_chars = ['@', '#', '$', '&']

    # remove space from name of user
    name_of_user = "".join(name_of_user.split()).lower()
    # calculate minimum characters that we need to take from name of user
    minimum_char_from_name = min_len_of_username - minimum_digits - minimum_special_char
    username = ""
    temp = 0
    for i in range(random.randint(minimum_char_from_name, len(name_of_user))):
        if temp < minimum_capital_letter:
            username += name_of_user[i].upper()
            temp += 1
        else:
            username += name_of_user[i]

    temp_list = []
    for i in range(minimum_digits):
        temp_list.append(str(random.randint(0, 9)))

    for i in range(minimum_special_char):
        temp_list.append(random.choice(special_chars))

    random.shuffle(temp_list)

    username += "".join(temp_list)

    return username

def generate_password(length=12):
    minimum_capital_letters = 2
    minimum_special_chars = 2
    minimum_digits = 2
    special_chars = ['@', '#', '$', '&', '%', '^', '&', '*']

    if length < (minimum_capital_letters + minimum_special_chars + minimum_digits):
        raise ValueError("Length is too short to meet the requirements")

    temp_list = []
    for _ in range(minimum_capital_letters):
        temp_list.append(chr(random.randint(65, 90)))

    for _ in range(minimum_digits):
        temp_list.append(str(random.randint(0, 9)))

    for _ in range(minimum_special_chars):
        temp_list.append(random.choice(special_chars))

    while len(temp_list) < length:
        temp_list.append(chr(random.randint(97, 122)))

    random.shuffle(temp_list)

    return ''.join(temp_list)

def generate_nationality_code(length=10):
    minimum_digits = 10

    if length < minimum_digits:
        raise ValueError("Length is too short to meet the requirements")

    temp_list = []
    for _ in range(minimum_digits):
        temp_list.append(str(random.randint(0, 9)))  # تولید 10 رقم به عنوان کد ملی

    return ''.join(temp_list)

if __name__ == "__main__":
    name_of_user = "Akshay Singh"

    # باز کردن یا ایجاد یک فایل CSV برای نوشتن نام کاربری‌ها و پسوردها
    file_exists = os.path.isfile("user_credentials.csv")  # بررسی وجود فایل
    with open("user_credentials.csv", "a", newline='') as file:
        writer = csv.writer(file)
        # نوشتن خط سرستون‌ها اگر فایل جدید باشد
        if not file_exists:
            writer.writerow(["Username", "Password", "Nationality Code"])  # برای ایجاد سرستون‌هاست

        for _ in range(50000):
            username = generate_username(name_of_user)
            password = generate_password()
            nationality_code = generate_nationality_code()
            writer.writerow([username, password, nationality_code])
            print(username, password, nationality_code)

