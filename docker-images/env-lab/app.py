from flask import Flask
import os

app = Flask(__name__)

CONFIG_KEYS = [
    ('APP_ENV',      'dev/prod 환경 구분'),
    ('DB_HOST',      'DB 서버 주소'),
    ('DB_PORT',      'DB 포트'),
    ('DB_PASSWORD',  'DB 비밀번호'),
    ('APP_VERSION',  '앱 버전 (ENV로 전달)'),
    ('BUILD_DATE',   '빌드 일자 (ENV로 전달)'),
]

@app.route('/')
def index():
    rows = ''
    for key, desc in CONFIG_KEYS:
        value = os.environ.get(key, '<not set>')
        # 비밀번호는 일부만 표시
        if key == 'DB_PASSWORD' and value != '<not set>':
            display = value[:2] + '*' * (len(value) - 2)
        else:
            display = value
        rows += f'<tr><td>{key}</td><td>{display}</td><td style="color:#888">{desc}</td></tr>'

    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>App Config</title>
  <style>
    body {{ font-family: monospace; padding: 40px; background: #f5f5f5; }}
    h2 {{ color: #333; }}
    table {{ border-collapse: collapse; width: 700px; background: white; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    th {{ background: #2d2d2d; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
    tr:last-child td {{ border-bottom: none; }}
  </style>
</head>
<body>
  <h2>🔧 App Configuration</h2>
  <table>
    <tr><th>Key</th><th>Value</th><th>Description</th></tr>
    {rows}
  </table>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
