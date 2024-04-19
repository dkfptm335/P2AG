import pandas as pd
from flask import Flask, request, session, flash
from flask import render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키 설정


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateMain')
def generate():
    return render_template('generateMain.html')

def process_form_data1(request):
    name = request.form['name']
    file = request.files['file']

    # 체크박스 확인
    selected_datas = request.form.getlist('securityMeasures')
    result_head = []
    result_messages = []
    if 'minimalStaffTraining' in selected_datas:
        result_head.append('[관리]개인정보 취급 직원의 최소화 및 교육')
        result_messages.append('개인정보를 취급하는 담당자는 반드시 필요한 인원에 한하여 지정ㆍ관리하고 있으며, 취급자를 대상으로 안전한 관리를 위한 교육을 실시하고 있습니다.')
    if 'regularSelfAudit' in selected_datas:
        result_head.append('[관리]정기적인 자체 감사')
        result_messages.append('개인정보 취급 관련 안정성 확보를 위해 정기적으로 자체 감사를 실시하고 있습니다.')
    if 'internalManagementPlan' in selected_datas:
        result_head.append('[관리]내부관리계획 수립 및 시행')
        result_messages.append('개인정보의 안전한 처리를 위하여 내부관리계획을 수립․시행하고 있습니다.')
    if 'dataEncryption' in selected_datas:
        result_head.append('[기술]개인정보의 암호화')
        result_messages.append(
            '이용자의 개인정보 중 비밀번호, 주민등록번호는 암호화 되어 저장 및 관리되고 있어, 본인만이 알 수 있으며 중요한 데이터는 파일 및 전송 데이터를 암호화 하거나 파일 잠금 기능을 사용하는 등의 별도 보안기능을 사용하고 있습니다.')
    if 'securitySoftware' in selected_datas:
        result_head.append('[기술]보안프로그램 설치 및 주기적 점검·갱신')
        result_messages.append(
            '해킹이나 컴퓨터 바이러스 등에 의한 개인정보 유출 및 훼손을 막기 위하여 보안프로그램을 설치하고 주기적인 갱신·점검을 하며 외부로부터 접근이 통제된 구역에 시스템을 설치하고 기술적/물리적으로 감시 및 차단하고 있습니다.')
    if 'accessRestriction' in selected_datas:
        result_head.append('[기술]개인정보에 대한 접근 제한')
        result_messages.append(
            '개인정보를 처리하는 데이터베이스시스템에 대한 접근권한의 부여,변경,말소를 통하여 개인정보에 대한 접근통제를 위하여 필요한 조치를 하고 있으며 침입차단시스템을 이용하여 외부로부터의 무단 접근을 통제하고 있습니다.')
    if 'unauthorizedAccessControl' in selected_datas:
        result_head.append('[물리]비인가자에 대한 출입 통제')
        result_messages.append('개인정보를 보관하고 있는 물리적 보관 장소를 별도로 두고 이에 대해 출입통제 절차를 수립, 운영하고 있습니다.')
    if 'logManagement' in selected_datas:
        result_head.append('[관리]접속기록의 보관 및 위 변조 방지')
        result_messages.append(
            '개인정보처리시스템에 접속한 기록을 최소 1년 이상 보관, 관리하고 있으며, 접속기록이 위·변조 및 도난, 분실되지 않도록 월 1회 이상 점검하고 있습니다. 다만, 5만 명 이상의 정보주체에 관하여 개인정보를 처리하거나, 고유식별정보 또는 민감정보를 처리하는 개인정보처리시스템의 경우에는 2년 이상 보관 및 관리하고 있습니다.')
    if 'documentSecurity' in selected_datas:
        result_head.append('[물리]문서보안을 위한 잠금장치 사용')
        result_messages.append('개인정보가 포함된 서류, 보조저장매체 등을 잠금 장치가 있는 안전한 장소에 보관하고 있습니다.')

    if not result_messages:
        result_messages.append('선택된 항목에 대한 설명이 없습니다.')
    combined_data = zip(result_head, result_messages)

    # 개인정보 보호책임자(담당부서)
    chargeName = request.form['chargeName']
    chargeAffiliation = request.form['chargeAffiliation']
    chargePhone = request.form['chargePhone']
    chargeEmail = request.form['chargeEmail']
    chargeEtc = request.form['chargeEtc']

    department = request.form['department']
    departmentName = request.form['departmentName']
    departmentPhone = request.form['departmentPhone']
    departmentEmail = request.form['departmentEmail']
    departmentEtc = request.form['departmentEtc']
    # 개인정보의 열람청구를 접수/처리하는 부서
    receipt_department = request.form['receipt_department']
    receipt_departmentName = request.form['receipt_departmentName']
    receipt_departmentPhone = request.form['receipt_departmentPhone']
    receipt_departmentEmail = request.form['receipt_departmentEmail']
    receipt_departmentEtc = request.form['receipt_departmentEtc']

    # 현재 날짜 받아오기
    current_date = request.form['current_date']

    # 제출된 데이터를 가져온다
    start_dates = request.form.getlist('start_date')
    end_dates = request.form.getlist('end_date')
    print(start_dates, end_dates)
    date_ranges = [{'start_date': start, 'end_date': end} for start, end in zip(start_dates, end_dates)]
    print(start_dates)

    # header=0 옵션으로 첫 번째 행을 칼럼명으로 사용
    df = pd.read_excel(file, header=None)
    columns = df.iloc[2][0:]
    # 0, 1, 2행 제거
    df = df.drop([0, 1, 2], axis=0)
    df.columns = columns
    df.reset_index(drop=True, inplace=True)

    # '개인정보파일의 운영 목적' 열에서 '학사' 또는 '행정'이 포함된 행을 필터링
    # 결측치 제거
    df.dropna(subset=['개인정보파일의 운영 목적'], inplace=True)
    df = df[['개인정보파일의 명칭', '개인정보파일의 운영 목적', '개인정보파일에 기록되는 개인정보의 항목', '개인정보의 보유기간']]
    academic_df = df[
        (df['개인정보파일의 운영 목적'].str.contains('학사관리')) | (df['개인정보파일의 운영 목적'].str.contains('학교행정업무')) | (
            df['개인정보파일의 운영 목적'].str.contains('학사')) | (df['개인정보파일의 운영 목적'].str.contains('행정')) | (
            df['개인정보파일의 운영 목적'].str.contains('학교 행정')) | (df['개인정보파일의 운영 목적'].str.contains('학교행정'))]
    scholarship_df = df[(df['개인정보파일의 운영 목적'].str.contains('장학생')) | (df['개인정보파일의 운영 목적'].str.contains('장학'))]
    grade_df = df[(df['개인정보파일의 운영 목적'].str.contains('성적')) | (df['개인정보파일의 운영 목적'].str.contains('수강')) | (
        df['개인정보파일의 운영 목적'].str.contains('수업'))]
    graduate_df = df[(df['개인정보파일의 운영 목적'].str.contains('졸업')) | (df['개인정보파일의 운영 목적'].str.contains('졸업생'))]
    # 필터링된 결과에서 최대 2개의 행만 선택
    if len(academic_df) > 2:
        academic_df = academic_df.iloc[:2]
    if len(scholarship_df) > 2:
        scholarship_df = scholarship_df.iloc[:2]
    if len(grade_df) > 2:
        grade_df = grade_df.iloc[:2]
    if len(graduate_df) > 2:
        graduate_df = graduate_df.iloc[:2]
    return {
        'name': name,
        'df': df,
        'chargeName': chargeName,
        'chargeAffiliation': chargeAffiliation,
        'chargePhone': chargePhone,
        'chargeEmail': chargeEmail,
        'chargeEtc': chargeEtc,
        'department': department,
        'departmentName': departmentName,
        'departmentPhone': departmentPhone,
        'departmentEmail': departmentEmail,
        'departmentEtc': departmentEtc,
        'combined_data': combined_data,
        'receipt_department': receipt_department,
        'receipt_departmentName': receipt_departmentName,
        'receipt_departmentPhone': receipt_departmentPhone,
        'receipt_departmentEmail': receipt_departmentEmail,
        'receipt_departmentEtc': receipt_departmentEtc,
        'current_date': current_date,
        'academic_df': academic_df,
        'scholarship_df': scholarship_df,
        'grade_df': grade_df,
        'graduate_df': graduate_df,
        'date_ranges': date_ranges
    }

