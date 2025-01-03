from flask import Flask, request, render_template
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import json

# إعداد التطبيق
app = Flask(__name__)

# قراءة بيانات الاعتماد من ملف JSON مباشرة
SERVICE_ACCOUNT_FILE = "GOOGLE_CREDENTIALS_JSON.json"  # اسم الملف

if not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise ValueError(f"File {SERVICE_ACCOUNT_FILE} not found!")

# إعداد الاعتمادات
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# معرف Google Sheets ونطاق البيانات
SPREADSHEET_ID = '1mdOJkxaV98nQ5taeav8eyd9JcoC_g_WZ3kLz1jKd5V0'
RANGE_NAME = 'استعلام!A:C'  # تعديل النطاق حسب الأعمدة المتاحة

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        passport_number = request.form['passport']

        # جلب البيانات من Google Sheets
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        rows = result.get('values', [])

        # البحث عن رقم الجواز
        for row in rows:
            if len(row) >= 3 and row[0] == passport_number:
                # إذا تم العثور على النتيجة
                return render_template(
                    "combined.html",
                    result={"passport": row[0], "name": row[1], "company": row[2]},
                    not_found=False,
                )

        # إذا لم يتم العثور على النتيجة
        return render_template("combined.html", not_found=True)

    # عرض نموذج البحث
    return render_template("combined.html")

if __name__ == "__main__":
    app.run(debug=True)
