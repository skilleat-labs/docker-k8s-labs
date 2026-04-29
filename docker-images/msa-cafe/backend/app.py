from flask import Flask, jsonify, request
import pymysql
import os
import socket
import time

app = Flask(__name__)


def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'cafe'),
        password=os.environ.get('DB_PASS', 'cafe1234'),
        database=os.environ.get('DB_NAME', 'cafedb'),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def init_db():
    # MySQL 기동 대기 (컨테이너 시작 순서 차이)
    for attempt in range(15):
        try:
            conn = get_db()
            break
        except Exception:
            print(f'DB 연결 대기 중... ({attempt + 1}/15)')
            time.sleep(3)
    else:
        raise RuntimeError('DB에 연결할 수 없습니다.')

    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            price INT NOT NULL,
            emoji VARCHAR(10) NOT NULL,
            category VARCHAR(20) NOT NULL
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(50) NOT NULL,
            quantity INT NOT NULL,
            total INT NOT NULL,
            created_at DATETIME DEFAULT NOW()
        )''')
        cur.execute('SELECT COUNT(*) AS cnt FROM products')
        if cur.fetchone()['cnt'] == 0:
            cur.executemany(
                'INSERT INTO products VALUES (%s,%s,%s,%s,%s)',
                [
                    (1, '아메리카노',  4500, '☕', '음료'),
                    (2, '카페라떼',   5500, '🥛', '음료'),
                    (3, '바닐라라떼', 5800, '🍦', '음료'),
                    (4, '치즈케이크', 6500, '🍰', '디저트'),
                    (5, '크로와상',   3500, '🥐', '베이커리'),
                    (6, '머핀',       3000, '🧁', '베이커리'),
                ]
            )
    conn.close()
    print('DB 초기화 완료')


@app.route('/api/products')
def get_products():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM products')
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            'SELECT *, DATE_FORMAT(created_at, "%H:%i:%S") AS created_at '
            'FROM orders ORDER BY id DESC LIMIT 30'
        )
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO orders (product_name, quantity, total) VALUES (%s,%s,%s)',
            (data['product_name'], data['quantity'], data['total'])
        )
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/status')
def status():
    return jsonify({
        'hostname': socket.gethostname(),
        'pid': os.getpid(),
    })


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
