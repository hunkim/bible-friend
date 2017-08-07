# -*- coding: utf-8 -*-
import requests
import json
import re
import difflib

# https://getbible.net/json?scrip=Acts%203:17-4;2:1

url = "https://getbible.net/json"

bible_name_dict = {
    '창': 'Gen',
    '창세기': 'Gen',
    'Gen': 50,

    '출': 'Exo',
    '출애굽기': 'Exo',
    'Exo': 40,

    '레': 'Lev',
    '레위기': 'Lev',
    'Lev': 27,

    '민': 'Num',
    '민수기': 'Num',
    'Num': 36,

    '신': 'Deu',
    '신명기': 'Deu',
    'Deu': 34,

    '수': 'Jos',
    '여호수아': 'Jos',
    'Jos': 24,

    '삿': 'Jdg',
    '사사기': 'Jdg',
    'Jdg': 21,

    '룻': 'Rut',
    '룻기': 'Rut',
    'Rut': 4,

    '삼상': '1sa',
    '사무엘상': '1sa',
    '1sa': 31,

    '삼하': '2sa',
    '사무엘하': '2sa',
    '2sa': 24,


    '왕상': '1ki',
    '열왕기상': '1ki',
    '1ki': 22,


    '왕하': '2ki',
    '열왕기하': '2ki',
    '2ki': 25,

    '대상': '1ch',
    '역대상': '1ch',
    '1ch': 29,

    '대하': '2ch',
    '역대하': '2ch',
    '2ch': 36,

    '스': 'Ezr',
    '에스라': 'Ezr',
    'Ezr': 10,

    '느': 'Neh',
    '느헤미야': 'Neh',
    'Neh': 13,

    '에': 'Est',
    '에스더': 'Est',
    'Est': 10,

    '욥': 'Job',
    '욥기': 'Job',
    'Job': 42,

    '시': 'Psa',
    '시편': 'Psa',
    'Psa': 150,

    '잠': 'Pro',
    '잠언': 'Pro',
    'Pro': 31,

    '전': 'Ecc',
    '전도서': 'Ecc',
    'Ecc': 12,

    '아': 'Sol',
    '아가': 'Sol',
    'Sol': 8,

    '사': 'Isa',
    '이사야': 'Isa',
    'Isa': 66,

    '렘': 'Jer',
    '예레미야': 'Jer',
    'Jer': 52,

    '애': 'Lam',
    '예레미야애가': 'Lam',
    'Lam': 5,

    '겔': 'Eze',
    '에스겔': 'Eze',
    'Eze': 48,

    '단': 'Dan',
    '다니엘': 'Dan',
    'Dan': 12,

    '호': 'Hos',
    '호세아': 'Hos',
    'Hos': 14,

    '욜': 'Joe',
    '요엘': 'Joe',
    'Joe': 3,

    '암': 'Amo',
    '아모스': 'Amo',
    'Amo': 9,

    '옵': 'Oba',
    '오바다': 'Oba',
    'Oba': 1,

    '욘': 'Jon',
    '요나': 'Jon',
    'Jon': 4,

    '미': 'Mic',
    '미가': 'Mic',
    'Mic': 7,

    '나': 'Nah',
    '나훔': 'Nah',
    'Nah': 3,

    '합': 'Hab',
    '하박국': 'Hab',
    'Hab': 3,

    '습': 'Zep',
    '스바냐': 'Zep',
    'Zep': 3,

    '학': 'Hag',
    '학개': 'Hag',
    'Hag': 2,

    '슥': 'Zec',
    '스가랴': 'Zec',
    'Zec': 14,

    '말': 'Mal',
    '말라기': 'Mal',
    'Mal': 4,

    '마': 'Mat',
    '마태': 'Mat',
    '마태복음': 'Mat',
    'Mat':    28,

    '막': 'Mar',
    '마가': 'Mar',
    '마가복음': 'Mar',
    'Mar':    16,

    '눈': 'Luk',
    '누가': 'Luk',
    '누가복음': 'Luk',
    'Luk': 24,

    '요': 'John',
    '요한': 'John',
    '요한복음': 'John',
    'John': 21,

    '사도': 'Act',
    '행': 'Act',
    '사도행전': 'Act',
    'Act': 28,

    '롬': 'Rom',
    '로마': 'Rom',
    '로마서': 'Rom',
    'Rom': 16,

    '고전': '1co',
    '고린도전서': '1co',
    '1co': 16,

    '고후': '2co',
    '고린도후서': '2co',
    '2co': 13,

    '갈': 'Gal',
    '갈라디아서': 'Gal',
    'Gal': 6,

    '엡': 'Eph',
    '에베소서': 'Eph',
    'Eph': 6,

    '빌': 'Phi',
    '빌립보서': 'Phi',
    'Phi': 4,

    '골': 'Col',
    '골로새서': 'Col',
    'Col': 4,

    '살전': '1th',
    '데살로니가전서': '1th',
    '1th': 5,

    '살후': '2th',
    '데살로니가후서': '2th',
    '2th': 3,

    '딤전': '1ti',
    '디모데전서': '1ti',
    '1ti': 6,

    '딤후': '2ti',
    '디모데후서': '2ti',
    '2ti': 4,


    '딛': 'Tit',
    '디도서': 'Tit',
    'Tit': 3,


    '몬': 'Phm',
    '빌레몬서': 'Phm',
    'Phm': 1,

    '히': 'Heb',
    '히브리서': 'Heb',
    'Heb': 13,

    '약': 'Jam',
    '야고보서': 'Jam',
    'Jam': 5,

    '벧전': '1pe',
    '베드로전서': '1pe',
    '1pe': 5,

    '벧후': '2pe',
    '베드로후서': '2pe',
    '2pe': 3,

    '요일': '1jo',
    '요한일서': '1jo',
    '1jo': 5,

    '요이': '2jo',
    '요한이서': '2jo',
    '2jo': 1,

    '요3': '3jo',
    '요삼': '3jo',
    '요한삼서': '3jo',
    '3jo': 1,

    '유': 'Jud',
    '유다서': 'Jud',
    'Jud': 1,

    '계': 'Rev',
    '요한계시록': 'Rev',
    '계시록': 'Rev',
    'Rev': 22
}


