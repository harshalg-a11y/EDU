const AUTH_TOKEN_KEY = 'edu_auth_token';
const AUTH_EXP_KEY = 'edu_auth_exp';
const AUTH_USER_KEY = 'edu_auth_user';
const AUTH_MODE_KEY = 'edu_auth_mode';
const AUTH_USERS_KEY = 'edu_users';

const Auth = {
  async hash(text) {
    const bytes = new TextEncoder().encode(text);
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, '0')).join('');
  },

  users() {
    return JSON.parse(localStorage.getItem(AUTH_USERS_KEY) || '{}');
  },

  saveUsers(users) {
    localStorage.setItem(AUTH_USERS_KEY, JSON.stringify(users));
  },

  tokenValid() {
    const token = localStorage.getItem(AUTH_TOKEN_KEY) || sessionStorage.getItem(AUTH_TOKEN_KEY);
    const exp = Number(localStorage.getItem(AUTH_EXP_KEY) || sessionStorage.getItem(AUTH_EXP_KEY) || 0);
    if (!token || !exp || Date.now() > exp) return false;
    return true;
  },

  setSession(email, remember) {
    const exp = Date.now() + (remember ? 30 : 1) * 24 * 60 * 60 * 1000;
    const store = remember ? localStorage : sessionStorage;
    const clear = remember ? sessionStorage : localStorage;
    clear.removeItem(AUTH_TOKEN_KEY); clear.removeItem(AUTH_EXP_KEY); clear.removeItem(AUTH_USER_KEY);
    store.setItem(AUTH_TOKEN_KEY, `tok_${crypto.randomUUID()}`);
    store.setItem(AUTH_EXP_KEY, String(exp));
    store.setItem(AUTH_USER_KEY, email);
    localStorage.setItem(AUTH_MODE_KEY, remember ? 'remember' : 'session');
  },

  logout() {
    [localStorage, sessionStorage].forEach((s) => {
      s.removeItem(AUTH_TOKEN_KEY); s.removeItem(AUTH_EXP_KEY); s.removeItem(AUTH_USER_KEY);
    });
    localStorage.removeItem(AUTH_MODE_KEY);
    window.location.href = '/index.html';
  },
};

function navState() {
  const page = document.body.dataset.page || 'dashboard';
  document.querySelectorAll('.nav-link').forEach((el) => {
    el.classList.toggle('active', el.dataset.nav === page);
  });
  const crumb = document.getElementById('breadcrumbCurrent');
  if (crumb) crumb.textContent = page[0].toUpperCase() + page.slice(1);
}

function guardPage() {
  const page = document.body.dataset.page || 'dashboard';
  if (page !== 'dashboard' && !Auth.tokenValid()) {
    window.location.href = '/index.html';
    return false;
  }
  return true;
}

function toggleAuth(show) {
  const overlay = document.getElementById('authOverlay');
  if (!overlay) return;
  overlay.classList.toggle('active', show);
}

function passwordValid(password) {
  return /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/.test(password);
}

function bindAuth() {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const msg = document.getElementById('authMsg');
  const tabs = document.querySelectorAll('.auth-tab');

  tabs.forEach((tab) => tab.addEventListener('click', () => {
    tabs.forEach((t) => t.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.form').forEach((f) => (f.style.display = 'none'));
    document.getElementById(`${tab.dataset.target}Form`).style.display = 'flex';
    msg.textContent = '';
  }));

  loginForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim().toLowerCase();
    const password = document.getElementById('loginPassword').value;
    const remember = document.getElementById('rememberMe').checked;
    const users = Auth.users();
    const hashed = await Auth.hash(password);

    if (!users[email] || users[email].password !== hashed) {
      msg.textContent = 'Invalid credentials.';
      msg.className = 'msg error';
      return;
    }

    Auth.setSession(email, remember);
    msg.textContent = 'Signed in successfully.';
    msg.className = 'msg';
    toggleAuth(false);
    window.location.reload();
  });

  registerForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value.trim().toLowerCase();
    const password = document.getElementById('registerPassword').value;
    const confirm = document.getElementById('registerConfirm').value;
    const users = Auth.users();

    if (!email.includes('@')) {
      msg.textContent = 'Enter a valid email.';
      msg.className = 'msg error';
      return;
    }
    if (!passwordValid(password)) {
      msg.textContent = 'Password must be 8+ chars with upper, lower, and number.';
      msg.className = 'msg error';
      return;
    }
    if (password !== confirm) {
      msg.textContent = 'Passwords do not match.';
      msg.className = 'msg error';
      return;
    }
    if (users[email]) {
      msg.textContent = 'Account already exists.';
      msg.className = 'msg error';
      return;
    }

    users[email] = { password: await Auth.hash(password), createdAt: Date.now() };
    Auth.saveUsers(users);
    msg.textContent = 'Account created. Please sign in.';
    msg.className = 'msg';
    document.querySelector('.auth-tab[data-target="login"]').click();
  });
}

async function loadDashboard() {
  const metricsEl = document.getElementById('metricsGrid');
  const conflictsEl = document.getElementById('alertsList');
  if (!metricsEl || !conflictsEl) return;

  try {
    const [metricsRes, conflictsRes] = await Promise.all([
      fetch('http://localhost:8000/api/metrics'),
      fetch('http://localhost:8000/api/conflicts'),
    ]);

    const metrics = await metricsRes.json();
    const conflicts = await conflictsRes.json();

    metricsEl.innerHTML = metrics.map((m) => `
      <article class="metric-card"><div class="metric-value">${m.value}</div><div class="metric-label">${m.name} · ${m.unit}</div></article>
    `).join('');

    conflictsEl.innerHTML = (conflicts.length ? conflicts : [{ title: 'No active alerts', description: 'System status nominal', severity: 'low' }]).map((c) => `
      <article class="item"><strong>${c.title}</strong><br><small>${c.description}</small></article>
    `).join('');
  } catch {
    metricsEl.innerHTML = '<article class="metric-card"><div class="metric-label">API unavailable</div></article>';
    conflictsEl.innerHTML = '<article class="item"><small>Unable to load alerts.</small></article>';
  }
}

function bindGlobal() {
  document.getElementById('logoutBtn')?.addEventListener('click', Auth.logout);
  document.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', (e) => {
      document.body.classList.add('page-transition');
      setTimeout(() => { document.body.classList.remove('page-transition'); }, 250);
    });
  });
}

function init() {
  if (!guardPage()) return;
  navState();
  bindGlobal();
  bindAuth();

  const isDashboard = (document.body.dataset.page || 'dashboard') === 'dashboard';
  if (isDashboard) {
    const loggedIn = Auth.tokenValid();
    toggleAuth(!loggedIn);
    if (loggedIn) loadDashboard();
  }
}

document.addEventListener('DOMContentLoaded', init);
