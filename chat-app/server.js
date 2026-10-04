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

// Documents dropped in ./docs are read on every request and used as context.
const DOCS_DIR = path.join(__dirname, 'docs');
const TEXT_EXT = new Set(['.txt', '.md', '.csv', '.tsv', '.json', '.html', '.xml', '.yaml', '.yml']);
const MAX_CONTEXT_CHARS = 400000;

const loadServerDocs = () => {
  if (!fs.existsSync(DOCS_DIR)) return [];
  return fs.readdirSync(DOCS_DIR)
    .filter((f) => TEXT_EXT.has(path.extname(f).toLowerCase()) && f.toLowerCase() !== 'readme.md')
    .map((f) => ({ name: f, text: fs.readFileSync(path.join(DOCS_DIR, f), 'utf8') }));
};

const buildSystemMessage = (uploaded) => {
  const docs = [...loadServerDocs(), ...(Array.isArray(uploaded) ? uploaded : [])];
  let budget = MAX_CONTEXT_CHARS;
  const parts = [];
  for (const d of docs) {
    if (!d || typeof d.text !== 'string' || budget <= 0) continue;
    const text = d.text.slice(0, budget);
    budget -= text.length;
    parts.push(`<document name="${String(d.name).replace(/"/g, '')}">\n${text}\n</document>`);
  }
  if (!parts.length) return null;
  return {
    role: 'system',
    content: 'You have access to the following documents. Use them as context, answer from them when relevant, and cite the document name. If the answer is not in the documents, say so.\n\n' + parts.join('\n\n'),
  };
};

const readBody = (req) =>
  new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (c) => { data += c; if (data.length > 12e6) req.destroy(); });
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
      return res.end(JSON.stringify({ default: APX_MODEL, models: (j.data || []).map((m) => m.id), serverDocs: loadServerDocs().map((d) => d.name) }));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ default: APX_MODEL, models: [APX_MODEL] }));
    }
  }
  if (req.method === 'POST' && req.url === '/api/chat') {
    try {
      const { messages, model, context } = JSON.parse(await readBody(req));
      if (!Array.isArray(messages)) throw new Error('messages must be an array');
      const sys = buildSystemMessage(context);
      const upstream = await fetch(`${APX_BASE_URL.replace(/\/$/, '')}/chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${APX_API_KEY}` },
        body: JSON.stringify({ model: typeof model === 'string' && model ? model : APX_MODEL, messages: sys ? [sys, ...messages] : messages, stream: true }),
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