def bookname_eng(book='계32'):
    book = book.replace(" ", "")
    m = re.search("\d", book)

    if m:
        book_name = book[:m.start()]
        rest = book[m.start():]

    else:
        book_name = book
        rest = "1"

    # Exact match
    if book_name in bible_name_dict:
        return str(bible_name_dict[book_name]) + rest
    else:  # https://stackoverflow.com/questions/10018679
        book_keys = bible_name_dict.keys()
        close_name = difflib.get_close_matches(book_name, book_keys, n=1)
        if close_name:
            return str(bible_name_dict[close_name[0]]) + rest

    return None


def json_txt(bible_json):
    res = ""
    if 'book' in bible_json:
        for book_ref in bible_json['book']:
            for chapter in book_ref['chapter']:
                res += chapter + ": " + \
                    book_ref['chapter'][chapter]['verse'] + "\n"
    elif 'chapter' in bible_json:
        for chapter in bible_json['chapter']:
            res += chapter + ": " + \
                bible_json['chapter'][chapter]['verse'] + "\n"
    else:
        return None

    return res


def get_bible(script="요한 3:16", translation='korean'):
    # Get English name from Korean bible names
    p = bookname_eng(script)
    if p is None:
        return script + " 찾지 못했습니다."

    data = {'p': p,
            'translation': translation}

    response = requests.get(url, params=data)
    print(response.url)
    res_code = response.status_code

    if res_code is not 200:
        print("Error Code:" + str(res_code))
        return script + " 찾기에 문제가 발생했습니다."

    res_txt = response.text.strip('();')

    if res_txt.startswith('NULL'):
        return script + " 은 없습니다."

    print(res_txt)
    res_json = json.loads(res_txt)

    bible_txt = json_txt(res_json)
    return bible_txt

if __name__ == "__main__":
    print(bookname_eng("요3:16"))
    print(bookname_eng("계 3:16"))
    print(bookname_eng("요한복 3:16"))
    print(bookname_eng("데살로 3:16"))
    print(bookname_eng("김성훈 3:16"))
    print(bookname_eng("요한"))

    print(get_bible(script="요3:16"))
    print(get_bible(script="요3:116"))
    print(get_bible(script="시편119"))
    print(get_bible(script="요한복음3:16"))
    print(get_bible(script="마태3:16"))
    print(get_bible(script="마3:16"))
    print(get_bible(script="요한계3:16"))
