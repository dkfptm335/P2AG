import pandas as pd
from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateMain')
def generate():
    return render_template('generateMain.html')


@app.route('/generateConfirm', methods=['POST'])
def generateConfirm():
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
    if file.filename.endswith('.xlsx'):
        # df = pd.read_excel(file, header=None)
        # columns = df.iloc[2][0:]
        # # 0, 1, 2행 제거
        # df = df.drop([0, 1, 2], axis=0)
        # df.columns = columns
        # df.reset_index(drop=True, inplace=True)
        # df.fillna("", inplace=True)
        # return render_template('generateConfirm.html', name=name, df=df, chargeName=chargeName,
        #                        chargeAffiliation=chargeAffiliation, chargePhone=chargePhone, chargeEmail=chargeEmail,
        #                        chargeEtc=chargeEtc, department=department, departmentName=departmentName,
        #                        departmentPhone=departmentPhone, departmentEmail=departmentEmail,
        #                        departmentEtc=departmentEtc)
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
        academic_df = df[(df['개인정보파일의 운영 목적'].str.contains('학사관리')) | (df['개인정보파일의 운영 목적'].str.contains('학교행정업무')) | (
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
        return render_template('generateConfirm.html', name=name, df=df, chargeName=chargeName,
                               chargeAffiliation=chargeAffiliation, chargePhone=chargePhone, chargeEmail=chargeEmail,
                               chargeEtc=chargeEtc, department=department, departmentName=departmentName,
                               departmentPhone=departmentPhone, departmentEmail=departmentEmail,
                               departmentEtc=departmentEtc, combined_data=combined_data,
                               receipt_department=receipt_department, receipt_departmentName=receipt_departmentName,
                               receipt_departmentPhone=receipt_departmentPhone,
                               receipt_departmentEmail=receipt_departmentEmail,
                               receipt_departmentEtc=receipt_departmentEtc, current_date=current_date,
                               academic_df=academic_df, scholarship_df=scholarship_df, grade_df=grade_df,
                               graduate_df=graduate_df, date_ranges=date_ranges)
    else:
        return render_template('generateMain.html', error='.xlsx 파일만 업로드 가능합니다.')


if __name__ == '__main__':
    app.run(debug=True)
