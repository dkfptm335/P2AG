import pandas as pd
import time
import re
import requests
import bs4
import difflib

from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

    

# Input     : bangchim attrubute, siblings list, check list
# Output    : updated check list
  
def check_siblings(bangchim_attrs, siblings, check_list):

    for near_bangchim in siblings:
        if type(near_bangchim) is bs4.element.NavigableString:
            continue
        
        if type(near_bangchim) is bs4.element.Comment:
            continue
        
        if near_bangchim == None:
            continue
        
        if near_bangchim.name == 'br':
            continue
        
        if 'wrapped' in bangchim_attrs:
            if ( near_bangchim.name != bangchim_attrs['parent_name'] ):
                check_list['differ_struct'] = True
                
            if 'parent_class' in bangchim_attrs:
                if 'class' in near_bangchim.attrs:
                    if near_bangchim.attrs['class'][0] != bangchim_attrs['parent_class']:
                        check_list['differ_parent_class'] = True
                else:
                    check_list['differ_parent_class'] = True
                    
                if bangchim_attrs['parent_name'] == 'strong':
                    check_list['triple_struct'] = 'strong'
            
            near_bangchim = near_bangchim.a

        if 'style' in bangchim_attrs:
            if 'style' not in near_bangchim.attrs:
                check_list['differ_style'] = True
            elif near_bangchim.attrs['style'] != bangchim_attrs['style']:
                check_list['differ_style'] = True
        
        if 'class' in bangchim_attrs:
            if 'class' not in near_bangchim.attrs:
                check_list['differ_class'] = True
            elif near_bangchim.attrs['class'][0] != bangchim_attrs['class']:
                check_list['differ_class'] = True
        
        if 'span' in bangchim_attrs:
            if near_bangchim.find('span'):
                check_list['differ_span'] = False
            else:
                check_list['differ_span'] = True
                
        if 'bold' in bangchim_attrs:
            if near_bangchim.find('b'):
                check_list['differ_bold'] = False
            else:
                check_list['differ_bold'] = True
                
        if 'strong' in bangchim_attrs:
            if near_bangchim.find('strong'):
                check_list['differ_strong'] = False
            else:
                check_list['differ_strong'] = True
                    

        
    return check_list
    
# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 

# Input     : url
# Output    : updated check list

def check_bangchim_highlighted(url): 
    
    try:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        response = requests.get(url, headers=headers, verify=False)
    except Exception as e:
        print(f"\n[Error] SSLError : {e}\n")
        return -1
    
    bss = bs(response.text, 'html.parser')

    datas = bss.find_all('a')

    bangchim = None
    for data in reversed(datas):
        if ( '개인정보' in data.get_text() ) & ( '처리방침' in data.get_text() ):
            bangchim = data
            break


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    check_point_num = 5

    bangchim_attrs = {}

    if bangchim:
        
        if len(bangchim.parent.find_all('a')) == 1:
            siblings_area = bangchim.parent
            bangchim_attrs['wrapped'] = True
            bangchim_attrs['parent_name'] = bangchim.parent.name
            
            if 'class' in bangchim.parent.attrs:
                bangchim_attrs['parent_class'] = bangchim.parent.attrs['class'][0]
        else:
            siblings_area = bangchim
        
        if 'style' in bangchim.attrs:
            pattern = r'color:.((.*?;)|(#[0-9a-f]{6}))'
            match = re.search(pattern, bangchim.attrs['style'])
            if match:
                bangchim_attrs['style'] = match.group(1)
            
        if 'class' in bangchim.attrs:
            bangchim_attrs['class'] = bangchim.attrs['class'][0]

        if bangchim.find('span'):
            bangchim_attrs['span'] = True
            
        if bangchim.find('b'):
            bangchim_attrs['bold'] = True
            
        if bangchim.find('strong'):
            bangchim_attrs['strong'] = True
    else:
        print("\n(Unexpected Result) : No bangchim\n")
        return False


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    check_list = {}

    check_list = check_siblings(bangchim_attrs, siblings_area.previous_siblings, check_list)
    check_list = check_siblings(bangchim_attrs, siblings_area.next_siblings, check_list)

    if 'differ_struct' in check_list:
        return True
    
    if 'differ_style' in check_list:
        return True
    
    if 'differ_class' in check_list:
        return True
    
    if 'differ_parent_class' in check_list:
        return True
    
    if 'differ_span' in check_list:
        return True
    
    if 'differ_bold' in check_list:
        return True
    
    if 'differ_strong' in check_list:
        return True
    
    return False