@app.route('/generateConfirm', methods=['POST'])
def generateConfirm():
    session['form_data_1'] = request.form.to_dict()
    process_data = process_form_data1(request)

    if request.form['action'] == 'confirm':
        return render_template('generateConfirm.html', **process_data)
    else:
        return redirect(url_for('nextForm'))


@app.route('/nextForm', methods=['GET', 'POST'])
def nextForm():
    return render_template('nextForm.html')

rows_data = {
    'check1': {'recipient': '대학 학적관리', 'purpose': '장학재단 장학 행정 협조', 'data_items': '주민등록번호, 성명, 학과,학번, 전화번호, 이메일,주소, 성별, 수험번호 , 학년, 학적, 신입생 여부, 등록납부대상구분, 학적상태, 입학년도, 총평균평점, 수납계좌번호', 'period': '연 2회, 10년', 'reason': ' - 한국장학재단 설립 등에 관한 법률 제 50조 및 제 50조의 2\n - 한국장학재단 설립 등에 관한 법률 시행령 제35조의2, 제35조의3, 제36조의2\n - 고등교육법 시행령 제73조 제2항\n - 취업 후 학자금 상환 특별법 제45조의2'},
    'check2': {'recipient': '근로복지공단', 'purpose': '4대보험 업무 처리\n - 고용보험 보험료 징수 및 관리\n - 산재보험 보험료 징수 및 관리', 'data_items': '성명, 주민등록번호, 연간보수총액, 월 소득액, 자격취득일, 직종부호, 1주소정근로시간', 'period': '영구', 'reason': ' - 고용산재보험료징수법 제5조, 제11조, 제 12조, 제16조의1~16조 9, 제 40조\n - 고용보험법 제8조 및 제15조\n - 산업재해보상보험법 제6조'},
    'check3': {'recipient': '국민연금관리공단', 'purpose': '4대보험 업무 처리\n - 국민연금가입 및 공제', 'data_items': '성명, 주민번호, 월 소득액, 입사일, 퇴사일, 직종, 휴직기록', 'period': '입사익월 15일 부터 퇴사익월 15일까지, 영구', 'reason': '국민연금법 제21조,제123조'},
    'check4': {'recipient': '국민건강보험공단', 'purpose': '4대보험 업무 처리\n- 건강보험가입 및 공제', 'data_items': '성명,주민등록번호, 입사일, 퇴사일, 휴직기록, 월 소득액, 직종, 재직당시 근로소득, 해외출국기록', 'period': '입사익월 15일부터 퇴사익월 15일까지, 영구', 'reason': ' - 국민건강보험법 제7조, 제9조, 제96조\n - 국민건강보험법 시행령 제38조\n - 국민건강보험법 시행규칙 제4조'},
    'check5': {'recipient': '병무청', 'purpose': '병무행정에 대한 협조\n - 신/재학생 입영 연기 처리\n - 학생 예비군 자원관리', 'data_items': '성명, 생년월일, 주소, 학적반영일, 제적사유, 학번, 전공, 학년, 이메일, 전화번호, 입학년도, 졸업년도', 'period': '연 2회(3월, 9월), 10년', 'reason': ' - 병역법 제80조 및 제60조\n - 병역법 시행령 제124조 및 제127조\n - 입영연기 관리 규정 제5조, 제6조, 제12조, 제14조'},
    'check6': {'recipient': '국가평생교육진흥원', 'purpose': '학점인정 및 교육원 학사관리', 'data_items': '성명, 생년월일, 학력, 주소, 전화번호, 이메일, 계좌번호', 'period': '연 4회, 준영구', 'reason': '연 4회, 준영구'},
    'check7': {'recipient': '한국대학교육협의회', 'purpose': '입학 지원자 현황 및 위반자 처리', 'data_items': '성명, 주민등록번호, 출신고교, 졸업년도', 'period': '연 1회, 5년', 'reason': '고등교육법시행령제35조'},
    'check8': {'recipient': '교육부', 'purpose': '교원의 자격검정에 관한 사무\n - 교원자격증 수여', 'data_items': '성명, 주민등록번호, 발급기관, 교원자격증번호, 발급일자, 보고년도, 취득일, 학위번호', 'period': '연 2회, 준영구', 'reason': ' - 교원자격검정령 제3조, 제31조\n - 교원자격검정령 시행규칙 제3조의 2'},
    'check9': {'recipient': '법무부(출입국관리사무소)', 'purpose': '외국인 유학생(출입국) 관리', 'data_items': '여권번호, 생년월일, 출신학교 이름, 출생국가, 성별, 국적, 이메일, 입학유형, 등록과정, 계열구분, 교육기간, 학과/전공, 한국어구사능력,출석현황', 'period': '연 8회, 준영구', 'reason': '출입국관리법 제19조의4, 시행령 제101조'},
    'check10': {'recipient': '한국대학교육협의회', 'purpose': '대입전형지원자 현황, 중복등록자 확인', 'data_items': '성명, 주민등록번호, 출신고교, 졸업년도', 'period': '5년', 'reason': '고등교육법시행령제35조, 제42조,제42조의2'},
    'check11': {'recipient': '국회도서관', 'purpose': '학위논문 납본', 'data_items': '학위등록번호, 성명, 학과, 졸업일자, 학위논문명', 'period': '준영구', 'reason': '국회도서관법 제7조'},
    'check12': {'recipient': '한국교육학술정보원', 'purpose': '학위논문 등록관리', 'data_items': '학위논문정보', 'period': '준영구', 'reason': '정보주체 동의'},
    'check13': {'recipient': '한국교육개발원', 'purpose': '고등교육기관 교육기본통계조사 수행(학생, 교원, 직원)', 'data_items': '성명,주민등록번호, 외국인등록번호, 입학년월일, 졸업년월일, 학적상태, 등록금납부현황, 학위취득일, 학위정보, 외국인학생졸업후상황, 교직원번호, 임용정보, 국적', 'period': '연2회, 5년', 'reason': ' -  고등교육법 제11조의 3\n - 교육통계조사에 대한 훈령\n - 통계법에 따른 통계청 지정통계 승인번호 제334001호'},
    'check14': {'recipient': '보훈처', 'purpose': '장학금(국가보조금) 지급', 'data_items': '보훈번호,성명,주민등록번호,학과,학년,평균성적,신청학점,입학금,수업료,이수학기, 등록여부, 학적변동일자', 'period': '연2회, 5년', 'reason': ' - 국가유공자등예우및지원에관한법률제25조\n - 국가유공자등예우및지원에관한 법률시행령제102조의2'}
}

