/**
 * Bookmarkable HTML inquiry viewer.
 * GET /api/inquiries/view?token=…&limit=20
 * Auth: ?token= (primary) or Authorization Bearer — INQUIRY_VIEW_TOKEN
 *       (fallback INQUIRY_DIAG_TOKEN). Missing secret → 503; wrong → 401.
 * Newest first. No frameworks. Mobile-first. noindex. no-store.
 */
const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 50;
const LIST_FETCH = 200;
const KEY_PREFIX = "inquiry:";
const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
const FORTY_EIGHT_H_MS = 48 * 60 * 60 * 1000;

function viewToken(env) {
  const view = String(env?.INQUIRY_VIEW_TOKEN || "").trim();
  if (view) return view;
  return String(env?.INQUIRY_DIAG_TOKEN || "").trim();
}

function extractBearer(request) {
  const header = request.headers.get("authorization") || "";
  const match = /^Bearer\s+(.+)$/i.exec(header.trim());
  return match ? match[1].trim() : "";
}

function parseLimit(raw) {
  const n = Number.parseInt(String(raw ?? ""), 10);
  if (!Number.isFinite(n) || n < 1) return DEFAULT_LIMIT;
  return Math.min(n, MAX_LIMIT);
}

/** Escape user/KV text for safe HTML embedding. */
export function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function parseReceivedAt(iso) {
  if (!iso) return NaN;
  const t = Date.parse(iso);
  return Number.isFinite(t) ? t : NaN;
}

export function countLast7Days(items, nowMs = Date.now()) {
  const cutoff = nowMs - SEVEN_DAYS_MS;
  let n = 0;
  for (const item of items) {
    const t = parseReceivedAt(item?.receivedAt);
    if (Number.isFinite(t) && t >= cutoff) n += 1;
  }
  return n;
}

export function isRecent48h(iso, nowMs = Date.now()) {
  const t = parseReceivedAt(iso);
  if (!Number.isFinite(t)) return false;
  return nowMs - t <= FORTY_EIGHT_H_MS && nowMs - t >= 0;
}

function dash(value) {
  const s = String(value ?? "").trim();
  return s || "—";
}

function formatDateTime(iso) {
  const t = parseReceivedAt(iso);
  if (!Number.isFinite(t)) return dash(iso);
  try {
    return new Date(t).toISOString().replace("T", " ").replace(/\.\d{3}Z$/, " UTC");
  } catch {
    return dash(iso);
  }
}

function telHref(phone) {
  const raw = String(phone ?? "").trim();
  if (!raw) return "";
  const cleaned = raw.replace(/[^\d+]/g, "");
  return cleaned ? `tel:${cleaned}` : "";
}

function mailHref(email) {
  const raw = String(email ?? "").trim();
  if (!raw || !raw.includes("@")) return "";
  // Percent-encode @ so Cloudflare Email Obfuscation does not rewrite the href.
  return `mailto:${raw.replace(/@/g, "%40")}`;
}

function mailDisplay(email) {
  const raw = String(email ?? "").trim();
  if (!raw) return escapeHtml("—");
  // Visible text without a raw "@" slows scrape-shield rewriting.
  return escapeHtml(raw).replace(/@/g, "&#64;");
}

function summarizeFull(key, record) {
  const fields = record?.fields || {};
  const person = [fields.first_name, fields.last_name].filter(Boolean).join(" ");
  return {
    key,
    receivedAt: record?.receivedAt || "",
    requestId: record?.requestId || "",
    company: fields.company || "",
    contact: person,
    email: fields.email || "",
    phone: fields.phone || "",
    location: fields.location || "",
    industry: fields.industry || "",
    employees: fields.employees || "",
    workstations: fields.workstations || "",
    m365: fields.m365 || "",
    internal_it: fields.internal_it || "",
    external_it: fields.external_it || "",
    area: fields.area || "",
    start: fields.start || "",
    description: String(fields.description ?? "").trim(),
    language: fields.language || record?.language || "",
    email_notification_status: record?.email_notification_status || "",
    missing: false,
    parseError: false,
    error: "",
  };
}

function emptyItem(key, extra = {}) {
  return {
    key,
    receivedAt: "",
    requestId: "",
    company: "",
    contact: "",
    email: "",
    phone: "",
    location: "",
    industry: "",
    employees: "",
    workstations: "",
    m365: "",
    internal_it: "",
    external_it: "",
    area: "",
    start: "",
    description: "",
    language: "",
    email_notification_status: "",
    missing: false,
    parseError: false,
    error: "",
    ...extra,
  };
}