def extract_bangchim(url_example):

    start = time.time()

    origin = ''
    saved = ''
    max_prior = 0
    min_level = 9999
    least = 999
            
    try:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        
        response = requests.get(url_example, headers=headers, verify=False)
        after_encode = response.content.decode('utf-8', 'replace')
        bss = bs(after_encode, 'html.parser')

        data = bss.find_all("div")
        
        if len(data) == 0:
            print("No div tag")
            pass
        # if end
        else:
            for idx in range(0, len(data)):
                
                prior = 0
                sector = data[idx].get_text()
                
                if len(sector) < 5000:
                    continue
                
                word1 = 9999
                word1s = ['개인정보처리방침', '개인정보 처리방침', '개인정보 보호정책', "개인정보 취급방침"]
                for word in word1s:
                    tmp_idx = sector.find(word)
                    if tmp_idx == -1:
                        pass
                    elif tmp_idx < word1:
                        word1 = tmp_idx
                
                if word1 == 9999:
                    continue
                prior += 1 if word1 < 50 else 0
                
                word2 = sector.find('수집')
                prior += 1 if word2 != -1 else 0

                pattern = r'\(.*?이하.*?\)'
                match = re.search(pattern, sector)
                if match:
                    word3 = match.start()
                else:
                    word3 = -1
                prior += 1 if (word3 < 500) & (word3 != -1) else 0
                    
                word4 = sector.find('3자')
                prior += 1 if word4 != -1 else 0
                
                word5 = sector.find('위탁')
                prior += 1 if word5 != -1 else 0
                
                if prior < max_prior:
                    continue    # skip
                elif prior > max_prior:
                    max_prior = prior   # update
                elif (len(sector) < min_level) & (len(sector) > least):
                    pass
                else:
                    continue
                
                min_level = len(sector)
                saved = sector
                origin = str(data[idx])
                # check
                    
        # else end
    # try end
    except Exception as e:
        print("Exception occured")
        saved = f"url : {url_example}, error: {e}"
    
    end = time.time()
    print(f"[Log] (func)/extract_bangchim Run Time : {(end - start):.4f} sec\n")
    
    return saved, origin


# Input     : string
# Output    : category tag number

def classify_category(string_example):
    
    # 길면 검색 효율 낮음 + 제목 아닐 가능성 높음
    
    # 제n조, 괄호는 불필요하니 제거
    pattern = r'(제[0-9 ]+조)?[ \.]{0,2}\(?([^\)]+)\)?'
    match = re.search(pattern, string_example)
    if match:
        string_example = match.group(2)
    
    
    if ('목적' in string_example) & ('항목' in string_example) & ('기간' in string_example):
        return 16, 100
    elif ('항목' not in string_example) & ('목적' in string_example) & ('기간' in string_example):
        return 17, 100
    elif ('항목' in string_example) & ('목적' in string_example) & ('기간' not in string_example):
        return 18, 100
    elif ('항목' in string_example) & ('목적' not in string_example) & ('기간' in string_example):
        return 19, 100
    elif ('목적' in string_example):
        return 2, 100
    elif ('기간' in string_example):
        return 3, 100
    elif ('항목' in string_example):
        return 4, 100
    
    if ('파기' in string_example):
        return 5, 100
    
    if ('정보주체' in string_example) & ('권리' in string_example) & ('의무' in string_example):
        return 6, 100
    
    if (('안전성' in string_example) | ('안정성' in string_example)) & ('확보' in string_example):
        return 7, 100
    
    if ('책임자' in string_example):
        return 8, 100
    
    if ('열람' in string_example) | ('창구' in string_example) | ('부서' in string_example):
        return 9, 100
    
    if ('권익' in string_example) | ('침해' in string_example) | ('구제' in string_example):
        return 10, 100
    
    if ('변경' in string_example):
        return 11, 100
    
    if ('3자' in string_example):
        return 12, 100
    
    if ('위탁' in string_example):
        return 13, 100
    
    if ('자동' in string_example) | ('수집' in string_example) | ('장치' in string_example):
        return 14, 100
    
    if ('영상' in string_example) | ('운영' in string_example):
        return 20, 100
    
    inferred_category = 0
    accuracy_of_infer = 100
    
    return inferred_category, accuracy_of_infer



