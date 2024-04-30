

def to_html_table(bodies, check_list):
    
    res = []
    
    tmp = []
    if not check_list[2]:
        tmp.append("[항목존재]")
    if not check_list[3]:
        tmp.append("[표현존재]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
        
    title = "-"
    for body in bodies:
        if body[0] == 2 or body[0] == 16 or body[0] == 17 or body[0] == 18:
            title = body[2]
            break
        
    res.append(["개인정보의 처리 목적", tmp, title])
    
    
    tmp = []
    if not check_list[4]:
        tmp.append("[항목존재]")
    if not check_list[5] or not check_list[6] or not check_list[7] or not check_list[8] or not check_list[9]:
        tmp.append("[컬럼명존재]")
    if not check_list[10] or not check_list[11]:
        tmp.append("[표현방식]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
        
    title = "-"
    for body in bodies:
        if body[0] == 3 or body[0] == 16 or body[0] == 17 or body[0] == 19:
            title = body[2]
            break
        
    res.append(["개인정보의 처리 및 보유기간", tmp, title])
    
    tmp = []
    if not check_list[12]:
        tmp.append("[항목존재]")
    if not check_list[5] or not check_list[6] or not check_list[7] or not check_list[8] or not check_list[9]:
        tmp.append("[컬럼명존재]")
    if not check_list[11]:
        tmp.append("[표현방식]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    
    title = "-"
    for body in bodies:
        if body[0] == 4 or body[0] == 16 or body[0] == 18 or body[0] == 19:
            title = body[2]
            break
    res.append(["처리하는 개인정보의 항목", tmp, title])
    
    if not check_list[14]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 5:
            title = body[2]
            break
    res.append(["개인정보의 파기 절차 및 방법에 관한 사항", tmp, title])
    
    if not check_list[15]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 6:
            title = body[2]
            break
    res.append(["정보주체와 법정대리인의 권리/의무 및 행사방법에 관한 사항", tmp, title])
    
    if not check_list[16]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 7:
            title = body[2]
            break
    res.append(["개인정보의 안정성 확보조치에 관한 사항", tmp, title])
    
    tmp = []
    if not check_list[17]:
        tmp.append("[항목존재]")
    if not check_list[18]:
        tmp.append("[정보값존재]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    title = "-"
    for body in bodies:
        if body[0] == 8:
            title = body[2]
            break
    res.append(["개인정보 보호책임자에 관한 사항", tmp, title])
    
    
    
    
    tmp = []
    if not check_list[19]:
        tmp.append("[항목존재]")
    if not check_list[20]:
        tmp.append("[정보값존재]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    title = "-"
    for body in bodies:
        if body[0] == 9:
            title = body[2]
            break
    res.append(["개인정보의 열람청구를 접수/처리하는 부서", tmp, title])
    
    
    tmp = []
    if not check_list[21]:
        tmp.append("[항목존재]")
    if not check_list[22]:
        tmp.append("[정보값존재]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    title = "-"
    for body in bodies:
        if body[0] == 10:
            title = body[2]
            break
    res.append(["정보주체의 권익침해에 대한 구제방법", tmp, title])
    
    if not check_list[23]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 11:
            title = body[2]
            break
    res.append(["개인정보 처리방침의 변경에 관한 사항", tmp, title])
    
    
    tmp = []
    if not check_list[24]:
        tmp.append("[항목존재]")
    if not check_list[25] or not check_list[26] or not check_list[27] or not check_list[28]:
        tmp.append("[컬럼값존재]")
    if not check_list[29] or not check_list[30] or not check_list[31]:
        tmp.append("[표현방식]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    title = "-"
    for body in bodies:
        if body[0] == 12:
            title = body[2]
            break
    res.append(["개인정보의 제3자 제공에 관한 사항", tmp, title])
    
    
    tmp = []
    if not check_list[32]:
        tmp.append("[항목존재]")
    if not check_list[33] or not check_list[34]:
        tmp.append("[컬럼값존재]")
    if not check_list[35] or not check_list[36]:
        tmp.append("[표현방식]")
    if len(tmp) > 1:
        tmp = ", ".join(tmp)
    elif len(tmp) == 1:
        tmp = tmp[0]
    else:
        tmp = "-"
    title = "-"
    for body in bodies:
        if body[0] == 13:
            title = body[2]
            break
    res.append(["개인정보 처리업무의 위탁에 관한 사항", tmp, title])
    
    if not check_list[37]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 14:
            title = body[2]
            break
    res.append(["개인정보를 자동으로 수집하는 장치의 설치/운영 및 그 거부에 관한 사항", tmp, title])
    
    if not check_list[38]:
        tmp = "[항목존재]"
    else:
        tmp = ''
    title = "-"
    for body in bodies:
        if body[0] == 15:
            title = body[2]
            break
    res.append(["영상정보처리기기 운영/관리에 관한 사항", tmp, title])

    return res



def to_html_results(bodies, check_list):
    
    result = []     # [title, content] 구성으로 전달
    tmp = []
    
    if not check_list[2]:
        tmp.append("[2] 개인정보의 처리 목적")
    if not check_list[4]:
        tmp.append("[3] 개인정보의 처리 및 보유기간")
    if not check_list[12]:
        tmp.append("[4] 처리하는 개인정보 항목")
    if not check_list[14]:
        tmp.append("[5] 개인정보의 파기 절차 및 방법에 관한 사항")
    if not check_list[15]:
        tmp.append("[6] 정보주체와 법정대리인의 권리/의무 및 행사방법에 관한 사항")
    if not check_list[16]:
        tmp.append("[7] 개인정보의 안전성 확보조치에 관한 사항")
    if not check_list[17]:
        tmp.append("[8] 개인정보 보호책임자에 관한 사항")
    if not check_list[19]:
        tmp.append("[9] 개인정보의 열람청구를 접수/처리하는 부서")
    if not check_list[21]:
        tmp.append("[10] 정보주체의 권익침해에 대한 구제방법")
    if not check_list[23]:
        tmp.append("[11] 개인정보 처리방침의 변경에 관한 사항")
    if not check_list[24]:
        tmp.append("[12] 개인정보의 제3자 제공에 관한 사항")
    if not check_list[32]:
        tmp.append("[13] 개인정보 처리업무의 위탁에 관한 사항")
    if not check_list[37]:
        tmp.append("[14] 개인정보를 자동으로 수집하는 장치의 설치/운영 및 그 거부에 관한 사항")
    if not check_list[38]:
        tmp.append("[15] 영상정보처리기기 운영/관리에 관한 사항")
    
    message = ''
    if tmp:
        title = '항목존재'
        message += f"항목 유무 검사 결과, { ', '.join(tmp) }가 확인되지 않습니다. 해당 항목은 개인정보처리방침에 필수 항목이니 반드시 작성해주십시오."
        result.append([title, message])
    
    
    tmp = []
    if not check_list[5]:
        tmp.append("개인정보파일명")
    if not check_list[6]:
        tmp.append("수집목적")
    if not check_list[7]:
        tmp.append("수집항목")
    if not check_list[8]:
        tmp.append("보유근거")
    if not check_list[9]:
        tmp.append("보유 및 이용 기간")
    
    message = '[3] 개인정보의 처리 및 보유기간, [4] 처리하는 개인정보의 항목 검사 결과, '
    if tmp:
        message += f"{ ','.join(tmp) } 가 확인되지 않습니다. 해당 항목은 개인정보처리방침에 필수 항목이니 반드시 작성해주십시오. "
        
    if not check_list[10]:
        message += "개인정보 처리 항목 또는 처리 목적에 대해 생략 없이 최대한 상세히 작성하십시오. "
    
    if not check_list[11]:
        message += "'상시', '목적달성시' 등의 표현방식은 정확하지 않습니다. 기간을 정확히 기입하십시오. "
        
    if message != '[3] 개인정보의 처리 및 보유기간, [4] 처리하는 개인정보의 항목 검사 결과, ':
        title = '개인정보의 처리 및 보유기간, 항목'
        result.append([title, message])
        
    
    
    if not check_list[18]:
        result.append(["개인정보 보호책임자에 관한 사항", f"[8] 개인정보 보호책임자에 관한 사항 검사 결과, 전화번호/이메일 양식이 알맞지 않습니다."])
    
    if not check_list[20]:
        result.append(["개인정보의 열람청구를 접수/처리하는 부서", f"[9] 개인정보의 열람청구를 접수/처리하는 부서 검사 결과, 전화번호/이메일 양식이 알맞지 않습니다."])
        
    if not check_list[22]:
        result.append(["정보주체의 권익침해에 대한 구제방법", f"[10] 정보주체의 권익침해에 대한 구제방법 검사 결과, 현재 접속 가능한 사이트 주소 및 연락처가 일치하지 않습니다. 권익침해 구제 방법 정보를 최신으로 업데이트 하십시오."])
        
    
    tmp = []
    if not check_list[25]:
        tmp.append("제공받는 자")
    if not check_list[26]:
        tmp.append("제공목적")
    if not check_list[27]:
        tmp.append("제공정보")
    if not check_list[28]:
        tmp.append("보유 및 이용 기간")

    message = '[12] 개인정보의 제3자 제공에 관한 사항 검사 결과, '
    if tmp:
        message += f"{ ','.join(tmp) } 가 확인되지 않습니다. 해당 항목은 개인정보처리방침에 필수 항목이니 반드시 작성해주십시오. "
    
    if not check_list[29]:
        message += "'기타', '등'이 확인됩니다. 개인정보 처리 항목 또는 처리 목적에 대해 생략 없이 최대한 상세히 작성하십시오. "
    
    if not check_list[30]:
        message += "대상을 '공공기관', '정부기관', '관련기관', '협회', '보험회사' 등 포괄적으로 지정하고 있습니다. 제공받는 자에 정확한 이름을 적으십시오. "
        
    if not check_list[31]:
        message += "기간 항목에 '수시', '상시', '목적달성시', '사유발생시' 등의 표현방식은 정확하지 않습니다. 기간을 정확히 기입하시오. "
        
    if message != '[12] 개인정보의 제3자 제공에 관한 사항 검사 결과, ':
        title = '개인정보의 제3자 제공에 관한 사항'
        result.append([title, message])
        
    
    tmp = []
    if not check_list[33]:
        tmp.append("수탁자")
    if not check_list[34]:
        tmp.append("위탁업무")

    message = '[13] 개인정보 처리업무의 위탁에 관한 사항 검사 결과, '
    if tmp:
        message += f"{ ','.join(tmp) } 가 확인되지 않습니다. 해당 항목은 개인정보처리방침에 필수 항목이니 반드시 작성해주십시오. "
    
    if not check_list[35]:
        message += "'기타', '등'이 확인됩니다. 개인정보 처리 항목 또는 처리 목적에 대해 생략 없이 최대한 상세히 작성하십시오. "
        
    if not check_list[36]:
        message += "기간 항목에 '수시', '상시', '목적달성시', '사유발생시' 등의 표현방식은 정확하지 않습니다. 기간을 정확히 기입하시오. "
        
    if message != '[13] 개인정보 처리업무의 위탁에 관한 사항 검사 결과, ':
        title = '개인정보 처리업무의 위탁에 관한 사항'
        result.append([title, message])
    
    
    
    return result