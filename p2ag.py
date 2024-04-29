import pandas as pd
from flask import Flask, request, session
from flask import render_template, redirect, url_for
import requests, re
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키 설정

def extract_and_verify(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, verify=False)
    html_content = response.content.decode('utf-8', 'replace')
    soup = bs(html_content, 'html.parser')
    text = soup.get_text()
    text = text.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')

 # 각 검사 함수를 호출
    item_results = check_required_items(text)
    keyword_results = check_keywords(text)
    description_results = check_descriptions(text)
    compliance_results = check_compliance(text)
    
    # 결과를 카테고리별로 저장
    categories = {
        '필수항목 유무 검사 결과': item_results,
        '키워드 검사 결과': keyword_results,
        '서술 방식 검사 결과': description_results,
        '표현방식 검사 결과': compliance_results
    }
    return categories

def check_required_items(text):
    missing_items = []
    required_items = [
        "목적", "처리", "보유기간", "항목", "파기", "정보주체", "법정대리인",
        "권리", "의무", "행사방법", "안전성확보조치", "책임자", ("열람청구", "열람요구"),
        "접수", "처리", "권익침해", ("처리방침의변경", "처리방침변경"), "제3자제공", "위탁"
    ]

    for item in required_items:
        if isinstance(item, tuple):
            if not any(variation in text for variation in item):
                missing_items.append(item[0])
        else:
            if item not in text:
                missing_items.append(item)

    return "누락된 필수 항목: " + ", ".join(missing_items) if missing_items else "모든 필수 항목이 존재합니다."

def check_keywords(text):
    missing_keywords = []
    keywords = [
    ('개인정보파일명', '파일명', '개인정보파일', '개인정보파일의명칭'),
    ('수집목적', '개인정보파일의운영목적', '운영목적', '개인정보수집/이용목적', '처리목적'),
    ('수집항목', '처리하는개인정보의항목', '처리하는개인정보항목', '개인정보의항목'),
    ('보유근거', '처리근거', '운영근거'),
    ('보유및이용기간','개인정보보유기간', '제공기간', '처리기간', '처리및보유기간','보유및처리기간'),
    ('제공받는자', '제공기관', '제공받는기관','제공현황','제공목록', '제공리스트'),
    ('제공목적', '제공받는자의이용목적', '이용목적'),
    ('제공정보', '제공하는항목', '제공하는개인정보항목', '제공항목', '개인정보파일명','제공현황', '제공리스트'),
    ('수탁자', '업체명', '위탁대상', '위탁업체명', '수탁기관', '수탁업체명', '수탁사', '수탁업체', '수탁업체명칭'),
    ('위탁하는업무내용', '업무목적', '위탁업무내용', '위탁업무', '위탁항목', '업무내용', '위탁하는업무의내용')
    ]

    for group in keywords:
        if not any(keyword in text for keyword in group):
            missing_keywords.append(group[0])

    return "누락된 키워드: " + ", ".join(missing_keywords) if missing_keywords else "모든 키워드가 존재합니다."

def check_descriptions(text):
    issues = []
    ambiguous_terms = ["기타등등", "등", "기타", "정부기관", "공공기관", "관련기관", "협회",
                       "보험회사", "목적달성시", "타법령에따라", "수시", "상시", "사유발생시","관계법률에"]
    for term in ambiguous_terms:
        if term in text:
            issues.append(f"모호한 용어 '{term}'이(가) 사용됨.")

    return "\n".join(issues) if issues else "문서에 모호한 용어가 없습니다."

def check_compliance(text):
    results = []
    # 전화번호 형식 검사
    if not re.search(r'\d{2,3}-\d{3,4}-\d{4}', text):
        results.append("전화번호 형식이 잘못되었습니다. 올바른 형식 예: 010-1234-5678")
    # 이메일 형식 검사
    if not re.search(r'[\w.-]+@[\w.-]+\.\w+', text):
        results.append("이메일 형식이 잘못되었습니다. 올바른 형식 예: example@example.com")

    return "\n".join(results) if results else "모든 표현이 적절합니다."

