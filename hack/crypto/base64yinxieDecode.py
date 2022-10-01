import base64
import sys
b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python base64yinxieDecode.py <base64 file path>')
        sys.exit()

    with open(sys.argv[1], 'rb') as f:
        bin_str = ''
        for line in f.readlines():
            stegb64 = str(line, "utf-8").strip("\n")
            rowb64 = str(base64.b64encode(base64.b64decode(stegb64)), "utf-8").strip("\n")
            offset = abs(b64chars.index(stegb64.replace('=', '')[-1]) - b64chars.index(rowb64.replace('=', '')[-1]))
            equalnum = stegb64.count('=')  # no equalnum no offset
            if equalnum:
                bin_str += bin(offset)[2:].zfill(equalnum * 2)
            print(''.join([chr(int(bin_str[i:i + 8], 2)) for i in range(0, len(bin_str), 8)]))  # 8 位一组
