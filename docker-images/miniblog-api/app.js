const express = require('express');
const mysql   = require('mysql2/promise');

const VERSION = '2.0.0';

const app = express();
app.use(express.json());

const dbConfig = {
  host:     process.env.DB_HOST     || 'localhost',
  port:     parseInt(process.env.DB_PORT || '3306'),
  database: process.env.DB_NAME     || 'blogdb',
  user:     process.env.DB_USER     || 'bloguser',
  password: process.env.DB_PASSWORD || 'blogpassword123',
};

let db;

async function connectWithRetry(maxRetries = 10, delayMs = 3000) {
  for (let i = 1; i <= maxRetries; i++) {
    try {
      db = await mysql.createConnection(dbConfig);

      // 테이블 생성 (없을 경우)
      await db.execute(`
        CREATE TABLE IF NOT EXISTS posts (
          id         INT AUTO_INCREMENT PRIMARY KEY,
          title      VARCHAR(255) NOT NULL,
          content    TEXT         NOT NULL,
          author     VARCHAR(100),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `);

      // v1 → v2 마이그레이션: author 컬럼이 없으면 추가
      try {
        await db.execute('ALTER TABLE posts ADD COLUMN author VARCHAR(100)');
        console.log('Migration: author column added');
      } catch {
        // 이미 존재하면 무시
      }

      console.log(`DB connected (${dbConfig.host}:${dbConfig.port}/${dbConfig.database})`);
      return;
    } catch (err) {
      console.error(`DB connection failed (${i}/${maxRetries}): ${err.message}`);
      if (i === maxRetries) throw err;
      await new Promise(r => setTimeout(r, delayMs));
    }
  }
}

// ── Routes ──────────────────────────────────────────────

app.get('/health', (req, res) => {
  res.json({ status: 'ok', version: VERSION });
});

app.get('/posts', async (req, res) => {
  try {
    const [rows] = await db.execute('SELECT * FROM posts ORDER BY id ASC');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/posts', async (req, res) => {
  const { title, content, author } = req.body;
  if (!title || !content) {
    return res.status(400).json({ error: 'title and content are required' });
  }
  try {
    const [result] = await db.execute(
      'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
      [title, content, author || null]
    );
    const post = { id: result.insertId, title, content, version: VERSION };
    if (author) post.author = author;
    res.status(201).json(post);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/posts/:id', async (req, res) => {
  try {
    const [rows] = await db.execute('SELECT * FROM posts WHERE id = ?', [req.params.id]);
    if (!rows.length) return res.status(404).json({ error: 'Not found' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ── Start ────────────────────────────────────────────────

connectWithRetry()
  .then(() => {
    app.listen(8080, () =>
      console.log(`miniblog-api v${VERSION} listening on :8080`)
    );
  })
  .catch(err => {
    console.error('Failed to start:', err.message);
    process.exit(1);
  });