@app.route('/')
def index():
    # 모든 global 변수 초기화
    global academic_df
    global scholarship_df
    global grade_df
    global graduate_df
    global newStudent_df
    global disorder_df
    global homepage_df
    global etc_df
    global combined_data_result
    global date_ranges
    global selected_rows
    global manager_position
    global manager_affiliation
    global manager_phone
    global access_position
    global access_affiliation
    global access_phone
    global checkBox4
    global checkList7
    global checkList8
    global checkbox2
    global checkbox3
    global selected_rows2
    global trustees
    global trustee_options
    global retrustees_dict

    academic_df = pd.DataFrame()
    scholarship_df = pd.DataFrame()
    grade_df = pd.DataFrame()
    graduate_df = pd.DataFrame()
    newStudent_df = pd.DataFrame()
    disorder_df = pd.DataFrame()
    homepage_df = pd.DataFrame()
    etc_df = pd.DataFrame()
    combined_data_result = dict()
    date_ranges = []
    selected_rows = []
    manager_position = ''
    manager_affiliation = ''
    manager_phone = ''
    access_position = ''
    access_affiliation = ''
    access_phone = ''
    checkBox4 = ''
    checkList7 = []
    checkList8 = []
    checkbox2 = ''
    checkbox3 = ''
    selected_rows2 = []
    trustees = []
    trustee_options = []
    retrustees_dict = {}

    # 모든 세션 데이터 초기화
    session.pop('form_data_1', None)
    session.pop('form_data_2', None)
    session.pop('form_data_3', None)
    session.pop('form_data_4', None)

    return render_template('index.html')


@app.route('/preGenerate')
def preGenerate():
    return render_template('preGenerate.html')


@app.route('/generateMain')
def generate():
    return render_template('generateMain.html')


@app.route('/generateMainMall')
def generateMainMall():
    return render_template('generateMainMall.html')


academic_df = pd.DataFrame()
scholarship_df = pd.DataFrame()
grade_df = pd.DataFrame()
graduate_df = pd.DataFrame()
newStudent_df = pd.DataFrame()
disorder_df = pd.DataFrame()
homepage_df = pd.DataFrame()
etc_df = pd.DataFrame()
combined_data_result = dict()
date_ranges = []


def process_form_data1(request):
    global academic_df
    global scholarship_df
    global grade_df
    global graduate_df
    global newStudent_df
    global disorder_df
    global homepage_df
    global etc_df
    global combined_data_result
    global date_ranges

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
    combined_data = dict(zip(result_head, result_messages))
    combined_data_result = combined_data

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
    date_ranges = [{'start_date': start, 'end_date': end} for start, end in zip(start_dates, end_dates)]

    # header=0 옵션으로 첫 번째 행을 칼럼명으로 사용
    df = pd.read_excel(file, header=None)
    columns = df.iloc[2][0:]
    # 0, 1, 2행 제거
    df = df.drop([0, 1, 2], axis=0)
    df.columns = columns
    df.reset_index(drop=True, inplace=True)

    # '개인정보파일의 명칭' 및 '개인정보의 보유기간'데이터가 NaN인 경우, 이전 행의 데이터로 채워넣기
    df['개인정보파일의 명칭'].ffill(inplace=True)
    df['개인정보의 보유기간'].ffill(inplace=True)
    df['개인정보파일에 기록되는 개인정보의 항목'].ffill(inplace=True)

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
    newStudent_df = df[(df['개인정보파일의 운영 목적'].str.contains('입시')) | (df['개인정보파일의 운영 목적'].str.contains('신입'))]
    disorder_df = df[(df['개인정보파일의 운영 목적'].str.contains('장애'))]
    homepage_df = df[(df['개인정보파일의 운영 목적'].str.contains('홈페이지')) | (df['개인정보파일의 운영 목적'].str.contains('웹사이트'))]

    # 나머지 데이터 etc_df로 저장
    etc_df = df[~df.index.isin(academic_df.index) & ~df.index.isin(scholarship_df.index) & ~df.index.isin(
        grade_df.index) & ~df.index.isin(graduate_df.index) & ~df.index.isin(newStudent_df.index) & ~df.index.isin(
        disorder_df.index) & ~df.index.isin(homepage_df.index)]

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
        'date_ranges': date_ranges,
        'newStudent_df': newStudent_df,
        'disorder_df': disorder_df,
        'homepage_df': homepage_df,
        'etc_df': etc_df
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


selected_rows = []


@app.route('/nextFormConfirm', methods=['POST'])
def nextFormConfirm():
    global selected_rows
    selected_rows = []
    form_data_1 = session.get('form_data_1', {})
    session['form_data_2'] = request.form.to_dict()
    name = form_data_1['name']
    # 제3자 제공 및 처리위탁 체크박스 확인
    checkBoxList = request.form.getlist('checkBoxList')
    checkbox1 = ''

    if 'checkBox1' in checkBoxList:
        checkbox1 = 1

    # 체크박스 선택 항목 가져오기
    selected_checks = request.form.getlist('checklist')

    # 선택된 체크박스에 대응하는 textarea 데이터 처리
    for check in selected_checks:
        # 각 항목의 recipient, purpose, items, period, reason 데이터 추출
        selected_rows.append({
            'recipient': request.form[f'recipient_{check}'],
            'purpose': request.form[f'purpose_{check}'],
            'data_items': request.form[f'items_{check}'],
            'period': request.form[f'period_{check}'],
            'reason': request.form[f'reason_{check}']
        })

    if request.form['action'] == 'confirm':
        return render_template('nextFormConfirm.html', name=name, checkbox1=checkbox1, selected_rows=selected_rows)
    else:
        return redirect(url_for('nextForm1_2'))


