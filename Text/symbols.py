from Text import vietnamese_phonemes


_pad = "_"
_punctuatuion = "!'(),.:?"
_special = "-"
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_letters_vi = 'aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵz'

_silences = ["@sp", "@spn", "@sil"]

# Thêm "@" vào các ký hiệu vietnamese_phonemes để đảm bảo tính duy nhất (một số giống như chữ in hoa):
_vietnamese_phonemes = ["@" + s for s in vietnamese_phonemes.valid_symbols]

# Export all symbols:
symbols_vi = (
    [_pad]
    + list(_special)
    + list(_punctuatuion)
    + _vietnamese_phonemes
    +_silences
)


def get_symbols(vi_lang=False):
    return symbols_vi
#    else:
#        return symbols*/

