from flask import Flask, request, render_template
from googleapiclient.discovery import build
from google.oauth2 import service_account

# إعداد التطبيق
app = Flask(__name__)

# ملف الاعتمادات
SERVICE_ACCOUNT_FILE = 'darsad-4190bdeb5d1c.json'  # اسم ملف JSON الخاص بك
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']  # أو .readonly إذا كنت تريد القراءة فقط

# إعداد الاعتمادات
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# معرف Google Sheets ونطاق البيانات
SPREADSHEET_ID = '1mdOJkxaV98nQ5taeav8eyd9JcoC_g_WZ3kLz1jKd5V0'
RANGE_NAME = 'استعلام!A:C'  # تعديل النطاق حسب الأعمدة المتاحة

@app.route('/')
def home():
    return render_template('index.html')  # يعرض صفحة الإدخال

@app.route('/search', methods=['POST'])
def search():
    passport_number = request.form['passport']

    # جلب البيانات من Google Sheets
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get('values', [])

    # البحث عن رقم الجواز
    for row in rows:
        if len(row) >= 3 and row[0] == passport_number:
            return render_template('result.html', passport=row[0], name=row[1], company=row[2])
    
    return render_template('not_found.html')

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