function htmlResponse(status, body) {
  return new Response(body, {
    status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store, no-cache, must-revalidate",
      pragma: "no-cache",
      "x-content-type-options": "nosniff",
      "referrer-policy": "no-referrer",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}

function renderError(status, title, message) {
  return htmlResponse(
    status,
    `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${escapeHtml(title)}</title>
<style>
body{margin:0;padding:1.25rem;font-family:system-ui,Segoe UI,sans-serif;line-height:1.45;color:#1a1a1a;background:#f4f5f3}
main{max-width:36rem;margin:0 auto}
h1{font-size:1.2rem;margin:0 0 .5rem}
p{margin:0;color:#444;overflow-wrap:anywhere}
</style>
</head>
<body><main>
<h1>${escapeHtml(title)}</h1>
<p>${escapeHtml(message)}</p>
</main></body></html>`,
  );
}

function row(label, valueHtml) {
  return `<div class="row"><dt>${escapeHtml(label)}</dt><dd>${valueHtml}</dd></div>`;
}

function plainRow(label, value) {
  return row(label, escapeHtml(dash(value)));
}

function renderViewer(items, last7, newestIso, limit, nowMs) {
  const newestLabel = newestIso
    ? escapeHtml(formatDateTime(newestIso))
    : "—";
  const articles = items
    .map((item) => {
      const recent = isRecent48h(item.receivedAt, nowMs);
      const cls = recent ? ' class="inquiry recent"' : ' class="inquiry"';
      const email = String(item.email || "").trim();
      const phone = String(item.phone || "").trim();
      const mHref = mailHref(email);
      const tHref = telHref(phone);
      const emailHtml = mHref
        ? `<a href="${escapeHtml(mHref)}">${mailDisplay(email)}</a>`
        : mailDisplay(email);      const phoneHtml = tHref
        ? `<a href="${escapeHtml(tHref)}">${escapeHtml(phone)}</a>`
        : escapeHtml(dash(phone));
      const desc = escapeHtml(dash(item.description)).replace(/\n/g, "<br>");
      const flags = [
        recent ? "weniger als 48 Stunden" : null,
        item.missing ? "fehlend" : null,
        item.parseError ? "Parse-Fehler" : null,
        item.error ? String(item.error) : null,
      ]
        .filter(Boolean)
        .map((f) => escapeHtml(f));
      const flagHtml = flags.length
        ? `<p class="flags">${flags.join(" · ")}</p>`
        : "";
      return `<article${cls}>
  <h2>${escapeHtml(formatDateTime(item.receivedAt))}</h2>
  <dl>
    ${plainRow("Unternehmen", item.company)}
    ${plainRow("Ansprechpartner", item.contact)}
    ${row("Geschäftliche E-Mail", emailHtml)}
    ${row("Telefon", phoneHtml)}
    ${plainRow("Standort / Kanton", item.location)}
    ${plainRow("Branche", item.industry)}
    ${plainRow("Mitarbeitende", item.employees)}
    ${plainRow("Arbeitsplätze", item.workstations)}
    ${plainRow("Microsoft 365", item.m365)}
    ${plainRow("Interne IT", item.internal_it)}
    ${plainRow("Externe IT", item.external_it)}
    ${plainRow("Bereich", item.area)}
    ${plainRow("Startzeitpunkt", item.start)}
    ${plainRow("Sprachversion", item.language)}
    ${plainRow("E-Mail-Benachrichtigung", item.email_notification_status)}
  </dl>
  <p class="desc"><strong>Beschreibung</strong><br>${desc}</p>
  ${flagHtml}
</article>`;
    })
    .join("\n");

  const empty =
    items.length === 0
      ? '<p class="empty">Keine Anfragen in diesem Ausschnitt.</p>'
      : "";

  return htmlResponse(
    200,
    `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>BIT Anfragen</title>
<style>
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;padding:1rem 1rem 3rem;font-family:system-ui,Segoe UI,sans-serif;line-height:1.45;color:#1a1a1a;background:linear-gradient(180deg,#e8eeea 0%,#f4f5f3 10rem);overflow-x:hidden}
header,main{max-width:40rem;margin:0 auto;width:100%}
h1{font-size:1.35rem;margin:0 0 .4rem;letter-spacing:-.02em}
.meta{margin:.15rem 0;color:#334;font-size:.95rem;overflow-wrap:anywhere}
.hint{margin:.55rem 0 0;color:#666;font-size:.8rem}
main{display:flex;flex-direction:column;gap:.9rem;margin-top:1.1rem}
.inquiry{background:#fff;border:1px solid #cfd6d1;border-radius:8px;padding:.9rem 1rem;overflow-wrap:anywhere}
.inquiry.recent{border-color:#2f6f4e;box-shadow:inset 4px 0 0 #2f6f4e;background:#f3faf6}
.inquiry h2{font-size:1rem;margin:0 0 .7rem}
dl{margin:0;display:flex;flex-direction:column;gap:.35rem}
.row{display:grid;grid-template-columns:minmax(7.5rem,9.5rem) 1fr;gap:.2rem .65rem}
dt{color:#555;font-size:.82rem}
dd{margin:0;overflow-wrap:anywhere;word-break:break-word}
a{color:#1a4d36;overflow-wrap:anywhere}
.desc{margin:.8rem 0 0}
.flags{margin:.5rem 0 0;color:#1a4d36;font-size:.82rem;font-weight:600}
.empty{margin:0;color:#555}
@media (max-width:520px){
  body{padding:.85rem .75rem 2.5rem}
  .row{grid-template-columns:1fr}
  dt{margin-top:.2rem}
}
</style>
</head>
<body>
<!--email_off-->
<header>
  <h1>BIT Anfragen</h1>
  <p class="meta"><strong>Einträge der letzten 7 Tage: ${escapeHtml(String(last7))}</strong></p>
  <p class="meta">Neueste Anfrage: <strong>${newestLabel}</strong></p>
  <p class="hint">Neueste zuerst · max. ${escapeHtml(String(limit))} · Einträge unter 48&nbsp;h hervorgehoben · Nur mit gültigem Token</p>
</header>
<main>
${empty}${articles}
</main>
<!--/email_off-->
</body>
</html>`,
  );
}

async function loadItems(env, limit) {
  const fetchLimit = Math.min(Math.max(limit, LIST_FETCH), 1000);
  let listed;
  try {
    listed = await env.INQUIRY_LOG.list({ prefix: KEY_PREFIX, limit: fetchLimit });
  } catch (err) {
    console.error("INQUIRIES_VIEW_LIST_FAILED", String(err));
    return { error: "list_failed" };
  }

  const items = [];
  for (const entry of listed?.keys || []) {
    const key = entry.name;
    try {
      const raw = await env.INQUIRY_LOG.get(key);
      if (!raw) {
        items.push(emptyItem(key, { missing: true }));
        continue;
      }
      let record;
      try {
        record = JSON.parse(raw);
      } catch {
        items.push(emptyItem(key, { parseError: true }));
        continue;
      }
      items.push(summarizeFull(key, record));
    } catch (err) {
      console.error("INQUIRIES_VIEW_GET_FAILED", key, String(err));
      items.push(emptyItem(key, { error: "read_failed" }));
    }
  }

  items.sort((a, b) => {
    const ta = parseReceivedAt(a.receivedAt);
    const tb = parseReceivedAt(b.receivedAt);
    return (Number.isFinite(tb) ? tb : 0) - (Number.isFinite(ta) ? ta : 0);
  });

  const last7 = countLast7Days(items);
  const newestIso = items.find((i) => i.receivedAt)?.receivedAt || "";
  return {
    items: items.slice(0, limit),
    last7,
    newestIso,
  };
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const required = viewToken(env);

  if (!required) {
    return renderError(
      503,
      "Viewer nicht konfiguriert",
      "INQUIRY_VIEW_TOKEN (or INQUIRY_DIAG_TOKEN) is not set in Production.",
    );
  }

  const provided =
    extractBearer(request) || String(url.searchParams.get("token") || "").trim();
  if (!provided || provided !== required) {
    return renderError(401, "Nicht autorisiert", "Ungültiges oder fehlendes Token.");
  }

  if (!env.INQUIRY_LOG) {
    return renderError(503, "KV fehlt", "INQUIRY_LOG KV binding missing.");
  }

  const limit = parseLimit(url.searchParams.get("limit"));
  const loaded = await loadItems(env, limit);
  if (loaded.error === "list_failed") {
    return renderError(502, "Liste fehlgeschlagen", "KV-Liste konnte nicht gelesen werden.");
  }

  return renderViewer(
    loaded.items,
    loaded.last7,
    loaded.newestIso,
    limit,
    Date.now(),
  );
}

export async function onRequest(context) {
  if (context.request.method === "GET") {
    return onRequestGet(context);
  }
  if (context.request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        Allow: "GET, OPTIONS",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "authorization, content-type",
        "cache-control": "no-store",
      },
    });
  }
  return renderError(405, "Methode nicht erlaubt", "Nur GET ist erlaubt.");
}
