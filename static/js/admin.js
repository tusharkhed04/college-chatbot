// ── State ─────────────────────────────────────────────────────────────
let currentYear    = 0;
let currentSection = "timetable";
let editingId      = null;
let editingType    = null;
let subjectsList   = [];
let facultyList    = [];

// ── API Helper ────────────────────────────────────────────────────────
async function api(url, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  return res.json();
}

function val(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : "";
}

function toast(msg, type = "success") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();
  const t = document.createElement("div");
  t.className = `toast toast-${type}`;
  t.textContent = (type === "success" ? "✅ " : "❌ ") + msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

// ── Login ─────────────────────────────────────────────────────────────
document.getElementById("admin-login-btn").addEventListener("click", doLogin);
document.getElementById("admin-pass").addEventListener("keydown", e => {
  if (e.key === "Enter") doLogin();
});

async function doLogin() {
  const password = document.getElementById("admin-pass").value;
  const errEl    = document.getElementById("admin-error");
  errEl.textContent = "";
  try {
    const res = await api("/admin/login", "POST", { password });
    if (res.error) { errEl.textContent = res.error; return; }
    document.getElementById("admin-login").classList.add("hidden");
    document.getElementById("admin-panel").classList.remove("hidden");
    await loadDropdownData();
    loadSection();
  } catch (e) {
    errEl.textContent = "Login failed. Try again.";
  }
}

document.getElementById("admin-logout-btn").addEventListener("click", async () => {
  await api("/admin/logout", "POST");
  document.getElementById("admin-panel").classList.add("hidden");
  document.getElementById("admin-login").classList.remove("hidden");
  document.getElementById("admin-pass").value = "";
});

// ── Year Filter ───────────────────────────────────────────────────────
document.querySelectorAll(".year-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".year-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentYear = parseInt(btn.dataset.year);
    loadSection();
  });
});

// ── Section Tabs ──────────────────────────────────────────────────────
document.querySelectorAll(".sec-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".sec-tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    tab.classList.add("active");
    currentSection = tab.dataset.section;
    document.getElementById("section-" + currentSection).classList.add("active");
    loadSection();
  });
});

function loadSection() {
  if      (currentSection === "timetable") loadTimetable();
  else if (currentSection === "exams")     loadExams();
  else if (currentSection === "faculty")   loadFaculty();
  else if (currentSection === "syllabus")  loadSyllabus();
}

// ── Add Buttons ───────────────────────────────────────────────────────
document.getElementById("btn-add-timetable").addEventListener("click", () => openModal("timetable"));
document.getElementById("btn-add-exam").addEventListener("click",      () => openModal("exam"));
document.getElementById("btn-add-faculty").addEventListener("click",   () => openModal("faculty"));
document.getElementById("btn-add-syllabus").addEventListener("click",  () => openModal("syllabus"));

// ── Modal Controls ────────────────────────────────────────────────────
document.getElementById("modal-close-btn").addEventListener("click",  closeModal);
document.getElementById("modal-cancel-btn").addEventListener("click", closeModal);
document.getElementById("modal-overlay").addEventListener("click", e => {
  if (e.target === document.getElementById("modal-overlay")) closeModal();
});
document.getElementById("modal-save-btn").addEventListener("click", () => {
  saveModal(editingType);
});

// ── Load Dropdown Data ────────────────────────────────────────────────
async function loadDropdownData() {
  try {
    const [subs, facs] = await Promise.all([
      api("/admin/subjects-list"),
      api("/admin/faculty-list"),
    ]);
    subjectsList = Array.isArray(subs) ? subs : [];
    facultyList  = Array.isArray(facs) ? facs : [];
  } catch (e) {
    subjectsList = [];
    facultyList  = [];
  }
}

