// Minimal chat backend: serves the UI and proxies streaming chat to an
// OpenAI-compatible API. The API key stays server-side.
const http = require('http');
const fs = require('fs');
const path = require('path');

const { APX_API_KEY, APX_BASE_URL = 'https://api.apmix.ai/v1', APX_MODEL = 'claude-sonnet-5', PORT = 3000 } = process.env;
if (!APX_API_KEY) {
  console.error('Missing APX_API_KEY. See .env.example');
  process.exit(1);
}

const indexHtml = fs.readFileSync(path.join(__dirname, 'public', 'index.html'));

const readBody = (req) =>
  new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (c) => { data += c; if (data.length > 1e6) req.destroy(); });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });

http.createServer(async (req, res) => {
  if (req.method === 'GET' && (req.url === '/' || req.url === '/index.html')) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(indexHtml);
  }
  if (req.method === 'GET' && req.url === '/api/models') {
    try {
      const r = await fetch(`${APX_BASE_URL.replace(/\/$/, '')}/models`, {
        headers: { Authorization: `Bearer ${APX_API_KEY}` },
      });
      const j = r.ok ? await r.json() : { data: [] };
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ default: APX_MODEL, models: (j.data || []).map((m) => m.id) }));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ default: APX_MODEL, models: [APX_MODEL] }));
    }
  }
  if (req.method === 'POST' && req.url === '/api/chat') {
    try {
      const { messages, model } = JSON.parse(await readBody(req));
      if (!Array.isArray(messages)) throw new Error('messages must be an array');
      const upstream = await fetch(`${APX_BASE_URL.replace(/\/$/, '')}/chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${APX_API_KEY}` },
        body: JSON.stringify({ model: typeof model === 'string' && model ? model : APX_MODEL, messages, stream: true }),
      });
      if (!upstream.ok) {
        res.writeHead(upstream.status, { 'Content-Type': 'text/plain' });
        return res.end(await upstream.text());
      }
      res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' });
      for await (const chunk of upstream.body) res.write(chunk);
      return res.end();
    } catch (e) {
      if (!res.headersSent) res.writeHead(500, { 'Content-Type': 'text/plain' });
      return res.end(String(e.message || e));
    }
  }
  res.writeHead(404); res.end('Not found');
}).listen(PORT, () => console.log(`Chat app on http://localhost:${PORT}`));
