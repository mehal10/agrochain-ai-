/* ==========================================
   AGROCHAIN AI — MAIN JS
   ========================================== */

// ---- CSRF COOKIE ----
function getCookie(name) {
  let v = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(c => {
      c = c.trim();
      if (c.startsWith(name + '=')) v = decodeURIComponent(c.slice(name.length + 1));
    });
  }
  return v;
}

// ---- TOAST ----
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 3500);
}
// alias used in landing page
window.showToastMsg = showToast;

// ---- AI PANEL ----
function toggleAI() {
  const panel = document.getElementById('ai-panel');
  if (panel) panel.classList.toggle('open');
}

function sendMsg() {
  const inp = document.getElementById('ai-input');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';
  const msgs = document.getElementById('ai-msgs');
  msgs.innerHTML += `<div class="msg user">${escapeHtml(msg)}</div>`;
  msgs.scrollTop = msgs.scrollHeight;

  const typing = document.getElementById('ai-typing');
  if (typing) typing.classList.add('show');

  fetch('/api/ai/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ message: msg })
  })
  .then(r => r.json())
  .then(data => {
    if (typing) typing.classList.remove('show');
    const reply = data.response || data.error || 'Something went wrong.';
    msgs.innerHTML += `<div class="msg bot">${escapeHtml(reply)}</div>`;
    msgs.scrollTop = msgs.scrollHeight;
  })
  .catch(() => {
    if (typing) typing.classList.remove('show');
    msgs.innerHTML += `<div class="msg bot">⚠ Network error. Please try again.</div>`;
    msgs.scrollTop = msgs.scrollHeight;
  });
}

function sendInline() {
  const inp = document.getElementById('inline-input');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';
  const chat = document.getElementById('inline-chat');
  chat.innerHTML += `<div class="msg user">${escapeHtml(msg)}</div>`;
  chat.scrollTop = chat.scrollHeight;

  fetch('/api/ai/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ message: msg })
  })
  .then(r => r.json())
  .then(data => {
    const reply = data.response || data.error || 'Something went wrong.';
    chat.innerHTML += `<div class="msg bot">${escapeHtml(reply)}</div>`;
    chat.scrollTop = chat.scrollHeight;
  })
  .catch(() => {
    chat.innerHTML += `<div class="msg bot">⚠ Network error.</div>`;
  });
}

// ---- ESCAPE HTML ----
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}

// ---- SHOW DJANGO MESSAGES ----
document.addEventListener('DOMContentLoaded', () => {
  const msgs = document.getElementById('django-messages');
  if (msgs) {
    msgs.querySelectorAll('span').forEach(m => showToast(m.textContent));
  }
});
