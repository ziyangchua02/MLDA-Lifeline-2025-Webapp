// Restrict inputs to digits and a single decimal point
(function() {
  const sanitize = (raw) => {
    if (!raw) return "";
    let v = String(raw).replace(/,/g, '.');
    v = v.replace(/[^0-9.]/g, '');
    const parts = v.split('.');
    if (parts.length > 2) {
      v = parts.shift() + '.' + parts.join('');
    }
    return v;
  };

  const inputs = document.querySelectorAll('#ctg-form input[type="text"], #ctg-form input[type="number"]');
  inputs.forEach((el) => {
    el.value = sanitize(el.value);

    el.addEventListener('input', (e) => {
      const selStart = el.selectionStart;
      const oldLen = el.value.length;
      el.value = sanitize(el.value);
      const newLen = el.value.length;
      const diff = newLen - oldLen;
      try { el.setSelectionRange(Math.max(0, selStart + diff), Math.max(0, selStart + diff)); } catch (err) {}
    });
  });
})();

const form = document.getElementById("ctg-form");
const resultDiv = document.getElementById("result");

// Create toast element for predictions
const toast = document.createElement('div');
toast.className = 'prediction-toast';
document.body.appendChild(toast);

function showPredictionToast(label) {
  const key = String(label).toLowerCase();
  toast.className = 'prediction-toast visible ' + (key === 'normal' ? 'normal' : key === 'suspect' ? 'suspect' : 'pathologic');
  toast.classList.add('fullscreen');
  toast.textContent = label;
  clearTimeout(toast._hideTimer);
  toast._hideTimer = setTimeout(() => {
    toast.className = 'prediction-toast';
    toast.classList.remove('fullscreen');
  }, 4000);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultDiv.textContent = "";
  const data = {};
  const fm = new FormData(form);
  for (const [k, v] of fm.entries()) data[k] = parseFloat(v);

  try {
        const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const text = await res.text();
    let json = null;
    if (text) {
      try { json = JSON.parse(text); } catch (parseErr) {}
    }

    if (res.ok) {
      if (json && json.prediction) {
        showPredictionToast(json.prediction);
      } else if (text) {
        resultDiv.textContent = "Response: " + text;
      } else {
        resultDiv.textContent = `Empty response (status ${res.status})`;
      }
    } else {
      const errMsg = (json && (json.error || json.detail)) || text || `HTTP ${res.status}`;
      resultDiv.textContent = "Error: " + errMsg;
    }
  } catch (err) {
    resultDiv.textContent = "Request failed: " + err.message;
  }
});