# find_all_h, classify_category
# Input     : html body
# Output    : 항목별 [태그, 정확도, 제목, 내용] 리스트

def extract_titles(html_body_tagged):
    start = time.time()

    bss = bs(html_body_tagged, "html.parser")
    
    find_h = []
    res = bss.find_all('h1')
    find_h.append(res)
    
    res = bss.find_all('h2')
    find_h.append(res)
    
    res = bss.find_all('h3')
    find_h.append(res)
    
    res = bss.find_all('h4')
    find_h.append(res)
    
    res = bss.find_all('h5')
    find_h.append(res)
    
    res = bss.find_all('h6')
    find_h.append(res)
        
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 제목 그룹 추정
    
    iidx = -1
    val_STANDARD = 8    # 최소 8개는 있어야
    cat_val = []
    
    for idx, each_h in enumerate(find_h):
        # 각 h1, h2... 등 h 그룹에 대하여
        val = 0
        cat_val.append([])
        
        for each in each_h:
            # 개별 태그 단위
            cat, accuracy = classify_category(each.get_text())
            
            cat_val[idx].append([cat, accuracy, each, each.get_text()])
            
            # if show_print:
            #     print(f"{cat:<5} {each}")
                
            if cat != 0:
                val += 1
                
        if val > val_STANDARD:
            iidx = idx
            ival = val
            break
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if iidx == -1:
        print("\n[Error] h레벨에서 제목으로 추정되는 항목 없음\n")
        return []
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # 제목 정리해서 출력하는 구문
    selected_cat_h_list = cat_val[iidx]
    processed_cat_h_list = []    
    counted = []

    for cat, acc, tag, text in selected_cat_h_list:
        # print(cat, text)
        if cat == 0:
            processed_cat_h_list.append([0, 0, tag, text])
        elif cat in counted:
            processed_cat_h_list.append([0, 0, tag, text])
        else:
            counted.append(cat)
            processed_cat_h_list.append([cat, acc, tag, text])
            
    end = time.time()
    print(f"[Log] (func)/extract_titles Run Time : {(end - start):.4f} sec\n")
    
    return processed_cat_h_list


# Input     : each body section
# Output    : text string

def parse_text_from(target):
    bss = bs(target, "html.parser")
    
    # using_tag = [['h1', 'h2', 'h3', 'h4', 'h5'], 'p', 'strong', 'li']
    # excluse_tag = ['a']
    all_text = ''
    
    res = bss.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'strong'])
    if res == []:
        pass
    else:
        for each in res:
            all_text += each.get_text() + '\n'
    
    # link 있는 버튼 등 (a href)은 무시
    res = bss.find_all('p')
    if res != []:
        for each in res:
            
            if each.find('a'):
                if each.find('a').has_attr('href'):
                    pass   
            else:
                all_text += each.get_text() + '\n'
                
    res = bss.find_all('li')
    if res != []:
        for each in res:
            if each.find('li'):
                a = str(each)
                b = each.find_all('ul')
                for ttt in b:
                    a = a.replace(str(ttt)+'\n', "")
                all_text += bs(a, 'html.parser').get_text() + '\n'
            else:
                all_text += each.get_text() + '\n'
        
    return all_text
    
    
