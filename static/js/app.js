// ── Elements ──────────────────────────────────────────────────────────
const authGate    = document.getElementById("auth-gate");
const appShell    = document.getElementById("app-shell");
const chatWindow  = document.getElementById("chat-window");
const chatInput   = document.getElementById("chat-input");
const sendBtn     = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");
const clearBtn    = document.getElementById("clear-btn");
const contextBadge = document.getElementById("context-badge");
const welcomeSplash = document.getElementById("welcome-splash");
const logoutBtn   = document.getElementById("logout-btn");
const sidebar     = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebar-toggle");

let currentContext = { branch: null, year: null };

// ── Auth Gate Tab Switching ───────────────────────────────────────────
document.querySelectorAll(".gate-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".gate-tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".gate-form").forEach(f => f.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById("gate-" + tab.dataset.tab).classList.add("active");
  });
});

// ── Login ─────────────────────────────────────────────────────────────
document.getElementById("g-login-btn").addEventListener("click", async () => {
  const email    = document.getElementById("g-login-email").value.trim();
  const password = document.getElementById("g-login-password").value.trim();
  const errEl    = document.getElementById("g-login-error");
  errEl.textContent = "";

  if (!email || !password) { errEl.textContent = "Please fill all fields."; return; }

  try {
    const res  = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.error) { errEl.textContent = data.error; return; }
    enterApp(data);
  } catch {
    errEl.textContent = "Login failed. Try again.";
  }
});

document.getElementById("g-login-password").addEventListener("keydown", e => {
  if (e.key === "Enter") document.getElementById("g-login-btn").click();
});

// ── Signup ────────────────────────────────────────────────────────────
document.getElementById("g-signup-btn").addEventListener("click", async () => {
  const name     = document.getElementById("g-signup-name").value.trim();
  const email    = document.getElementById("g-signup-email").value.trim();
  const password = document.getElementById("g-signup-password").value.trim();
  const branch   = document.getElementById("g-signup-branch").value;
  const year     = document.getElementById("g-signup-year").value;
  const errEl    = document.getElementById("g-signup-error");
  errEl.textContent = "";

  if (!name || !email || !password || !branch || !year) {
    errEl.textContent = "Please fill all fields."; return;
  }

  try {
    const res  = await fetch("/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, branch, year }),
    });
    const data = await res.json();
    if (data.error) { errEl.textContent = data.error; return; }
    enterApp(data);
  } catch {
    errEl.textContent = "Signup failed. Try again.";
  }
});

// ── Enter App after successful auth ───────────────────────────────────
function enterApp(data) {
  authGate.classList.add("hidden");
  appShell.classList.remove("hidden");

  document.getElementById("profile-name").textContent    = data.name;
  document.getElementById("profile-meta").textContent    = `${data.branch} · Year ${data.year}`;
  document.getElementById("profile-initials").textContent = data.name.charAt(0).toUpperCase();

  currentContext.branch = data.branch;
  currentContext.year   = data.year;
  updateContextBadge(currentContext);

  loadHistory();
  appendMessage("bot",
    `👋 Welcome, <b>${data.name}</b>! I'm your College Assistant.\n` +
    `Branch: <b>${data.branch}</b> · Year: <b>${data.year}</b>\n\n` +
    `Ask me about timetables, syllabus, faculty, or exams. Type <b>help</b> for options.`
  );
}

// ── Logout ────────────────────────────────────────────────────────────
logoutBtn.addEventListener("click", async () => {
  await fetch("/auth/logout", { method: "POST" });
  appShell.classList.add("hidden");
  authGate.classList.remove("hidden");
  chatWindow.innerHTML = "";
  chatWindow.appendChild(welcomeSplash);
  welcomeSplash.style.display = "";
  currentContext = { branch: null, year: null };
  contextBadge.textContent = "";
  document.getElementById("g-login-email").value    = "";
  document.getElementById("g-login-password").value = "";
  document.getElementById("g-login-error").textContent = "";
});

// ── Check existing session on load ───────────────────────────────────
async function checkAuth() {
  try {
    const res  = await fetch("/auth/me");
    const data = await res.json();
    if (data.logged_in) {
      enterApp(data);
    }
    // If not logged in, auth gate stays visible (default)
  } catch {}
}

// ── Chat Helpers ──────────────────────────────────────────────────────
function formatTime(d = new Date()) {
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function appendMessage(role, text) {
  if (welcomeSplash) welcomeSplash.style.display = "none";

  const row = document.createElement("div");
  row.className = `message-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = role === "bot" ? "🎓" : "👤";

  const inner = document.createElement("div");

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = text.replace(/\n/g, "<br/>");

  const time = document.createElement("div");
  time.className = "msg-time";
  time.textContent = formatTime();

  inner.appendChild(bubble);
  inner.appendChild(time);
  row.appendChild(avatar);
  row.appendChild(inner);
  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showTyping() {
  typingIndicator.classList.add("show");
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
function hideTyping() { typingIndicator.classList.remove("show"); }

function updateContextBadge(ctx) {
  contextBadge.textContent =
    ctx.branch || ctx.year
      ? `${ctx.branch || ""}${ctx.year ? " · Year " + ctx.year : ""}`
      : "";
}

// ── Send Message ──────────────────────────────────────────────────────
async function sendMessage(text) {
  const msg = text || chatInput.value.trim();
  if (!msg) return;
  chatInput.value = "";

  appendMessage("user", msg);
  showTyping();

  try {
    const payload = { message: msg };
    if (currentContext.branch) payload.branch = currentContext.branch;
    if (currentContext.year)   payload.year   = currentContext.year;

    const res  = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    hideTyping();

    if (res.status === 401) {
      // Session expired — kick back to login
      appShell.classList.add("hidden");
      authGate.classList.remove("hidden");
      return;
    }

    if (data.error) { appendMessage("bot", "⚠️ " + data.error); return; }

    appendMessage("bot", data.response);

    if (data.context) {
      if (data.context.branch) currentContext.branch = data.context.branch;
      if (data.context.year)   currentContext.year   = data.context.year;
      updateContextBadge(currentContext);
    }
  } catch {
    hideTyping();
    appendMessage("bot", "❌ Connection error. Please check the server.");
  }
}

async function loadHistory() {
  try {
    const res  = await fetch("/chat/history");
    if (res.status === 401) return;
    const data = await res.json();
    if (data.history && data.history.length > 0) {
      welcomeSplash.style.display = "none";
      data.history.forEach(h => appendMessage(h.role, h.message));
    }
  } catch {}
}

async function clearChat() {
  try {
    await fetch("/chat/clear", { method: "POST" });
    chatWindow.innerHTML = "";
    chatWindow.appendChild(welcomeSplash);
    welcomeSplash.style.display = "";
    currentContext = { branch: currentContext.branch, year: currentContext.year };
  } catch {}
}

// ── Event Listeners ───────────────────────────────────────────────────
sendBtn.addEventListener("click", () => sendMessage());
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
clearBtn.addEventListener("click", clearChat);

document.querySelectorAll(".qa-btn").forEach(btn => {
  btn.addEventListener("click", () => sendMessage(btn.dataset.msg));
});
document.querySelectorAll(".chip").forEach(chip => {
  chip.addEventListener("click", () => sendMessage(chip.dataset.msg));
});

sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("open"));
document.addEventListener("click", e => {
  if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
    sidebar.classList.remove("open");
  }
});

// ── Boot ──────────────────────────────────────────────────────────────
checkAuth();
