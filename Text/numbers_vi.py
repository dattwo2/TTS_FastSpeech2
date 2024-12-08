import re

# dinh nghia cac yeu to can thiet
_UNITS = ["mươi", "trăm", "nghìn", "mươi", "trăm", "triệu", "mươi", "trăm", "tỷ"]
_LETTERS = {"0":"không", "1":"một", "2":"hai", "3":"ba", "4":"bốn","5":"năm","6":"sáu", "7":"bảy", "8":"tám", "9":"chín"}

_comma_number_re = re.compile(r'([0-9][0-9\.]+[0-9])')
_full_date_re = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{1,4})')
_short_date_re = re.compile(r'(\d{1,2})/(\d{1,2})')
_full_time_re = re.compile(r'(\d+):(\d{1,2}):(\d+(?:,\d+)?)')
_short_time1_re = re.compile(r'(\d+):(\d{1,2})')
_short_time2_re = re.compile(r'(\d+)h(\d{1,2})')
_general_number_re = re.compile(r'(-?\+?\d+(?:,\d+)?e?\d*(?:,\d+)?)(kg/m3|rad/s|km/h|l/km|m3/s|w/m2|m/s|vnd|rad|mol|km|kg|kb|mb|gb|tb|°c|ºc|°k|ºk|mg|mm|cm|dm|ma|hz|mw|kw|kj|tj|kv|lm|pa|va|m2|m3|kω|mω|ev|d|m|g|k|b|s|a|w|j|v|f|n|l|h|ω|t|°|º|%)?')
_roman_re = re.compile(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b')
_coner_re = re.compile(r'(\d+)°(\d+)′(\d+(?:,\d+)?)″')
_number_range_re = re.compile(r'(\d+(?:,\d+)?)\s*[-–-]\s*(\d+(?:,\d+)?)')
_whitespace_re = re.compile(r'\s+')


def unintStr2Str(input:str, isSingle=False):
    result =""

    if isinstance(input,str) and len(input)>0:
        #neu chi la lay cac chu so thong thuong
        if isSingle==True:
            for c in input:
                if (c in _LETTERS):
                    result += " "+_LETTERS[c]
                else:
                    result = ""
                    break
        # khong thi thuc hien chuyen so sang chu
        else:
            # strip leading zero
            if (len(input)>1):
                input = input.lstrip('0')
            # kiem tra do dai input sau khi loai tru so 0 o dau chuoi
            if input is None or len(input)==0:
                return "không"
            inputLength = len(input)
            # dem ki tu
            idx = 0
            for c in input:
                if (c in _LETTERS):
                    bilCount = (inputLength -1 - idx) //9
                    # xac dinh hang don vi
                    unitIdx = (inputLength -2 - idx) % len(_UNITS)
                    if unitIdx <0:
                        unitIdx = len(_UNITS) -1
                    # chu so va don vi hien tai
                    num = _LETTERS[c]
                    unit = _UNITS[unitIdx]
                    # xem xet hang don vi truoc
                    if idx ==inputLength -1:
                        unit = None
                        if c=='0':
                            if idx>0:
                                num = None
                        elif c == '1':
                            if idx>0 and input[idx-1] != "1" and input[idx-1] != '0':
                                num = "mốt"
                        elif c == '4':
                            if idx>0 and input[idx-1]!='1' and input[idx-1]!='0':
                                num ="tư"
                        elif c == '5':
                            if idx>0 and input[idx-1] !='0':
                                num = "lăm"
                    # xem xet so tai cac vi tri khac
                    else:
                        if unitIdx==0 or unitIdx==3 or unitIdx==6:
                            if c=='0':
                                if idx+1 < inputLength and input[idx+1]!='0':
                                    num = "linh"
                                    unit = None
                                else:
                                    num = None
                                    unit = None
                            elif c=='1':
                                num = "mười"
                                unit = None
                        elif unitIdx==1 or unitIdx==4 or unitIdx==7:
                            if c=='0' and idx+2 <inputLength and input[idx+1]=='0' and input[idx+2]=='0':
                                num = None
                                unit = None
                        elif unitIdx==2 or unitIdx==5 or unitIdx==8:
                            # sua don vi nghin/trieu/ty ty
                            if bilCount>0 and unitIdx==8 and (idx<2 or input[idx-1]!='0' or input[idx-2]!=0):
                                for i in range(0, bilCount -1):
                                    unit += "tỷ"
                            if idx>0:
                                if c=='0':
                                    num = None
                                    if unitIdx !=8:
                                        if idx>1 and input[idx-1]=='0' and input[idx-2]=='0':
                                            unit = None
                                elif c == '1':
                                    if input[idx - 1] != "1" and input[idx - 1] != '0':
                                        num = "mốt"
                                elif c == '4':
                                    if input[idx - 1] != '1' and input[idx - 1] != '0':
                                        num = "tư"
                                elif c == '5':
                                    if input[idx - 1] != '0':
                                        num = "lăm"
                            if unit is not None:
                                pass
                        # them so vao ket qua
                        if num is not None:
                            result += " " +num
                        # them don vi vao ket qua
                        if unit is not None:
                            result += " " + unit
                else:
                    result = ""
                    break
                # tan bien dem
                idx +=1
    # tra ve ket qua
    return result.strip()


def floatStr2Str (input:str, dot=',', isPoweredNumber=False):
    result = ""
    if len(input)>0:
        signStr = ""
        if input[0] == "-":
            if isPoweredNumber==True:
                signStr = "trừ "
            else:
                signStr = "âm "
            input = input[1:]
        elif input[0] == '+':
            signStr = "dương "
            input = input[1:]
        parts = input.split(dot)
        if len(parts)>1:
            single = True
            if len(parts)>1:
                single = False
                result = signStr + unintStr2Str(parts[0]) + " phẩy " + unintStr2Str(parts[1], single)
            else:
                result = signStr + unintStr2Str(parts[0])
    return result


def doubleStr2Str(input:str,dot=","):
    input = input.lower()
    parts = input.split("e")
    if len(parts)>1:
        return floatStr2Str(parts[0],dot) + " nhân mười mũ " + floatStr2Str(parts[1],dot,True)
    else:
        return floatStr2Str(parts[0])


# replace 00/00/0000
def _replace_full_date(m):
    return " ngày" + doubleStr2Str(m.group(1)) + " tháng" + doubleStr2Str(m.group(2)) + " năm " + doubleStr2Str(m.group(3)) + " "


#replace 00/00
def _replace_short_date(m):
    return " ngày" + doubleStr2Str(m.group(1)) + " tháng" + doubleStr2Str(m.group(2)) + " "


#replace 000:00:00

def _replace_full_time(m):
    return " " + doubleStr2Str(m.group(1)) + " giờ" + doubleStr2Str(m.group(2)) + " phút " + doubleStr2Str(m.group(3)) + " giây "


#replace 000:00
def _replace_short_time1(m):
    return " " + doubleStr2Str(m.group(1)) + " giờ" + doubleStr2Str(m.group(2)) + " phút "


#replace 000h00
def _replace_short_time2(m):
    return " " + doubleStr2Str(m.group(1)) + " giờ" + doubleStr2Str(m.group(2)) + " phút "


def _replace_number_range(m):
    return " từ " + m.group(1) + " đến" + m.group(2)


def _replace_coner(m):
    return " " + doubleStr2Str(m.group(1)) + " độ " + doubleStr2Str(m.group(2)) + " phút " + doubleStr2Str(m.group(3)) + " giây "


def _replace_number(m):
    if (len(m.group())>1 and m.group(2) is not None):
        orgUnit = m.group(2)
        unit = "" #vnd|d|m|kg|g|k|b|kb|mb|gb|tb|°c|°k
        if orgUnit == 'vnd' or orgUnit == 'd':
            unit = 'đồng'
        elif orgUnit == 'km':
            unit = 'kilô mét'
        elif orgUnit == 'm':
            unit = 'mét'
        elif orgUnit == 'dm':
            unit = ' đềxi mét'
        elif orgUnit == 'cm':
            unit = 'xenti mét'
        elif orgUnit == 'kg':
            unit = 'kilô gram'
        elif orgUnit == 'g':
            unit = 'gram'
        elif orgUnit == 'mg':
            unit = 'mili gram'
        elif orgUnit == 'k':
            unit = 'nghìn'
        elif orgUnit == 'b':
            unit = 'bai'
        elif orgUnit == 'kb':
            unit = 'kilô bai'
        elif orgUnit == 'mb':
            unit = 'mêga bai'
        elif orgUnit == 'gb':
            unit = 'giga bai'
        elif orgUnit == 'tb':
            unit = 'tera bai'
        elif orgUnit == '°c' or orgUnit == 'ºc':
            unit = 'độ xê'
        elif orgUnit == '°k' or orgUnit == 'ºk':
            unit = 'độ kenvin'
        elif orgUnit == 's':
            unit = 'giây'
        elif orgUnit == 'a':
            unit = 'ampe'
        elif orgUnit == 'ma':
            unit = 'mili ampe'
        elif orgUnit == 'hz':
            unit = 'héc'
        elif orgUnit == 'w':
            unit = 'oắt'
        elif orgUnit == 'kw':
            unit = 'kilô oắt'
        elif orgUnit == 'mw':
            unit = 'mêga oát'
        elif orgUnit == 'j':
            unit = 'giun'
        elif orgUnit == 'kj':
            unit = 'kilô giun'
        elif orgUnit == 'tj':
            unit = 'tera giun'
        elif orgUnit == 'v':
            unit = 'vôn'
        elif orgUnit == 'kv':
            unit = 'kilô vôn'
        elif orgUnit == 'lm':
            unit = 'lumen'
        elif orgUnit == 'pa':
            unit = 'pátcan'
        elif orgUnit == 'rad':
            unit = 'rađian'
        elif orgUnit == 'va':
            unit = 'vôn ampe'
        elif orgUnit == 'km/h':
            unit = 'kilô mét trên giờ'
        elif orgUnit == 'm/s':
            unit = 'mét trên giây'
        elif orgUnit == 'f':
            unit = 'phara'
        elif orgUnit == 'n':
            unit = 'niutơn'
        elif orgUnit == 'm2':
            unit = 'mét vuông'
        elif orgUnit == 'm3':
            unit = 'mét khối'
        elif orgUnit == 'l':
            unit = 'lít'
        elif orgUnit == 'rad/s':
            unit = 'rađian trên giây'
        elif orgUnit == 'l/km':
            unit = 'lít trên kilômét'
        elif orgUnit == 'kg/m3':
            unit = 'kilôgram trên mét khối'
        elif orgUnit == 'm3/s':
            unit = 'mét khối trên giây'
        elif orgUnit == 'h':
            unit = 'henri'
        elif orgUnit == 'w/m2':
            unit = 'oát trên mét vuông'
        elif orgUnit == 'mol':
            unit = 'mon'
        elif orgUnit == 'ω':
            unit = 'ôm'
        elif orgUnit == 'kω':
            unit = 'kilô ôm'
        elif orgUnit == 'mω':
            unit = 'mêga ôm'
        elif orgUnit == 't':
            unit = 'tấn'
        elif orgUnit == '°' or orgUnit == 'º':
            unit = 'độ'
        elif orgUnit == 'ev':
            unit = 'êlêctrôn vôn'
        elif orgUnit == '%':
            unit = 'phần trăm'
        return " " + doubleStr2Str(m.group(1)) + " " + unit + " "
    else:
        return " " + doubleStr2Str(m.group(1)) + " "


def _remove_commas(m):
    return m.group(1).replace('.','')


def _expand_roman(m):
    roman_numerals = {'I':1,'V':5,'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    result = 0
    num = m.group(0)
    for i,c in enumerate(num):
        if (i+1) == len(num) or roman_numerals[c] >= roman_numerals[num[i+1]]:
            result += roman_numerals[c]
        else:
            result -= roman_numerals[c]
    return str(result)


def normalize_numbers(text:str):
    #roman number
    text = re.sub(_roman_re, _expand_roman, text)
    #range
    text = re.sub(_number_range_re,_replace_number_range, text)
    #lower
    text = text.lower()
    #remove comma
    text = re.sub(_comma_number_re,_remove_commas,text)
    #full date
    text = re.sub(_full_date_re,_replace_full_date, text)
    text = re.sub(_short_date_re,_replace_short_date, text)
    #full time
    text = re.sub(_full_time_re,_replace_full_time, text)
    text = re.sub(_short_time1_re,_replace_short_time1, text)
    text = re.sub(_short_time2_re,_replace_short_time2, text)
    #coner
    text = re.sub(_coner_re,_replace_coner, text)
    # number and unit
    text = re.sub(_general_number_re, _replace_number, text)
    #return result
    return re.sub(_whitespace_re,' ',text)