// ── TIMETABLE ─────────────────────────────────────────────────────────
async function loadTimetable() {
  try {
    const url  = "/admin/timetable" + (currentYear ? `?year=${currentYear}` : "");
    const rows = await api(url);
    const tbody = document.getElementById("timetable-body");
    if (!Array.isArray(rows) || rows.length === 0) {
      tbody.innerHTML = `<tr><td class="empty-td" colspan="7">No timetable entries found.</td></tr>`;
      return;
    }
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td><span class="badge badge-blue">Year ${r.year}</span></td>
        <td>${r.branch}</td>
        <td>${r.day}</td>
        <td>${r.time_slot}</td>
        <td>${r.subject}</td>
        <td>${r.room}</td>
        <td><div class="action-btns">
          <button class="btn-edit"   data-type="timetable" data-row='${JSON.stringify(r)}'>Edit</button>
          <button class="btn-delete" data-type="timetable" data-id="${r.id}">Delete</button>
        </div></td>
      </tr>`).join("");
    attachRowActions();
  } catch (e) {
    document.getElementById("timetable-body").innerHTML = `<tr><td class="empty-td" colspan="7">Failed to load.</td></tr>`;
  }
}

// ── EXAMS ─────────────────────────────────────────────────────────────
async function loadExams() {
  try {
    const url  = "/admin/exams" + (currentYear ? `?year=${currentYear}` : "");
    const rows = await api(url);
    const tbody = document.getElementById("exams-body");
    if (!Array.isArray(rows) || rows.length === 0) {
      tbody.innerHTML = `<tr><td class="empty-td" colspan="8">No exam entries found.</td></tr>`;
      return;
    }
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td><span class="badge badge-blue">Year ${r.year}</span></td>
        <td>${r.branch}</td>
        <td><span class="badge ${r.exam_type === 'Mid-Term' ? 'badge-yellow' : 'badge-green'}">${r.exam_type}</span></td>
        <td>${r.subject}</td>
        <td>${r.exam_date}</td>
        <td>${r.start_time}</td>
        <td>${r.room}</td>
        <td><div class="action-btns">
          <button class="btn-edit"   data-type="exam" data-row='${JSON.stringify(r)}'>Edit</button>
          <button class="btn-delete" data-type="exam" data-id="${r.id}">Delete</button>
        </div></td>
      </tr>`).join("");
    attachRowActions();
  } catch (e) {
    document.getElementById("exams-body").innerHTML = `<tr><td class="empty-td" colspan="8">Failed to load.</td></tr>`;
  }
}

// ── FACULTY ───────────────────────────────────────────────────────────
async function loadFaculty() {
  try {
    const rows  = await api("/admin/faculty");
    const tbody = document.getElementById("faculty-body");
    if (!Array.isArray(rows) || rows.length === 0) {
      tbody.innerHTML = `<tr><td class="empty-td" colspan="7">No faculty found.</td></tr>`;
      return;
    }
    tbody.innerHTML = rows.map(f => `
      <tr>
        <td><b>${f.name}</b></td>
        <td>${f.department}</td>
        <td>${f.subject}</td>
        <td>${f.email}</td>
        <td>${f.cabin}</td>
        <td>${f.phone}</td>
        <td><div class="action-btns">
          <button class="btn-edit"   data-type="faculty" data-row='${JSON.stringify(f)}'>Edit</button>
          <button class="btn-delete" data-type="faculty" data-id="${f.id}">Delete</button>
        </div></td>
      </tr>`).join("");
    attachRowActions();
  } catch (e) {
    document.getElementById("faculty-body").innerHTML = `<tr><td class="empty-td" colspan="7">Failed to load.</td></tr>`;
  }
}

// ── SYLLABUS ──────────────────────────────────────────────────────────
async function loadSyllabus() {
  try {
    const url   = "/admin/syllabus" + (currentYear ? `?year=${currentYear}` : "");
    const rows  = await api(url);
    const tbody = document.getElementById("syllabus-body");
    if (!Array.isArray(rows) || rows.length === 0) {
      tbody.innerHTML = `<tr><td class="empty-td" colspan="8">No subjects found.</td></tr>`;
      return;
    }
    tbody.innerHTML = rows.map(s => `
      <tr>
        <td><span class="badge badge-blue">Year ${s.year}</span></td>
        <td>Sem ${s.semester}</td>
        <td><span class="badge badge-green">${s.code}</span></td>
        <td><b>${s.name}</b></td>
        <td>${s.branch}</td>
        <td>${s.credits} Cr</td>
        <td>${s.faculty}</td>
        <td><div class="action-btns">
          <button class="btn-edit"   data-type="syllabus" data-row='${JSON.stringify(s)}'>Edit</button>
          <button class="btn-delete" data-type="syllabus" data-id="${s.id}">Delete</button>
        </div></td>
      </tr>`).join("");
    attachRowActions();
  } catch (e) {
    document.getElementById("syllabus-body").innerHTML = `<tr><td class="empty-td" colspan="8">Failed to load.</td></tr>`;
  }
}

// ── Attach Edit/Delete Buttons ────────────────────────────────────────
function attachRowActions() {
  document.querySelectorAll(".btn-edit").forEach(btn => {
    btn.addEventListener("click", () => {
      const type = btn.dataset.type;
      const row  = JSON.parse(btn.dataset.row);
      openModal(type, row);
    });
  });
  document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", () => {
      deleteEntry(btn.dataset.type, btn.dataset.id);
    });
  });
}