@app.route('/nextFormConfirm', methods=['POST'])
def nextFormConfirm():
    form_data_1 = session.get('form_data_1', {})
    name = form_data_1['name']
    # 제3자 제공 및 처리위탁 체크박스 확인
    checkBoxList = request.form.getlist('checkBoxList')
    checkbox1 = ''

    if 'checkBox1' in checkBoxList:
        checkbox1 = 1


    selected_ids = request.form.getlist('checklist')
    selected_rows = [rows_data[id] for id in selected_ids if id in rows_data]
    print(selected_rows)
    if request.form['action'] == 'confirm':
        return render_template('nextFormConfirm.html', name=name, checkbox1=checkbox1, selected_rows=selected_rows)
    else:
        return redirect(url_for('nextForm1_2'))

@app.route('/nextForm1_2', methods=['GET', 'POST'])
def nextForm1_2():
    return render_template('nextForm1_2.html')

@app.route('/nextForm1_2Confirm', methods=['POST'])
def nextForm1_2Confirm():
    form_data_1 = session.get('form_data_1', {})
    name = form_data_1['name']
    # 제3자 제공 및 처리위탁 체크박스 확인
    checkBoxList = request.form.getlist('checkBoxList')
    checkbox2 = ''

    if 'checkBox2' in checkBoxList:
        checkbox2 = 1

    selected_ids = request.form.getlist('checklist')
    selected_rows = [rows_data[id] for id in selected_ids if id in rows_data]
    print(selected_rows)
    if request.form['action'] == 'confirm':
        return render_template('nextForm1_2Confirm.html', name=name, checkbox2=checkbox2, selected_rows=selected_rows)
    else:
        return redirect(url_for('nextForm1_2'))