@app.route('/nextForm1_2', methods=['GET', 'POST'])
def nextForm1_2():
    return render_template('nextForm1_2.html')


checkbox2 = ''
checkbox3 = ''
selected_rows2 = []
trustees = []
trustee_options = []
retrustees_dict = {}


@app.route('/nextForm1_2Confirm', methods=['POST'])
def nextForm1_2Confirm():
    global checkbox2
    global checkbox3
    global selected_rows2
    global trustees
    global trustee_options
    global retrustees_dict

    form_data_1 = session.get('form_data_1', {})
    session['form_data_3'] = request.form.to_dict()
    name = form_data_1['name']
    # 제3자 제공 및 처리위탁 체크박스 확인
    checkBoxList = request.form.getlist('checkBoxList')
    checkbox2 = ''
    checkbox3 = ''

    if 'checkBox2' in checkBoxList:
        checkbox2 = 1
    if 'checkBox3' in checkBoxList:
        checkbox3 = 1

    # 체크박스 선택 항목 가져오기
    selected_checks = request.form.getlist('checklist2')
    selected_rows2 = []
    # 선택된 체크박스에 대응하는 textarea 데이터 처리
    for check in selected_checks:
        selected_rows2.append({
            'trustee': request.form[f'trustee_{check}'],
            'text': request.form[f'text_{check}'],
        })

    # 수탁사 이름 받아오기

    fieldsetCount = request.form['fieldsetCount']
    classification1 = []
    classification2 = []
    trustees = []
    trustee_options = []
    for key in request.form:
        if key.startswith('add_trustee'):
            trustees.append(request.form[key])
    for i in range(1, int(fieldsetCount) + 1):
        trustee_options = []
        for key in request.form:
            if key.startswith(f'trustee{i}_option'):
                trustee_options.append(request.form[key])
        classification1.append(next((request.form[key] for key in trustee_options if key.startswith(f'trustee')), None))
        classification2.append(
            next((request.form[key] for key in trustee_options if key.startswith(f'trustee{i}_option2')), None))

    trustees = zip(trustees, classification1, classification2)

    retrustees_dict = {}

    for i in range(1, int(fieldsetCount) + 1):
        trustee1_retrustee_name = request.form.getlist(f'trustee{i}_retrustee_name[]')
        trustee1_retrustee_business = request.form.getlist(f'trustee{i}_retrustee_business[]')
        retrustee_list = zip(trustee1_retrustee_name, trustee1_retrustee_business)
        # 딕셔너리에 i에 retrustee 추가
        retrustees_dict[i] = [{'name': name, 'business': business} for name, business in retrustee_list]

    if request.form['action'] == 'confirm':
        return render_template('nextForm1_2Confirm.html', name=name, checkbox2=checkbox2, checkbox3=checkbox3,
                               selected_rows=selected_rows2, trustees=trustees, retrustees_dict=retrustees_dict)
    else:
        return redirect(url_for('nextForm1_3'))


@app.route('/nextForm1_3', methods=['GET', 'POST'])
def nextForm1_3():
    return render_template('nextForm1_3.html')


@app.route('/nextForm1_3Confirm', methods=['GET', 'POST'])
def nextForm1_3Confirm():
    form_data_1 = session.get('form_data_1', {})
    name = form_data_1['name']
    # 제3자 제공 및 처리위탁 체크박스 확인
    checkBoxList = request.form.getlist('checkBoxList')
    checkbox1 = ''
    checkbox2 = ''
    if 'checkBox1' in checkBoxList:
        checkbox1 = 1
    if 'checkBox2' in checkBoxList:
        checkbox2 = 1

    # 체크박스 선택 항목 가져오기
    selected_checks = request.form.getlist('checklist2')
    selected_rows = []
    auto_collect = request.form['auto_collect']
    # 선택된 체크박스에 대응하는 textarea 데이터 처리
    for check in selected_checks:
        selected_rows.append({
            'trustee': request.form[f'trustee_{check}'],
            'text': request.form[f'text_{check}'],
        })

    if request.form['action'] == 'confirm':
        return render_template('nextForm1_3Confirm.html', name=name, checkbox2=checkbox2, checkbox1=checkbox1,
                               selected_rows=selected_rows, auto_collect=auto_collect)
    else:
        return redirect(url_for('nextForm2'))