# Input     : html body
# Output    : table attributes

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def parse_table_from(target):
    
    table_set = []
    
    bss = bs(target, "html.parser")
    
    ress = bss.find_all('table')
    if len(ress) == 0:
        pass
    else:
        for res in ress:

            header = []
            header_ = []
            rows = []
            cols = []
            
            # head, body 둘 다 있음
            there = res.find("thead")
            if there:
                rmax = 1
                cmax = 0
                there = res.find("thead").find("tr")
                for child in there.children:
                    if (type(child) == bs4.element.NavigableString) or (type(child) == bs4.element.Comment):
                        continue
                    
                    if 'rowspan' in child.attrs:
                        if int(child.attrs['rowspan']) > rmax:
                            rmax = int(child.attrs['rowspan'])
                            
                    if 'colspan' in child.attrs:
                        cmax += int(child.attrs['colspan'])
                    else:
                        cmax += 1
                        
                there = res.find("thead").find_all("tr")
                header_ = [ [ 'No Data' for _ in range(cmax)] for __ in range(rmax) ]
                
                for ridx, line in enumerate(there):
                    gap = 0
                    for cidx, child in enumerate(line.children):
                        if (type(child) == bs4.element.NavigableString) or (type(child) == bs4.element.Comment):
                            gap += 1
                            continue
                        child_text = child.get_text().replace('\n', '').strip()
                        
                        if ('rowspan' in child.attrs) & ('colspan' in child.attrs):
                            for i in range(int(child.attrs['rowspan']) ):
                                for j in range(int(child.attrs['colspan']) ):
                                    header_[ridx + i][cidx - gap + j] = child_text
                        elif ('rowspan' not in child.attrs) & ('colspan' in child.attrs):
                            for j in range(int(child.attrs['colspan']) ):
                                header_[ridx][cidx - gap + j] = child_text
                        elif ('rowspan' in child.attrs) & ('colspan' not in child.attrs):
                            for i in range(int(child.attrs['rowspan']) ):
                                header_[ridx + i][cidx - gap] = child_text
                        else:
                            header_[ridx][cidx - gap] = child_text

                header = header_[rmax-1]

                there = res.find("tbody").find_all("tr")
                rows = [ [ 'No Data' for __ in range(cmax) ] for _ in range(len(there)) ]
                cols = [ [ 'No Data' for __ in range(len(there)) ] for _ in range(cmax) ]
                    
            # end if (head, body)   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            else:
                # 1) 헤더 견적을 보고
                rmax = 1
                cmax = 0
                there = res.find("tr")
                for child in there.children:
                    if (type(child) == bs4.element.NavigableString) or (type(child) == bs4.element.Comment):
                        continue
                    
                    if 'rowspan' in child.attrs:
                        if int(child.attrs['rowspan']) > rmax:
                            rmax = int(child.attrs['rowspan'])
                            
                    if 'colspan' in child.attrs:
                        cmax += int(child.attrs['colspan'])
                    else:
                        cmax += 1
                            
                # 2) 헤더를 찾기 위해 뻘짓 ( ~ rmax까지는 header, 나머지는 body )   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
                there = res.find_all("tr")
                header_ = [ [ 'No Data' for _ in range(cmax)] for __ in range(rmax) ]

                for ridx, line in enumerate(there):
                    if ridx == rmax:
                        break
                    else:
                        gap = 0
                        for cidx, child in enumerate(line.children):
                            if (type(child) == bs4.element.NavigableString) or (type(child) == bs4.element.Comment):
                                gap += 1
                                continue
                            child_text = child.get_text().replace('\n', '').strip()
                            
                            if ('rowspan' in child.attrs) & ('colspan' in child.attrs):
                                for i in range(int(child.attrs['rowspan']) ):
                                    for j in range(int(child.attrs['colspan']) ):
                                        header_[ridx + i][cidx - gap + j] = child_text
                            elif ('rowspan' not in child.attrs) & ('colspan' in child.attrs):
                                for j in range(int(child.attrs['colspan']) ):
                                    header_[ridx][cidx - gap + j] = child_text
                            elif ('rowspan' in child.attrs) & ('colspan' not in child.attrs):
                                for i in range(int(child.attrs['rowspan']) ):
                                    header_[ridx + i][cidx - gap] = child_text
                            else:
                                header_[ridx][cidx - gap] = child_text

                header = header_[rmax-1]

                there = there[rmax:]
                rows = [ [ 'No Data' for __ in range(cmax) ] for _ in range(len(there)) ]
                cols = [ [ 'No Data' for __ in range(len(there)) ] for _ in range(cmax) ]
                
                
                
            # body 탐색은 동일
            for ridx, line in enumerate(there):
                gap = 0
                for cidx, child in enumerate(line.children):
                    if (type(child) == bs4.element.NavigableString) or (type(child) == bs4.element.Comment):
                        gap += 1
                        continue
                    
                    child_text = child.get_text().replace('\n', '').strip()
                    
                    if ('rowspan' in child.attrs) & ('colspan' in child.attrs):
                        for i in range(int(child.attrs['colspan']) ):
                            for j in range(int(child.attrs['rowspan']) ):
                                rows[ridx + j][cidx - gap + i] = child_text
                                cols[cidx - gap + i][ridx + j] = child_text
                        gap -= 1
                            
                    elif ('rowspan' not in child.attrs) & ('colspan' in child.attrs):
                        for i in range(int(child.attrs['colspan']) ):
                            rows[ridx][cidx - gap + i] = child_text
                            cols[cidx - gap + i][ridx] = child_text
                        gap -= 1

                    elif ('rowspan' in child.attrs) & ('colspan' not in child.attrs):
                        for i in range(int(child.attrs['rowspan']) ):
                            rows[ridx + i][cidx - gap] = child_text
                            cols[cidx - gap][ridx + i] = child_text

                    else:
                        rows[ridx][cidx - gap] = child_text
                        cols[cidx - gap][ridx] = child_text
            
            table_set.append([header, rows, cols, res.get_text()])
    # end else         
    return table_set



 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

 
