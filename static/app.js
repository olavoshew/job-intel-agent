var cvFileText = "";

document.getElementById("cv-file").addEventListener("change", function (e) {
    var file = e.target.files[0];
    if (!file) { cvFileText = ""; return; }
    var reader = new FileReader();
    reader.onload = function (ev) { cvFileText = ev.target.result; };
    reader.readAsText(file);
});

document.getElementById("cv-toggle").addEventListener("click", function () {
    var wrap = document.getElementById("cv-paste");
    var open = wrap.style.display !== "none";
    wrap.style.display = open ? "none" : "block";
    this.textContent = open ? "Paste CV Manually" : "Hide CV Input";
});

function getFormData() {
    return {
        input: document.getElementById("input").value.trim(),
        cv: cvFileText || document.getElementById("cv").value.trim(),
        demo: document.getElementById("demo").checked,
        apiKey: document.getElementById("apikey").value.trim(),
        provider: document.getElementById("provider").value,
    };
}

function buildBody(form, requireCv) {
    var body = {};
    if (form.demo) {
        body.demo = true;
        return body;
    }
    if (form.input.startsWith("http://") || form.input.startsWith("https://")) {
        body.url = form.input;
    } else if (form.input.length > 0) {
        body.text = form.input;
    } else {
        throw new Error("Enter a URL or paste job description text.");
    }
    if (!form.apiKey) {
        throw new Error("Enter your API key or use demo mode.");
    }
    if (requireCv && !form.cv) {
        throw new Error("Paste your CV text to get a rewrite.");
    }
    body.api_key = form.apiKey;
    body.provider = form.provider;
    if (form.cv) {
        body.cv_text = form.cv;
    }
    return body;
}

function setButton(btn, disabled, text) {
    btn.disabled = disabled;
    btn.textContent = text;
}

function renderAnalyze(data) {
    document.getElementById("score-val").textContent = data.match_percentage;
    var gapsUl = document.getElementById("gaps");
    gapsUl.innerHTML = "";
    data.gap_list.forEach(function (g) {
        var li = document.createElement("li");
        li.textContent = g;
        gapsUl.appendChild(li);
    });
    var pointsUl = document.getElementById("points");
    pointsUl.innerHTML = "";
    data.talking_points.forEach(function (p) {
        var li = document.createElement("li");
        li.textContent = p;
        pointsUl.appendChild(li);
    });
    document.getElementById("pitch").textContent = data.pitch;
    document.getElementById("results").style.display = "block";
}

function renderRewrite(data) {
    var tipsEl = document.getElementById("tips");
    tipsEl.innerHTML = "";
    data.tips.forEach(function (t) {
        var div = document.createElement("div");
        div.className = "tip";
        div.innerHTML = "<strong>" + t.section + ":</strong> " + t.problem + "<br><em>" + t.suggestion + "</em>";
        tipsEl.appendChild(div);
    });
    document.getElementById("rewritten-cv").textContent = data.rewritten_cv;
    document.getElementById("rewrite-results").style.display = "block";
}

async function submitRequest(endpoint, body) {
    var resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    if (!resp.ok) {
        var err = await resp.json();
        throw new Error(err.detail || "Request failed");
    }
    return await resp.json();
}

var errorEl = document.getElementById("error");

document.getElementById("form").addEventListener("submit", async function (e) {
    e.preventDefault();
    var btn = document.getElementById("btn");
    errorEl.textContent = "";
    document.getElementById("results").style.display = "none";
    setButton(btn, true, "Analyzing...");
    try {
        var form = getFormData();
        var body = buildBody(form, false);
        var data = await submitRequest("/analyze", body);
        renderAnalyze(data);
    } catch (err) {
        errorEl.textContent = err.message;
    } finally {
        setButton(btn, false, "Analyze");
    }
});

document.getElementById("rewrite-btn").addEventListener("click", async function () {
    var btn = document.getElementById("rewrite-btn");
    errorEl.textContent = "";
    document.getElementById("rewrite-results").style.display = "none";
    setButton(btn, true, "Rewriting...");
    try {
        var form = getFormData();
        var body = buildBody(form, true);
        var data = await submitRequest("/rewrite", body);
        renderRewrite(data);
    } catch (err) {
        errorEl.textContent = err.message;
    } finally {
        setButton(btn, false, "Rewrite CV");
    }
});

document.getElementById("copy-btn").addEventListener("click", function () {
    var text = document.getElementById("rewritten-cv").textContent;
    navigator.clipboard.writeText(text).then(function () {
        var btn = document.getElementById("copy-btn");
        btn.textContent = "Copied!";
        setTimeout(function () { btn.textContent = "Copy to clipboard"; }, 2000);
    });
});
