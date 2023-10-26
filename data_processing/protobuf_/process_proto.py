# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : process_proto.py
@Project  : common_tools
@Time     : 2023/10/10 9:57
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/10 9:57            1.0             Zhang ZiXu
"""
import json
import struct
from typing import Dict

import zs_protobuf


class ParseProto(object):

    @staticmethod
    def get_dynamic_wire_format(data, start, end):
        wire_type = data[start] & 0x7
        firstByte = data[start]
        if (firstByte & 0x80) == 0:
            field_number = (firstByte >> 3)
            return (start + 1, wire_type, field_number)
        else:
            byteList = []
            pos = 0
            while True:
                if start + pos >= end:
                    return (None, None, None)
                oneByte = data[start + pos]
                byteList.append(oneByte & 0x7F)
                pos = pos + 1
                if oneByte & 0x80 == 0x0:
                    break;

            newStart = start + pos

            index = len(byteList) - 1
            field_number = 0
            while index >= 0:
                field_number = (field_number << 0x7) + byteList[index]
                index = index - 1

            field_number = (field_number >> 3)
            return (newStart, wire_type, field_number)

    @staticmethod
    def retrieve_int(data, start, end):
        pos = 0
        byteList = []
        while True:
            if start + pos >= end:
                return (None, None, False)
            oneByte = data[start + pos]
            byteList.append(oneByte & 0x7F)
            pos = pos + 1
            if oneByte & 0x80 == 0x0:
                break

        newStart = start + pos

        index = len(byteList) - 1
        num = 0
        while index >= 0:
            num = (num << 0x7) + byteList[index]
            index = index - 1
        return (num, newStart, True)

    @staticmethod
    def parse_repeated_field(data, start, end, message, depth=0):
        while start < end:
            (num, start, success) = ParseProto.retrieve_int(data, start, end)
            if success == False:
                return False
            message.append(num)
        return True

    @staticmethod
    def parse_data(data, start, end, messages, depth=0):
        ordinary = 0
        while start < end:
            (start, wire_type, field_number) = ParseProto.get_dynamic_wire_format(data, start, end)
            if start == None:
                return False
            if wire_type == 0x00:  # Varint
                (num, start, success) = ParseProto.retrieve_int(data, start, end)
                if success == False:
                    return False
                messages['%02d:%02d' % (field_number, ordinary)] = num
                ordinary = ordinary + 1
            elif wire_type == 0x01:  # 64-bit
                num = 0
                pos = 7
                while pos >= 0:
                    # if start+1+pos >= end:
                    if start + pos >= end:
                        return False
                    # num = (num << 8) + ord(data[start+1+pos])
                    num = (num << 8) + data[start + pos]
                    pos = pos - 1

                # start = start + 9
                start = start + 8
                try:
                    floatNum = struct.unpack('d', struct.pack('q', int(hex(num), 16)))
                    floatNum = floatNum[0]
                except:
                    floatNum = None

                if floatNum != None:
                    messages['%02d:%02d' % (field_number, ordinary)] = floatNum
                else:
                    messages['%02d:%02d' % (field_number, ordinary)] = num

                ordinary = ordinary + 1


            elif wire_type == 0x02:  # Length-delimited
                # (stringLen, start, success) = retrieve_int(data, start+1, end)
                (stringLen, start, success) = ParseProto.retrieve_int(data, start, end)
                if success == False:
                    return False
                # stringLen = ord(data[start+1])
                messages['%02d:%02d' % (field_number, ordinary)] = {}
                if start + stringLen > end:  # pop failed result
                    messages.pop('%02d:%02d:embedded message' % (field_number, ordinary), None)
                    return False

                ret = ParseProto.parse_data(data, start, start + stringLen,
                                            messages['%02d:%02d' % (field_number, ordinary)], depth + 1)
                # print '%d:%d:embedded message' % (field_number, ordinary)
                if ret == False:
                    # print 'pop: %d:%d:embedded message' % (field_number, ordinary)
                    messages.pop('%02d:%02d:embedded message' % (field_number, ordinary), None)
                    # print messages
                    try:
                        data[start:start + stringLen].decode('utf-8')  # .encode('utf-8')
                        messages['%02d:%02d' % (field_number, ordinary)] = data[start:start + stringLen].decode(
                            'utf-8')
                    except:
                        messages['%02d:%02d' % (field_number, ordinary)] = []
                        ret = ParseProto.parse_repeated_field(data, start, start + stringLen,
                                                              messages['%02d:%02d' % (field_number, ordinary)],
                                                              depth + 1)
                        if ret == False:
                            messages.pop('%02d:%02d:repeated' % (field_number, ordinary), None)
                            # print traceback.format_exc()
                            hexStr = ['0x%x' % x for x in data[start:start + stringLen]]
                            hexStr = ':'.join(hexStr)
                            messages['%02d:%02d' % (field_number, ordinary)] = hexStr

                ordinary = ordinary + 1
                start = start + stringLen
            elif wire_type == 0x05:  # 32-bit
                num = 0
                pos = 3
                while pos >= 0:
                    if start + pos >= end:
                        return False
                    num = (num << 8) + data[start + pos]
                    pos = pos - 1
                start = start + 4
                try:
                    floatNum = struct.unpack('f', struct.pack('i', int(hex(num), 16)))
                    floatNum = floatNum[0]
                except:
                    floatNum = None
                if floatNum != None:
                    messages['%02d:%02d' % (field_number, ordinary)] = floatNum
                else:
                    messages['%02d:%02d' % (field_number, ordinary)] = num
                ordinary = ordinary + 1
            else:
                return False

        return True

    @staticmethod
    def parse_proto(data, fileName="", messages={}):
        if not data and fileName:
            data = open(fileName, "rb").read()
        size = len(data)
        ParseProto.parse_data(data, 0, size, messages)

    @staticmethod
    def gen_value_list(value):
        valueList = []
        # while value > 0:
        while value >= 0:
            oneByte = (value & 0x7F)
            value = (value >> 0x7)
            if value > 0:
                oneByte |= 0x80
            valueList.append(oneByte)
            if value == 0:
                break

        return valueList

    @staticmethod
    def write_value(value, output):
        byteWritten = 0
        # while value > 0:
        while value >= 0:
            oneByte = (value & 0x7F)
            value = (value >> 0x7)
            if value > 0:
                oneByte |= 0x80
            output.append(oneByte)
            byteWritten += 1
            if value == 0:
                break

        return byteWritten

    @staticmethod
    def write_var_int(field_number, value, output):
        byteWritten = 0
        wireFormat = (field_number << 3) | 0x00
        # output.append(wireFormat)
        # byteWritten += 1
        byteWritten += ParseProto.write_value(wireFormat, output)
        # while value > 0:
        while value >= 0:
            oneByte = (value & 0x7F)
            value = (value >> 0x7)
            if value > 0:
                oneByte |= 0x80
            output.append(oneByte)
            byteWritten += 1
            if value == 0:
                break

        return byteWritten

    @staticmethod
    def write_64_bit_float(field_number, value, output):
        byteWritten = 0
        wireFormat = (field_number << 3) | 0x01
        # output.append(wireFormat)
        # byteWritten += 1
        byteWritten += ParseProto.write_value(wireFormat, output)

        bytesStr = struct.pack('d', value).encode('hex')
        n = 2
        bytesList = [bytesStr[i:i + n] for i in range(0, len(bytesStr), n)]
        # i = len(bytesList) - 1
        # while i >= 0:
        #    output.append(int(bytesList[i],16))
        #    byteWritten += 1
        #    i -= 1
        for i in range(0, len(bytesList)):
            output.append(int(bytesList[i], 16))
            byteWritten += 1

        return byteWritten

    @staticmethod
    def write_64_bit(field_number, value, output):
        byteWritten = 0
        wireFormat = (field_number << 3) | 0x01
        byteWritten += ParseProto.write_value(wireFormat, output)
        # output.append(wireFormat)
        # byteWritten += 1

        for i in range(0, 8):
            output.append(value & 0xFF)
            value = (value >> 8)
            byteWritten += 1

        return byteWritten

    @staticmethod
    def write_32_bit_float(field_number, value, output):
        byteWritten = 0
        wireFormat = (field_number << 3) | 0x05
        # output.append(wireFormat)
        # byteWritten += 1
        byteWritten += ParseProto.write_value(wireFormat, output)

        bytesStr = struct.pack('f', value).encode('hex')
        n = 2
        bytesList = [bytesStr[i:i + n] for i in range(0, len(bytesStr), n)]
        # i = len(bytesList) - 1
        # while i >= 0:
        #    output.append(int(bytesList[i],16))
        #    byteWritten += 1
        #    i -= 1
        for i in range(0, len(bytesList)):
            output.append(int(bytesList[i], 16))
            byteWritten += 1

        return byteWritten

    @staticmethod
    def write_32_bit(field_number, value, output):
        byteWritten = 0
        wireFormat = (field_number << 3) | 0x05
        # output.append(wireFormat)
        # byteWritten += 1
        byteWritten += ParseProto.write_value(wireFormat, output)

        for i in range(0, 4):
            output.append(value & 0xFF)
            value = (value >> 8)
            byteWritten += 1

        return byteWritten

    @staticmethod
    def write_repeated_field(message, output):
        byteWritten = 0
        for v in message:
            byteWritten += ParseProto.write_value(v, output)
        return byteWritten

    @staticmethod
    def decode(binary):
        messages = {}
        ret = ParseProto.parse_data(binary, 0, len(binary), messages)

        if ret == False:
            return False

        return messages

    @staticmethod
    def re_encode(messages, output):
        byteWritten = 0
        # for key in sorted(messages.iterkeys(), key= lambda x: int(x.split(':')[0]+x.split(':')[1])):
        for key in sorted(messages.iterkeys(), key=lambda x: int(x.split(':')[1])):
            keyList = key.split(':')
            field_number = int(keyList[0])
            wire_type = keyList[2]
            value = messages[key]

            if wire_type == 'Varint':
                byteWritten += ParseProto.write_var_int(field_number, value, output)
            elif wire_type == '32-bit':
                if type(value) == type(float(1.0)):
                    byteWritten += ParseProto.write_32_bit_float(field_number, value, output)
                else:
                    byteWritten += ParseProto.write_32_bit(field_number, value, output)
            elif wire_type == '64-bit':
                if type(value) == type(float(1.0)):
                    byteWritten += ParseProto.write_64_bit_float(field_number, value, output)
                else:
                    byteWritten += ParseProto.write_64_bit(field_number, value, output)
            elif wire_type == 'embedded message':
                wireFormat = (field_number << 3) | 0x02
                byteWritten += ParseProto.write_value(wireFormat, output)
                index = len(output)
                tmpByteWritten = ParseProto.re_encode(messages[key], output)
                valueList = ParseProto.gen_value_list(tmpByteWritten)
                listLen = len(valueList)
                for i in range(0, listLen):
                    output.insert(index, valueList[i])
                    index += 1
                # output[index] = tmpByteWritten
                # print "output:", output
                byteWritten += tmpByteWritten + listLen
            elif wire_type == 'repeated':
                wireFormat = (field_number << 3) | 0x02
                byteWritten += ParseProto.write_value(wireFormat, output)
                index = len(output)
                tmpByteWritten = ParseProto.write_repeated_field(messages[key], output)
                valueList = ParseProto.gen_value_list(tmpByteWritten)
                listLen = len(valueList)
                for i in range(0, listLen):
                    output.insert(index, valueList[i])
                    index += 1
                # output[index] = tmpByteWritten
                # print "output:", output
                byteWritten += tmpByteWritten + listLen
            elif wire_type == 'string':
                wireFormat = (field_number << 3) | 0x02
                byteWritten += ParseProto.write_value(wireFormat, output)

                bytesStr = [int(elem.encode("hex"), 16) for elem in messages[key].encode('utf-8')]

                byteWritten += ParseProto.write_value(len(bytesStr), output)

                output.extend(bytesStr)
                byteWritten += len(bytesStr)
            elif wire_type == 'bytes':
                wireFormat = (field_number << 3) | 0x02
                byteWritten += ParseProto.write_value(wireFormat, output)

                bytesStr = [int(byte, 16) for byte in messages[key].split(':')]
                byteWritten += ParseProto.write_value(len(bytesStr), output)

                output.extend(bytesStr)
                byteWritten += len(bytesStr)

        return byteWritten

    @staticmethod
    def save_modification(messages, file_name):
        output = list()
        ParseProto.re_encode(messages, output)
        f = open(file_name, 'wb')
        f.write(bytearray(output))
        f.close()

    @staticmethod
    def pxprint(dict, indent=0):
        spaces = "    "
        for k, v in dict.items():
            if isinstance(v, Dict):
                print(spaces * (indent + 1) + f'"{k}": {{')
                ParseProto.pxprint(v, indent + 1)
                print(spaces * (indent + 1) + '}')
            else:
                try:
                    print(spaces * (indent + 1) + f'"{k}":"{v}"')
                except UnicodeEncodeError as e:
                    # python的终端打印不出多字节字符，会抛这个error，单独处理下，数据库要能存储才行，如mysql，则要设置编码[数据库和表都要设置]为utf8mb4_general_ci
                    print(spaces * (indent + 1) + f'"{k}":"error-v"')


if __name__ == '__main__':
    messages = {}
    file_path = r"C:\Users\JustZzer\Desktop\getPbCompressAd0-0"
    # ParseProto.parse_proto(None, file_path, messages)
    # print(messages)
    # ParseProto.pxprint(dict)

    file_content = open(file_path, "rb").read()
    print(file_content)

    data, mess_data = zs_protobuf.decode_message(file_content)
    print(json.dumps(data))
    print("= = =" * 10)
    print(json.dumps(mess_data))