// ── MODAL ─────────────────────────────────────────────────────────────
function openModal(type, data = null) {
  editingId   = data ? data.id : null;
  editingType = type;

  const titles = {
    timetable: "Timetable Entry",
    exam:      "Exam Schedule",
    faculty:   "Faculty",
    syllabus:  "Subject"
  };
  document.getElementById("modal-title").textContent = (data ? "Edit " : "Add ") + titles[type];
  document.getElementById("modal-body").innerHTML    = buildForm(type, data || {});
  document.getElementById("modal-overlay").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
  editingId   = null;
  editingType = null;
}

// ── Form Builder ──────────────────────────────────────────────────────
function buildForm(type, d) {
  const subjectOptions = subjectsList.map(s =>
    `<option value="${s.id}" ${d.subject_id == s.id ? "selected" : ""}>${s.name} (Year ${s.year})</option>`
  ).join("");

  const facultyOptions = facultyList.map(f =>
    `<option value="${f.id}" ${d.faculty_id == f.id ? "selected" : ""}>${f.name}</option>`
  ).join("");

  const dayOptions = ["Monday","Tuesday","Wednesday","Thursday","Friday"].map(day =>
    `<option value="${day}" ${d.day === day ? "selected" : ""}>${day}</option>`
  ).join("");

  const yearOptions = [1,2,3,4].map(y =>
    `<option value="${y}" ${d.year == y ? "selected" : ""}>Year ${y}</option>`
  ).join("");

  const branchOptions = ["CSE","IT","MECH","CIVIL"].map(b =>
    `<option value="${b}" ${d.branch === b ? "selected" : ""}>${b}</option>`
  ).join("");

  if (type === "timetable") {
    return `
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">BRANCH</label>
          <select id="f-branch"><option value="">Select Branch</option>${branchOptions}</select>
        </div>
        <div class="field-group">
          <label class="field-label">YEAR</label>
          <select id="f-year"><option value="">Select Year</option>${yearOptions}</select>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">DAY</label>
          <select id="f-day"><option value="">Select Day</option>${dayOptions}</select>
        </div>
        <div class="field-group">
          <label class="field-label">TIME SLOT</label>
          <input id="f-slot" placeholder="e.g. 9:00-10:00" value="${d.time_slot || ''}"/>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label">SUBJECT</label>
        <select id="f-subject">
          <option value="">Select Subject</option>${subjectOptions}
        </select>
      </div>
      <div class="field-group">
        <label class="field-label">ROOM</label>
        <input id="f-room" placeholder="e.g. CS-201" value="${d.room || ''}"/>
      </div>`;
  }

  if (type === "exam") {
    return `
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">BRANCH</label>
          <select id="f-branch"><option value="">Select Branch</option>${branchOptions}</select>
        </div>
        <div class="field-group">
          <label class="field-label">YEAR</label>
          <select id="f-year"><option value="">Select Year</option>${yearOptions}</select>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">EXAM TYPE</label>
          <select id="f-exam-type">
            <option value="Mid-Term"  ${d.exam_type === "Mid-Term"  ? "selected" : ""}>Mid-Term</option>
            <option value="End-Term"  ${d.exam_type === "End-Term"  ? "selected" : ""}>End-Term</option>
            <option value="Practical" ${d.exam_type === "Practical" ? "selected" : ""}>Practical</option>
            <option value="Viva"      ${d.exam_type === "Viva"      ? "selected" : ""}>Viva</option>
          </select>
        </div>
        <div class="field-group">
          <label class="field-label">SUBJECT</label>
          <select id="f-subject">
            <option value="">Select Subject</option>${subjectOptions}
          </select>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">EXAM DATE</label>
          <input id="f-date" type="date" value="${d.exam_date || ''}"/>
        </div>
        <div class="field-group">
          <label class="field-label">START TIME</label>
          <input id="f-time" type="time" value="${d.start_time || '10:00'}"/>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label">ROOM / HALL</label>
        <input id="f-room" placeholder="e.g. Exam Hall A" value="${d.room || ''}"/>
      </div>`;
  }

  if (type === "faculty") {
    return `
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">FULL NAME</label>
          <input id="f-name" placeholder="Dr. / Prof. Name" value="${d.name || ''}"/>
        </div>
        <div class="field-group">
          <label class="field-label">DEPARTMENT</label>
          <input id="f-dept" placeholder="e.g. Computer Science" value="${d.department || ''}"/>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">SUBJECT TAUGHT</label>
          <input id="f-subject-name" placeholder="e.g. Data Structures" value="${d.subject || ''}"/>
        </div>
        <div class="field-group">
          <label class="field-label">CABIN NO.</label>
          <input id="f-cabin" placeholder="e.g. CS-101" value="${d.cabin || ''}"/>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">EMAIL</label>
          <input id="f-email" type="email" placeholder="name@college.edu" value="${d.email || ''}"/>
        </div>
        <div class="field-group">
          <label class="field-label">PHONE</label>
          <input id="f-phone" placeholder="10-digit number" value="${d.phone || ''}"/>
        </div>
      </div>`;
  }

  if (type === "syllabus") {
    return `
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">SUBJECT NAME</label>
          <input id="f-name" placeholder="e.g. Data Structures" value="${d.name || ''}"/>
        </div>
        <div class="field-group">
          <label class="field-label">SUBJECT CODE</label>
          <input id="f-code" placeholder="e.g. CS201" value="${d.code || ''}"/>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">BRANCH</label>
          <select id="f-branch"><option value="">Select Branch</option>${branchOptions}</select>
        </div>
        <div class="field-group">
          <label class="field-label">YEAR</label>
          <select id="f-year"><option value="">Select Year</option>${yearOptions}</select>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <label class="field-label">SEMESTER</label>
          <select id="f-sem">
            ${[1,2,3,4,5,6,7,8].map(s => `<option value="${s}" ${d.semester == s ? "selected" : ""}>Semester ${s}</option>`).join("")}
          </select>
        </div>
        <div class="field-group">
          <label class="field-label">CREDITS</label>
          <select id="f-credits">
            ${[1,2,3,4,5].map(c => `<option value="${c}" ${d.credits == c ? "selected" : ""}>${c} Credits</option>`).join("")}
          </select>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label">ASSIGN FACULTY</label>
        <select id="f-faculty">
          <option value="">Not Assigned</option>${facultyOptions}
        </select>
      </div>`;
  }

  return "";
}