@app.route('/nextForm2', methods=['GET', 'POST'])
def nextForm2():
    return render_template('nextForm2.html')


manager_position = ''
manager_affiliation = ''
manager_phone = ''
access_position = ''
access_affiliation = ''
access_phone = ''
checkBox4 = ''
checkList7 = []
checkList8 = []


def process_form_data3(request):
    global manager_position
    global manager_affiliation
    global manager_phone
    global access_position
    global access_affiliation
    global access_phone
    global checkBox4
    global checkList7
    global checkList8
    checkList7 = []
    checkList8 = []

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

    if manager:  # manager에서 / 단위로 잘라서 책임자 직위 소속 연락처로 넣기
        manager_position = manager.split('/')[0]
        manager_affiliation = manager.split('/')[1]
        manager_phone = manager.split('/')[2]

    access_authority = request.form['access_authority']  # 접근 권한자
    if access_authority:
        access_position = access_authority.split('/')[0]
        access_affiliation = access_authority.split('/')[1]
        access_phone = access_authority.split('/')[2]

    # 4. 영상정보 촬영시간, 보관기간, 보관장소, 처리방법
    shooting_time = request.form['shooting_time']  # 촬영 시간
    storage_period = request.form['storage_period']  # 보관 기간
    storage_location = request.form['storage_location']  # 보관 장소
    processing_method = request.form['processing_method']  # 처리 방법

    # 이거 예시가 없음
    trustee = request.form['trustee']
    trustee_tel = request.form['trustee_tel']

    # 5. 영상정보 확인 방법 및 장소
    checking_method = request.form['checking_method']
    checking_location = request.form['checking_location']

    # 6~7
    checkListYes = request.form.getlist('checkListYes')
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

    # 만 14세 미만 개인정보 처리
    checkBox2 = ''
    if 'checkBox2' in request.form.getlist('checkBox2'):
        checkBox2 = 1

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
        'processing_method': processing_method,
        'trustee': trustee,
        'trustee_tel': trustee_tel,
        'checkList7': checkList7,
        'checkList8': checkList8,
        'checkBox4': checkBox4,
        'checking_method': checking_method,
        'checking_location': checking_location,
        'current_date': current_date,
        'checkBox2': checkBox2
    }


@app.route('/nextForm2Confirm', methods=['GET', 'POST'])
def nextForm2Confirm():
    session['form_data_4'] = request.form.to_dict()
    processed_data = process_form_data3(request)
    if processed_data:
        if 'action' in request.form and request.form['action'] == 'confirm':
            return render_template('nextForm2Confirm.html', **processed_data)
        else:
            return redirect(url_for('result'))
    else:
        return redirect(url_for('result'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    global academic_df
    global scholarship_df
    global grade_df
    global graduate_df
    global newStudent_df
    global disorder_df
    global homepage_df
    global etc_df
    global combined_data_result
    global selected_rows
    global manager_position
    global manager_affiliation
    global manager_phone
    global access_position
    global access_affiliation
    global access_phone
    global checkBox4
    global checkList7
    global checkList8
    global date_ranges
    global checkbox2
    global checkbox3
    global selected_rows2
    global trustees
    global trustee_options
    global retrustees_dict

    form_data1 = session.get('form_data_1', {})
    form_data2 = session.get('form_data_2', {})
    form_data3 = session.get('form_data_3', {})
    form_data4 = session.get('form_data_4', {})

    return render_template('result.html', form_data1=form_data1, form_data2=form_data2, form_data4=form_data4,
                           academic_df=academic_df, scholarship_df=scholarship_df, grade_df=grade_df,
                           graduate_df=graduate_df, newStudent_df=newStudent_df, disorder_df=disorder_df,
                           homepage_df=homepage_df, etc_df=etc_df, combined_data_result=combined_data_result,
                           selected_rows=selected_rows, manager_position=manager_position,
                           manager_affiliation=manager_affiliation, manager_phone=manager_phone,
                           access_position=access_position, access_affiliation=access_affiliation,
                           access_phone=access_phone, checkBox4=checkBox4, checkList7=checkList7, checkList8=checkList8,
                           date_ranges=date_ranges, checkbox2=checkbox2, checkbox3=checkbox3, trustees=trustees,
                           trustee_options=trustee_options, retrustees_dict=retrustees_dict, form_data3=form_data3,
                           selected_rows2=selected_rows2)


@app.route('/inspectionMain')
def inspectionMain():
    return render_template('inspectionMain.html')


if __name__ == '__main__':
    app.run(debug=True)
