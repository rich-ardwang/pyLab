from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64

key = bytes('pvjxzjmzvewfscft', encoding='UTF-8')
iv = bytes('qvibvaiwgouxwjeu', encoding='UTF-8')

def get_aes_cbc_base64_encode_string(password):
    aes = AES.new(key, AES.MODE_CBC, iv)
    padtext = pad(password.encode('utf-8'), 16, style='pkcs7')
    en_text = base64.b64encode(aes.encrypt(padtext))
    return en_text.decode('utf-8')

def get_aes_cbc_base64_decode_string(en_pass):
    aes = AES.new(key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(base64.b64decode(en_pass.encode('utf-8')))
    de_text = unpad(plaintext, 16, 'pkcs7')
    return de_text.decode('utf-8')

'''
password = 'abc593'
en_code = get_aes_cbc_base64_encode_string(password)
print("en_code: ", en_code)
de_code = get_aes_cbc_base64_decode_string(en_code)
print("de_code: ", de_code)
'''

if __name__ == '__main__':
    aes_cbc_b64_encodes = []
    with open('./weak-top1k.txt', 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
        for line in lines:
            aes_cbc_b64_encodes.append(get_aes_cbc_base64_encode_string(line)+'\r\n')

    with open('./weak_top1k_b64.txt', 'w', encoding='utf-8') as wf:
        wf.writelines(aes_cbc_b64_encodes)