def parse_body(target):
    
    start = time.time()
    
    bodies = []
    
    pre = [ -1, -1, 0, '', '']  # index, cat_num, acc, title(tag), title(non_tag)
    all_list = extract_titles(target)

    for cat, acc, tagged_title, title in all_list:
        
        point = target.find(str(tagged_title))
        
        # 제목 앞의 내용은 잘라버려!
        if pre[0] == -1:
            pre = [ point + len(str(tagged_title)), cat, acc, tagged_title, title ]
            continue
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # 내용 추출 -> 저장
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        
        splited_body = target[pre[0] : point]
        extract_text = parse_text_from(splited_body)
        extract_table = parse_table_from(splited_body)
        
        bodies.append( [ pre[1], pre[2], pre[4], extract_text, extract_table ] )    # category_number, accuracy, title, body, table
        pre = [ point + len(str(tagged_title)), cat, acc, tagged_title, title ]
        
    # 마지막 문항 : 나머지 내용도 출력
    if pre[1] != 0:
        splited_body = target[pre[0] : ]
        
        extract_text = parse_text_from(splited_body)
        extract_table = parse_table_from(splited_body)
        bodies.append( [ pre[1], pre[2], pre[4], extract_text, extract_table ] )
        

    end = time.time()
    print(f"[Log] (func)/parse_body Run Time : {(end - start):.4f} sec\n")
    
    return bodies


def has_(header_list, word_list):
    condition = 0.8
    for idx, h in enumerate(header_list):
        for w in word_list:
            h = h.strip()
            if is_similar_word(h, w) > condition:
                return idx
    return -1
        
    