@app.route('/nextForm2', methods=['GET', 'POST'])
def nextForm2():
    return render_template('nextForm2.html')

def process_form_data3(request):
    form_data_1 = session.get('form_data_1', {})
    name = form_data_1['name']
    checkBoxList = request.form.getlist('checkBoxList')
    # 체크박스 확인
    checkBox1 = ''
    if 'checkBox1' in request.form.getlist('checkBox1'):
        checkBox1 = 1

    # 1. 영상정보처리기기 설치근거·목적
    purpose = request.form['purpose']  # 근거 목적
    # 2. 설치 대수, 설치 위치, 촬영 범위
    installation_number = request.form['installation_number']  # 설치 대수
    installation_location = request.form['installation_location']  # 설치 위치 및 범위

    # 3. 관리책임자, 담당부서 및 영상정보에 대한 접근권한자
    manager = request.form['manager']  # 관리책임자
    # '/'가 정확히 2개 포함되어 있는지 확인

    manager_position = ''
    manager_affiliation = ''
    manager_phone = ''
    if manager:  # manager에서 / 단위로 잘라서 책임자 직위 소속 연락처로 넣기
        manager_position = manager.split('/')[0]
        manager_affiliation = manager.split('/')[1]
        manager_phone = manager.split('/')[2]

    access_authority = request.form['access_authority']  # 접근 권한자
    access_position = ''
    access_affiliation = ''
    access_phone = ''
    if access_authority:
        access_position = access_authority.split('/')[0]
        access_affiliation = access_authority.split('/')[1]
        access_phone = access_authority.split('/')[2]


    # 4. 영상정보 촬영시간, 보관기간, 보관장소, 처리방법
    shooting_time = request.form['shooting_time']  # 촬영 시간
    storage_period = request.form['storage_period']  # 보관 기간
    storage_location = request.form['storage_location']  # 보관 장소

    ###############보류################
    # 체크박스 확인
    checkBox4 = ''
    if 'Processing_method' in request.form.getlist('Processing_method'):
        checkBox4 = '‣ 처리방법 : 개인영상정보의 목적 외 이용, 제3자 제공, 파기, 열람 등 요구에 관한 사항을 기록ㆍ관리하고, 보관기간 만료시 복원이 불가능한 방법으로 영구 삭제(출력물의 경우 파쇄 또는 소각)합니다.'

    # 이거 예시가 없음
    trustee = request.form['trustee']
    trustee_tel = request.form['trustee_tel']

    # 5. 영상정보 확인 방법 및 장소
    checking_method = request.form['checking_method']
    checking_location = request.form['checking_location']

    # 6~7
    checkListYes = request.form.getlist('checkListYes')
    checkList7 = []
    checkList8 = []
    print(checkList7)
    if 'sub7' in checkListYes:
        checkList7.append('‣  귀하는 개인영상정보에 관하여 열람 또는 존재확인ㆍ삭제를 원하는 경우 언제든지 영상정보처리기기 운영자에게 요구하실 수 있습니다. ')
        checkList7.append('‣  단, 귀하가 촬영된 개인영상정보 및 명백히 정보주체의 급박한 생명, 신체, 재산의 이익을 위하여 필요한 개인영상정보에 한정됩니다.')
        checkList7.append('‣  본 기관은 개인영상정보에 관하여 열람 또는 존재확인ㆍ삭제를 요구한 경우 지체없이 필요한 조치를 하겠습니다.')
    if 'sub8' in checkListYes:
        checkList8.append('‣  본 기관에서 처리하는 영상정보는 암호화 조치 등을 통하여 안전하게 관리되고 있습니다. ')
        checkList8.append(
            '‣  또한 본 기관은 개인영상정보보호를 위한 관리적 대책으로서 개인정보에 대한 접근 권한을 차등부여하고 있고, 개인영상정보의 위ㆍ변조 방지를 위하여 개인영상정보의 생성 일시, 열람시 열람 목적ㆍ열람자ㆍ열람 일시 등을 기록하여 관리하고 있습니다. ')
        checkList8.append('‣  이 외에도 개인영상정보의 안전한 물리적 보관을 위하여 잠금장치를 설치하고 있습니다')

    # 8. 영상정보처리기기 운영·관리 방침의 변경에 관한 사항
    # 현재 날짜 받아오기
    current_date = request.form['current_date']

    # 제출된 데이터를 가져온다
    start_dates = request.form.getlist('start_date')
    end_dates = request.form.getlist('end_date')
    date_ranges = [{'start_date': start, 'end_date': end} for start, end in zip(start_dates, end_dates)]

    # 처리된 데이터를 딕셔너리로 반환
    return {
        'name': name,
        'checkBox1': checkBox1,
        'checkBoxList': checkBoxList,
        'purpose': purpose,
        'installation_number': installation_number,
        'installation_location': installation_location,
        'manager_position': manager_position,
        'manager_affiliation': manager_affiliation,
        'manager_phone': manager_phone,
        'access_position': access_position,
        'access_affiliation': access_affiliation,
        'access_phone': access_phone,
        'shooting_time': shooting_time,
        'storage_period': storage_period,
        'storage_location': storage_location,
        'trustee': trustee,
        'trustee_tel': trustee_tel,
        'checkList7': checkList7,
        'checkList8': checkList8,
        'checkBox4': checkBox4,
        'checking_method': checking_method,
        'checking_location': checking_location,
        'current_date': current_date,
        'date_ranges': date_ranges
    }

@app.route('/nextForm2Confirm', methods=['GET','POST'])
def nextForm2Confirm():
    processed_data = process_form_data3(request)
    if processed_data:
        if 'action' in request.form and request.form['action'] == 'confirm':
            return render_template('nextForm2Confirm.html', **processed_data)
        else:
            return redirect(url_for('result'))
    else:
        return redirect(url_for('result'))




@app.route('/result', methods=['GET','POST'])
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
