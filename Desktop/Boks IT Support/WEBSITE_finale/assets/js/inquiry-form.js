/** Client-side inquiry form submitter with accessible status messages. */

const DEFAULT_SUCCESS =
  "Danke. Ihre Angaben sind eingegangen. Rückmeldung in der Regel innerhalb von zwei Arbeitstagen.";
const DEFAULT_SAVED_NOTE =
  " Ihre Anfrage wurde gespeichert. Die E-Mail-Benachrichtigung kann kurz verzögert sein.";
const DEFAULT_ERROR =
  "Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es später erneut oder schreiben Sie an admin@boksitsupport.ch.";
const INQUIRY_TO = "admin@boksitsupport.ch";

function collect(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  data.privacy = form.elements.namedItem("privacy")?.checked === true;
  return data;
}

function setStatus(el, message, isError) {
  if (!el) return;
  el.textContent = message;
  el.dataset.state = isError ? "error" : "ok";
}

/** True when the build gated the form (inquiry.live: false). */
export function isInquiryOffline(form) {
  return form?.dataset?.inquiryOffline === "true";
}

/** Force HTML disabled on the submit control; never leave it clickable offline. */
export function enforceOfflineSubmit(form) {
  if (!form || !isInquiryOffline(form)) return;
  const button = form.querySelector('button[type="submit"]');
  if (!button) return;
  button.disabled = true;
  button.setAttribute("disabled", "disabled");
  button.setAttribute("aria-disabled", "true");
}

/** Build a mailto: URL that preserves every entered field in the body. */
export function buildMailtoHref(data) {
  const subject = `BIT Anfrage: ${data.company || ""} · ${data.area || ""}`;
  const body = [
    `Firma: ${data.company || ""}`,
    `Name: ${data.first_name || ""} ${data.last_name || ""}`,
    `E-Mail: ${data.email || ""}`,
    `Telefon: ${data.phone || "—"}`,
    `Standort: ${data.location || "—"}`,
    `Branche: ${data.industry || "—"}`,
    `Mitarbeitende: ${data.employees || ""}`,
    `Arbeitsplätze: ${data.workstations || "—"}`,
    `M365: ${data.m365 || "—"}`,
    `Interne IT: ${data.internal_it || "—"}`,
    `Externe IT: ${data.external_it || "—"}`,
    `Bereich: ${data.area || ""}`,
    `Start: ${data.start || "—"}`,
    "",
    data.description || "",
  ].join("\n");
  return (
    `mailto:${INQUIRY_TO}` +
    `?subject=${encodeURIComponent(subject)}` +
    `&body=${encodeURIComponent(body)}`
  );
}

/** Show error text plus a mailto link; never clear the form. */
function showFailure(status, errorMsg, data) {
  if (!status) return;
  status.dataset.state = "error";
  status.replaceChildren();
  const text = document.createElement("span");
  text.textContent = `${errorMsg} `;
  const link = document.createElement("a");
  link.href = buildMailtoHref(data);
  link.textContent = "Stattdessen per E-Mail senden (Angaben übernommen)";
  status.append(text, link);
}

async function onSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;

  // Offline: HTML disabled + early return — no fetch, no field clear, no error UI.
  if (isInquiryOffline(form)) {
    enforceOfflineSubmit(form);
    return;
  }

  const status = form.querySelector("#inquiry-status");
  const button = form.querySelector('button[type="submit"]');
  const successMsg = form.dataset.success || DEFAULT_SUCCESS;
  const errorMsg = form.dataset.error || DEFAULT_ERROR;
  const data = collect(form);

  if (!form.reportValidity()) {
    // Keep all field values on validation failure.
    showFailure(status, errorMsg, data);
    return;
  }

  button.disabled = true;
  setStatus(status, "…", false);

  try {
    const response = await fetch("/api/inquiry", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(data),
    });
    const payload = await response.json().catch(() => ({}));
    if (response.ok && payload.ok) {
      // KV success is enough for the user; soft note if push notify did not fire.
      const notifyMissed =
        payload.notified === false || payload.emailQueued === false;
      const msg = notifyMissed ? `${successMsg}${DEFAULT_SAVED_NOTE}` : successMsg;
      setStatus(status, msg, false);
      form.reset();
      return;
    }

    // Keep all field values. Offer mailto with the entered data.
    showFailure(status, errorMsg, data);
  } catch {
    showFailure(status, errorMsg, data);
  } finally {
    if (isInquiryOffline(form)) {
      enforceOfflineSubmit(form);
    } else if (button) {
      button.disabled = false;
    }
  }
}

/** Block submit in capture phase while offline (defence in depth). */
function onSubmitCapture(event) {
  const form = event.currentTarget;
  if (!isInquiryOffline(form)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  enforceOfflineSubmit(form);
}

/** Preselect area (and other fields) from ?area= URL params when present. */
function applyQueryParams(form) {
  const params = new URLSearchParams(window.location.search);
  const area = params.get("area");
  if (!area) return;
  const select = form.elements.namedItem("area");
  if (!(select instanceof HTMLSelectElement)) return;
  const match = [...select.options].find((opt) => opt.value === area);
  if (match) {
    select.value = area;
  }
}

const form = document.getElementById("inquiry-form");
if (form) {
  applyQueryParams(form);
  enforceOfflineSubmit(form);
  form.addEventListener("submit", onSubmitCapture, true);
  form.addEventListener("submit", onSubmit);
}