def is_similar_word(word_to_check, word_to_compare):
    
    if word_to_compare in word_to_check:
        return 1
    
    # Cosine
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform((word_to_compare, word_to_check))
    cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Jaccard
    intersection_cardinality = len(set.intersection(*[set(word_to_compare), set(word_to_check)]))
    union_cardinality = len(set.union(*[set(word_to_compare), set(word_to_check)]))
    j_similar = intersection_cardinality / float(union_cardinality)

    # SequenceMatcher
    answer_bytes = bytes(word_to_compare, 'utf-8')
    input_bytes = bytes(word_to_check, 'utf-8')
    answer_bytes_list = list(answer_bytes)
    input_bytes_list = list(input_bytes)

    sm = difflib.SequenceMatcher(None, answer_bytes_list, input_bytes_list)
    s_similar = sm.ratio()

    
    return max(cos_similar, j_similar, s_similar)



def check1check(bodies):
    
    start = time.time()
    
    checklist_len = 38
    checklist = [ False for _ in range(checklist_len+1) ]
    
    cat_num_table = []
    
    for body in bodies:
        cat_num_table.append(body[0])
        
    # print(cat_num_table)
    
    # 1번 : 제목은 패스
    
    # 2 ~ 3
    if (2 in cat_num_table):
        checklist[2] = True
        
        for table in bodies[cat_num_table.index(2)][4]:
            header = table[0]
            cols = table[2]
            rawText = table[4]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True        
                        
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False

        
        
    # 4 ~ 11
    if (3 in cat_num_table):
        checklist[4] = True
        
        for table in bodies[cat_num_table.index(3)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False
        
    # 12 ~ 13
    if (4 in cat_num_table):
        checklist[12] = True
        
        for table in bodies[cat_num_table.index(4)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False
        
    # 14
    if (5 in cat_num_table):
        checklist[14] = True
    
    # 15
    if (6 in cat_num_table):
        checklist[15] = True
        
    # 16
    if (7 in cat_num_table):
        checklist[16] = True
        
    # 17 ~ 18
    if (8 in cat_num_table):
        checklist[17] = True
        checklist[18] = True
        
        if bodies[cat_num_table.index(8)][4] == []:
            rawText = bodies[cat_num_table.index(8)][3]
        else:
            rawText = bodies[cat_num_table.index(8)][4][0][3]
        
        patterns = {
        'phone': r'(\d{2,3}[-)]?\d{3,4}[-)]?\d{4})',
        'email': r'([\w!-_.]+@[\w!-_.]+\.[\w]{2,3})'
        }
        if not re.search(patterns['phone'], rawText):
            checklist[18] = False
        if not re.search(patterns['email'], rawText):
            checklist[18] = False
        
    # 19 ~ 20
    if (9 in cat_num_table):
        checklist[19] = True
        checklist[20] = True
        
        if bodies[cat_num_table.index(9)][4] == []:
            rawText = bodies[cat_num_table.index(9)][3]
        else:
            rawText = bodies[cat_num_table.index(9)][4][0][3]
        
        patterns = {
        'phone': r'(\d{2,3}[-)]?\d{3,4}[-)]?\d{4})',
        'email': r'([\w!-_.]+@[\w!-_.]+\.[\w]{2,3})'
        }
        if not re.search(patterns['phone'], rawText):
            checklist[20] = False
        if not re.search(patterns['email'], rawText):
            checklist[20] = False
            
    # 21 ~ 22
    if (10 in cat_num_table):
        checklist[21] = True
        checklist[22] = True
        rawText = bodies[cat_num_table.index(10)][3]
        if rawText.find('privacy.kisa.or.kr') == -1:
            checklist[22] = False
        if rawText.find('www.kopico.go.kr') == -1:
            checklist[22] = False
        if rawText.find('www.spo.go.kr') == -1:
            checklist[22] = False
        if rawText.find('ecrm.cyber.go.kr') == -1:
            checklist[22] = False
        
        
        
    # 23
    if (11 in cat_num_table):
        checklist[23] = True
    # 24 ~ 31
    if (12 in cat_num_table):
        checklist[24] = True
        
        for table in bodies[cat_num_table.index(12)][4]:
            header = table[0]
            cols = table[2]
            
            that_idx = has_(header, ['제공받는자', '제공기관', '제공받는기관'])
            if that_idx != -1:
                checklist[25] = True
                checklist[30] = True
                for col in cols[that_idx]:
                    if '공공기관' in col:
                        checklist[30] = False
                    if '정부기관' in col:
                        checklist[30] = False
                    if '관련기관' in col:
                        checklist[30] = False
                    if '협회' in col:
                        checklist[30] = False
                    if '보험회사' in col:
                        checklist[30] = False
                
            if has_(header, ['목적', '제공목적', '이용목적', '제공받는자의이용목적']):
                checklist[26] =  True
            if has_(header, ['항목', '제공정보', '제공하는개인정보항목', '제공하는개인정보파일명']):
                checklist[27] = True
                
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[28] = True
                checklist[31] = True
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[31] = False
                    if '목적달성시' in col:
                        checklist[31] = False
                    if '수시' in col:
                        checklist[31] = False
                    if '사유발생시' in col:
                        checklist[31] = False

                
                
    # 32 ~ 36
    if (13 in cat_num_table):
        checklist[32] = True
        
        for table in bodies[cat_num_table.index(13)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['수탁자', '업체명', '위탁대상', '위탁업체명', '수탁기관', '수탁업체명', '수탁사', '수탁업체', '수탁업체명칭']):
                checklist[33] = True
            if has_(header, ['위탁업무', '업무목적', '업무내용', '위탁항목', '위탁하는업무내용']):
                checklist[34] = True
                
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[36] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[36] = False
                    if '목적달성시' in col:
                        checklist[36] = False
                    if '수시' in col:
                        checklist[36] = False
                    if '사유발생시' in col:
                        checklist[36] = False
   


                
    # 37
    if (14 in cat_num_table):
        checklist[37] = True
    # 38
    if (15 in cat_num_table):
        checklist[38] = True
        
        
        
    if (16 in cat_num_table):
        checklist[2] = True
        checklist[4] = True
        checklist[12] = True
        
        for table in bodies[cat_num_table.index(16)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False
                
    
    if (17 in cat_num_table):
        checklist[2] = True
        checklist[4] = True
        
        for table in bodies[cat_num_table.index(17)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False

            
    
    if (18 in cat_num_table):
        checklist[2] = True
        checklist[12] = True
        
        for table in bodies[cat_num_table.index(18)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False
                
    
    if (19 in cat_num_table):
        checklist[4] = True
        checklist[12] = True
        
        for table in bodies[cat_num_table.index(19)][4]:
            header = table[0]
            cols = table[2]
            
            if has_(header, ['파일명', '명칭', '개인정보파일명', '개인정보파일의명칭']):
                checklist[5] = True
            if has_(header, ['목적', '수집목적', '운영목적', '수집/이용목적', '처리목적', '개인정보파일의운영목적']):
                checklist[6] = True   
            if has_(header, ['항목', '처리하는개인정보의항목']):
                checklist[7] = True                
            if has_(header, ['근거', '보유근거', '처리근거', '운영근거']):
                checklist[8] = True                
            
            that_idx = has_(header, ['기간', '보유및이용기간'])
            if that_idx:
                checklist[9] = True  
                checklist[11] = True
                
                for col in cols[that_idx]:
                    col = col.replace(' ', '')
                    if '상시' in col:
                        checklist[11] = False
                    if '목적달성시' in col:
                        checklist[11] = False
                    if '수시' in col:
                        checklist[11] = False
                    if '사유발생시' in col:
                        checklist[11] = False
                
    
    
    end = time.time()
    print(f"[Log] (func)/checkList Run Time : {(end - start):.4f} sec\n")
    
    return checklist