// ── Save Modal ────────────────────────────────────────────────────────
async function saveModal(type) {
  let payload = {};
  let url, method;

  if (type === "timetable") {
    payload = {
      branch:     val("f-branch"),
      year:       val("f-year"),
      day:        val("f-day"),
      time_slot:  val("f-slot"),
      subject_id: val("f-subject"),
      room:       val("f-room"),
    };
    if (!payload.branch || !payload.year || !payload.day || !payload.time_slot || !payload.subject_id || !payload.room) {
      return toast("Please fill all fields", "error");
    }
    url    = editingId ? `/admin/timetable/${editingId}` : "/admin/timetable";
    method = editingId ? "PUT" : "POST";
  }

  else if (type === "exam") {
    payload = {
      branch:     val("f-branch"),
      year:       val("f-year"),
      exam_type:  val("f-exam-type"),
      subject_id: val("f-subject"),
      exam_date:  val("f-date"),
      start_time: val("f-time"),
      room:       val("f-room"),
    };
    if (!payload.branch || !payload.year || !payload.subject_id || !payload.exam_date) {
      return toast("Please fill all required fields", "error");
    }
    url    = editingId ? `/admin/exams/${editingId}` : "/admin/exams";
    method = editingId ? "PUT" : "POST";
  }

  else if (type === "faculty") {
    payload = {
      name:       val("f-name"),
      department: val("f-dept"),
      subject:    val("f-subject-name"),
      cabin:      val("f-cabin"),
      email:      val("f-email"),
      phone:      val("f-phone"),
    };
    if (!payload.name || !payload.department) {
      return toast("Name and department are required", "error");
    }
    url    = editingId ? `/admin/faculty/${editingId}` : "/admin/faculty";
    method = editingId ? "PUT" : "POST";
  }

  else if (type === "syllabus") {
    payload = {
      name:       val("f-name"),
      code:       val("f-code"),
      branch:     val("f-branch"),
      year:       val("f-year"),
      semester:   val("f-sem"),
      credits:    val("f-credits"),
      faculty_id: val("f-faculty") || null,
    };
    if (!payload.name || !payload.code || !payload.branch || !payload.year) {
      return toast("Please fill all required fields", "error");
    }
    url    = editingId ? `/admin/syllabus/${editingId}` : "/admin/syllabus";
    method = editingId ? "PUT" : "POST";
  }

  try {
    const res = await api(url, method, payload);
    if (res.error) return toast(res.error, "error");
    toast(editingId ? "Updated successfully!" : "Added successfully!", "success");
    closeModal();
    await loadDropdownData();
    loadSection();
  } catch (e) {
    toast("Save failed. Try again.", "error");
  }
}

// ── Delete ────────────────────────────────────────────────────────────
async function deleteEntry(type, id) {
  if (!confirm("Are you sure you want to delete this entry?")) return;
  const urlMap = {
    timetable: "timetable",
    exam:      "exams",
    faculty:   "faculty",
    syllabus:  "syllabus"
  };
  try {
    const res = await api(`/admin/${urlMap[type]}/${id}`, "DELETE");
    if (res.error) return toast(res.error, "error");
    toast("Deleted successfully!", "success");
    await loadDropdownData();
    loadSection();
  } catch (e) {
    toast("Delete failed.", "error");
  }
}
