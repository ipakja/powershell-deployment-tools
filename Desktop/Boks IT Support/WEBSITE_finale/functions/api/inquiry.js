/**
 * Inquiry form API – KV store (durable) + optional Resend email + push notify.
 *
 * Visitor success requires KV write when INQUIRY_LOG is bound.
 * Email/notify failures keep the KV record and still return 200.
 *
 * Notify options (any):
 *   - RESEND_API_KEY (preferred email)
 *   - TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
 *   - INQUIRY_WEBHOOK_URL (Slack/Discord/generic)
 */
const MAX_BODY = 32_000;
const HONEYPOT = "website";
/** ~12 months; aligns with privacy retention wording. */
const KV_TTL_SECONDS = 60 * 60 * 24 * 365;
const WEBHOOK_TIMEOUT_MS = 8_000;
const DEFAULT_NOTIFY_EMAIL = "admin@boksitsupport.ch";
const DEFAULT_FROM = "BIT Anfrage <anfrage@boksitsupport.ch>";
const RATE_LIMIT_WINDOW_SECONDS = 3600;
const RATE_LIMIT_MAX = 8;

const REQUIRED = [
  "company",
  "first_name",
  "last_name",
  "email",
  "employees",
  "area",
  "description",
];

const OPTIONAL = [
  "phone",
  "location",
  "industry",
  "workstations",
  "m365",
  "internal_it",
  "external_it",
  "start",
];

/** Meta fields accepted from the client (not form inputs). */
const META = ["language", "timestamp", "source_page", "privacy"];

const ALLOWED_KEYS = new Set([...REQUIRED, ...OPTIONAL, ...META, HONEYPOT]);

const FIELD_MAX = {
  company: 200,
  first_name: 100,
  last_name: 100,
  email: 200,
  employees: 40,
  area: 80,
  description: 4000,
  phone: 40,
  location: 120,
  industry: 120,
  workstations: 40,
  m365: 40,
  internal_it: 40,
  external_it: 40,
  start: 80,
  language: 8,
  timestamp: 40,
  source_page: 200,
};

const REJECT_KEY_RE =
  /password|passwd|secret|token|mfa|otp|cookie|authorization|api[_-]?key|credit|ssn|iban/i;

function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function sanitize(value, max = 4000) {
  return String(value ?? "")
    .replace(/\r/g, "")
    .trim()
    .slice(0, max);
}

/** Escape text for safe HTML email bodies. */
export function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 200;
}

function notifyEmail(env) {
  const raw = String(
    env?.INQUIRY_NOTIFY_EMAIL || env?.INQUIRY_TO || DEFAULT_NOTIFY_EMAIL,
  ).trim();
  return isEmail(raw) ? raw : DEFAULT_NOTIFY_EMAIL;
}

function fromAddress(env) {
  const raw = String(
    env?.INQUIRY_FROM_EMAIL || env?.INQUIRY_FROM || DEFAULT_FROM,
  ).trim();
  return raw || DEFAULT_FROM;
}

function isAllowedContentType(request) {
  const ct = (request.headers.get("content-type") || "").toLowerCase();
  return ct.includes("application/json");
}

function hasRejectedKeys(data) {
  if (!data || typeof data !== "object" || Array.isArray(data)) return true;
  for (const key of Object.keys(data)) {
    if (REJECT_KEY_RE.test(key)) return true;
    if (!ALLOWED_KEYS.has(key)) return true;
  }
  return false;
}

function buildTextBody(requestId, receivedAt, fields, source) {
  const person = [fields.first_name, fields.last_name].filter(Boolean).join(" ");
  return [
    "Neue BIT-Anfrage",
    "",
    `Unternehmen: ${fields.company || "—"}`,
    `Ansprechpartner: ${person || "—"}`,
    `E-Mail: ${fields.email || "—"}`,
    `Telefon: ${fields.phone || "—"}`,
    `Standort: ${fields.location || "—"}`,
    `Branche: ${fields.industry || "—"}`,
    `Mitarbeitende: ${fields.employees || "—"}`,
    `Arbeitsplätze: ${fields.workstations || "—"}`,
    `Microsoft 365: ${fields.m365 || "—"}`,
    `Interne IT: ${fields.internal_it || "—"}`,
    `Externe IT: ${fields.external_it || "—"}`,
    `Leistungsbereich: ${fields.area || "—"}`,
    `Startzeitpunkt: ${fields.start || "—"}`,
    `Sprache: ${fields.language || "—"}`,
    "",
    "Kurzbeschreibung:",
    fields.description || "—",
    "",
    `Request-ID: ${requestId}`,
    `Empfangen: ${receivedAt}`,
    `Quelle: ${source || "—"}`,
  ].join("\n");
}

function buildHtmlBody(requestId, receivedAt, fields, source) {
  const person = [fields.first_name, fields.last_name].filter(Boolean).join(" ");
  const rows = [
    ["Unternehmen", fields.company],
    ["Ansprechpartner", person],
    ["E-Mail", fields.email],
    ["Telefon", fields.phone || "—"],
    ["Standort", fields.location || "—"],
    ["Branche", fields.industry || "—"],
    ["Mitarbeitende", fields.employees],
    ["Arbeitsplätze", fields.workstations || "—"],
    ["Microsoft 365", fields.m365 || "—"],
    ["Interne IT", fields.internal_it || "—"],
    ["Externe IT", fields.external_it || "—"],
    ["Leistungsbereich", fields.area],
    ["Startzeitpunkt", fields.start || "—"],
    ["Sprache", fields.language || "—"],
  ]
    .map(
      ([label, value]) =>
        `<tr><td style="padding:4px 12px 4px 0;color:#555;vertical-align:top">${escapeHtml(label)}</td><td style="padding:4px 0;vertical-align:top">${escapeHtml(value || "—")}</td></tr>`,
    )
    .join("");
  return `<!DOCTYPE html><html><body style="font-family:system-ui,sans-serif;line-height:1.45;color:#1a1a1a">
<h1 style="font-size:1.15rem">Neue BIT-Anfrage</h1>
<table style="border-collapse:collapse">${rows}</table>
<p style="margin-top:1rem"><strong>Kurzbeschreibung</strong><br>${escapeHtml(fields.description || "—").replace(/\n/g, "<br>")}</p>
<p style="margin-top:1rem;color:#555;font-size:0.9rem">Request-ID: ${escapeHtml(requestId)}<br>Empfangen: ${escapeHtml(receivedAt)}<br>Quelle: ${escapeHtml(source || "—")}</p>
</body></html>`;
}

/** Compact human notification for Telegram/Slack/Discord. */
export function buildNotifyText(record) {
  const f = record.fields || {};
  const person = [f.first_name, f.last_name].filter(Boolean).join(" ");
  return [
    "Neue BIT-Anfrage",
    `Zeit: ${record.receivedAt || ""}`,
    `Unternehmen: ${f.company || "—"}`,
    `Ansprechpartner: ${person || "—"}`,
    `E-Mail: ${f.email || "—"}`,
    f.phone ? `Telefon: ${f.phone}` : null,
    `Bereich: ${f.area || "—"}`,
    f.start ? `Startzeitpunkt: ${f.start}` : null,
    f.employees ? `Mitarbeitende: ${f.employees}` : null,
    "",
    "Kurzbeschreibung:",
    f.description || "—",
    "",
    `ID: ${record.requestId || ""}`,
    record.email_notification_status
      ? `E-Mail-Status: ${record.email_notification_status}`
      : null,
  ]
    .filter((line) => line !== null)
    .join("\n");
}

export function hasDurableDelivery(env) {
  return Boolean(
    env?.INQUIRY_LOG ||
      env?.INQUIRY_WEBHOOK_URL ||
      env?.RESEND_API_KEY ||
      (env?.TELEGRAM_BOT_TOKEN && env?.TELEGRAM_CHAT_ID),
  );
}

export function hasPushNotify(env) {
  return Boolean(
    String(env?.INQUIRY_WEBHOOK_URL || "").trim() ||
      (String(env?.TELEGRAM_BOT_TOKEN || "").trim() &&
        String(env?.TELEGRAM_CHAT_ID || "").trim()) ||
      env?.RESEND_API_KEY,
  );
}

async function enforceRateLimit(env, ip, requestId) {
  if (!env?.INQUIRY_LOG || !ip) {
    return { ok: true, skipped: true };
  }
  const key = `ratelimit:${ip}`;
  try {
    const raw = await env.INQUIRY_LOG.get(key);
    const count = raw ? Number.parseInt(raw, 10) || 0 : 0;
    if (count >= RATE_LIMIT_MAX) {
      console.warn("INQUIRY_RATE_LIMITED", requestId, ip);
      return { ok: false };
    }
    await env.INQUIRY_LOG.put(key, String(count + 1), {
      expirationTtl: RATE_LIMIT_WINDOW_SECONDS,
    });
    return { ok: true };
  } catch (err) {
    console.error("INQUIRY_RATE_LIMIT_ERROR", requestId, String(err));
    return { ok: true, skipped: true };
  }
}

async function storeInKv(env, record) {
  if (!env.INQUIRY_LOG) {
    return { ok: false, reason: "not_bound" };
  }
  const key = `inquiry:${record.receivedAt}:${record.requestId}`;
  try {
    await env.INQUIRY_LOG.put(key, JSON.stringify(record), {
      expirationTtl: KV_TTL_SECONDS,
    });
    console.log("INQUIRY_KV_STORED", record.requestId, key);
    return { ok: true, via: "kv", key };
  } catch (err) {
    console.error("INQUIRY_KV_FAILED", record.requestId, String(err));
    return { ok: false, reason: "write_failed" };
  }
}

async function updateKvEmailStatus(env, key, record, status) {
  if (!env.INQUIRY_LOG || !key) return;
  record.email_notification_status = status;
  try {
    await env.INQUIRY_LOG.put(key, JSON.stringify(record), {
      expirationTtl: KV_TTL_SECONDS,
    });
    console.log("INQUIRY_KV_EMAIL_STATUS", record.requestId, status);
  } catch (err) {
    console.error("INQUIRY_KV_STATUS_UPDATE_FAILED", record.requestId, String(err));
  }
}

async function postJson(url, body, requestId, label) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), WEBHOOK_TIMEOUT_MS);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json; charset=utf-8" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const detail = await response.text().catch(() => "");
    console.log(
      label,
      requestId,
      "status=",
      response.status,
      "body=",
      detail.slice(0, 800),
    );
    if (response.status >= 200 && response.status < 300) {
      return { ok: true };
    }
    console.error(label + "_FAILED", requestId, response.status, detail.slice(0, 800));
    return { ok: false, reason: "http_error", status: response.status };
  } catch (err) {
    console.error(label + "_NETWORK", requestId, String(err));
    return { ok: false, reason: "network" };
  } finally {
    clearTimeout(timer);
  }
}

/** Telegram Bot API sendMessage. */
export async function deliverViaTelegram(env, record) {
  const token = String(env.TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = String(env.TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId) {
    return { ok: false, reason: "not_configured" };
  }
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const result = await postJson(
    url,
    {
      chat_id: chatId,
      text: buildNotifyText(record),
      disable_web_page_preview: true,
    },
    record.requestId,
    "INQUIRY_TELEGRAM_HTTP",
  );
  return result.ok
    ? { ok: true, via: "telegram" }
    : { ok: false, reason: result.reason || "telegram_failed", status: result.status };
}

/**
 * Slack Incoming Webhook, Discord webhook, Telegram sendMessage URL, or generic JSON.
 */
export async function deliverViaWebhook(env, record) {
  const url = String(env.INQUIRY_WEBHOOK_URL || "").trim();
  if (!url) {
    return { ok: false, reason: "not_configured" };
  }

  const text = buildNotifyText(record);
  let body;

  if (url.includes("api.telegram.org") && url.includes("sendMessage")) {
    const chatId = String(env.TELEGRAM_CHAT_ID || "").trim();
    body = {
      chat_id: chatId || undefined,
      text,
      disable_web_page_preview: true,
    };
  } else if (url.includes("hooks.slack.com") || url.includes("slack.com/services")) {
    body = { text };
  } else if (url.includes("discord.com/api/webhooks")) {
    body = { content: text.slice(0, 1900) };
  } else {
    body = {
      text,
      content: text,
      summary: text,
      inquiry: record,
    };
  }

  const result = await postJson(url, body, record.requestId, "INQUIRY_WEBHOOK_HTTP");
  return result.ok
    ? { ok: true, via: "webhook" }
    : { ok: false, reason: result.reason || "webhook_failed", status: result.status };
}

/** Run configured push channels; does not touch KV. */
export async function deliverPushNotify(env, record) {
  const telegramResult = await deliverViaTelegram(env, record);
  const webhookResult = await deliverViaWebhook(env, record);
  const notifyVias = [];
  if (telegramResult.ok) notifyVias.push("telegram");
  if (webhookResult.ok) notifyVias.push("webhook");
  if (!telegramResult.ok && telegramResult.reason !== "not_configured") {
    console.error("INQUIRY_NOTIFY_TELEGRAM_FAILED", record.requestId, telegramResult);
  }
  if (!webhookResult.ok && webhookResult.reason !== "not_configured") {
    console.error("INQUIRY_NOTIFY_WEBHOOK_FAILED", record.requestId, webhookResult);
  }
  return {
    ok: notifyVias.length > 0,
    notifyVias,
    telegram: telegramResult,
    webhook: webhookResult,
  };
}

async function deliverViaResend(env, requestId, receivedAt, fields, source) {
  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    return { ok: false, reason: "not_configured" };
  }

  const to = notifyEmail(env);
  const from = fromAddress(env);
  const mirror = env.INQUIRY_MIRROR_TO || "";
  const subject = `Neue BIT-Anfrage – ${fields.company} – ${fields.area}`;

  const emailBody = {
    from,
    to: [to],
    subject,
    text: buildTextBody(requestId, receivedAt, fields, source),
    html: buildHtmlBody(requestId, receivedAt, fields, source),
    reply_to: fields.email,
  };
  if (mirror) {
    emailBody.bcc = [mirror];
  }

  let resendResponse;
  try {
    resendResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "content-type": "application/json",
      },
      body: JSON.stringify(emailBody),
    });
  } catch (err) {
    console.error("INQUIRY_RESEND_NETWORK", requestId, String(err));
    return { ok: false, error: "delivery_network" };
  }

  const detail = await resendResponse.text();
  console.log(
    "INQUIRY_RESEND_HTTP",
    requestId,
    "status=",
    resendResponse.status,
    "body=",
    detail.slice(0, 2000),
    "from=",
    from,
    "to=",
    to,
  );

  if (!resendResponse.ok) {
    console.error(
      "INQUIRY_RESEND_FAILED",
      requestId,
      resendResponse.status,
      detail.slice(0, 2000),
    );
    return {
      ok: false,
      error: "delivery_failed",
      resendStatus: resendResponse.status,
    };
  }

  let resendJson = {};
  try {
    resendJson = JSON.parse(detail);
  } catch {
    resendJson = {};
  }
  console.log("INQUIRY_DELIVERED_RESEND", requestId, resendJson.id || "");
  return { ok: true, via: "resend" };
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const receivedAt = new Date().toISOString();
  const requestId = crypto.randomUUID();

  if (!isAllowedContentType(request)) {
    return json(400, { ok: false, error: "invalid_content_type" });
  }

  let raw;
  try {
    raw = await request.text();
  } catch {
    return json(400, { ok: false, error: "body_unreadable" });
  }
  if (raw.length > MAX_BODY) {
    return json(413, { ok: false, error: "body_too_large" });
  }

  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    return json(400, { ok: false, error: "invalid_json" });
  }

  if (hasRejectedKeys(data)) {
    return json(400, { ok: false, error: "unexpected_fields" });
  }

  if (sanitize(data[HONEYPOT], 200)) {
    return json(200, { ok: true, requestId, notified: false, emailQueued: false });
  }

  const ip = request.headers.get("cf-connecting-ip") || "";
  const rate = await enforceRateLimit(env, ip, requestId);
  if (!rate.ok) {
    return json(429, { ok: false, error: "rate_limited" });
  }

  const fields = {};
  for (const key of REQUIRED) {
    fields[key] = sanitize(data[key], FIELD_MAX[key] || 4000);
    if (!fields[key]) {
      return json(400, { ok: false, error: "missing_field", field: key });
    }
  }
  for (const key of OPTIONAL) {
    fields[key] = sanitize(data[key], FIELD_MAX[key] || 4000);
  }
  fields.privacy = Boolean(data.privacy);
  const langRaw = sanitize(data.language || "", FIELD_MAX.language).toLowerCase();
  fields.language = langRaw === "en" || langRaw === "de" ? langRaw : "";

  if (!fields.privacy) {
    return json(400, { ok: false, error: "privacy_required" });
  }
  if (!isEmail(fields.email)) {
    return json(400, { ok: false, error: "invalid_email" });
  }

  const defaultSource =
    fields.language === "en"
      ? "boksitsupport.ch/en/inquiry/"
      : "boksitsupport.ch/de/anfrage/";
  const clientSource = sanitize(data.source_page || "", FIELD_MAX.source_page);
  const sourcePath =
    clientSource.startsWith("boksitsupport.ch/") ||
    clientSource.startsWith("https://boksitsupport.ch/")
      ? clientSource.replace(/^https?:\/\//, "")
      : defaultSource;

  const clientTs = sanitize(data.timestamp || "", FIELD_MAX.timestamp);
  const clientTimestamp =
    clientTs && Number.isFinite(Date.parse(clientTs)) ? clientTs : receivedAt;

  const emailConfigured = Boolean(env.RESEND_API_KEY);
  const initialEmailStatus = emailConfigured ? "pending" : "skipped";

  const record = {
    requestId,
    receivedAt,
    clientTimestamp,
    source: sourcePath,
    source_page: sourcePath,
    language: fields.language || "",
    ip,
    country: request.cf?.country || "",
    email_notification_status: initialEmailStatus,
    fields,
  };

  console.log(
    "INQUIRY_SUBMISSION",
    JSON.stringify({
      requestId,
      receivedAt,
      source: sourcePath,
      language: fields.language,
      company: fields.company,
      area: fields.area,
      email_notification_status: initialEmailStatus,
    }),
  );

  if (!hasDurableDelivery(env)) {
    console.log("INQUIRY_NO_DURABLE_PATH", requestId);
    return json(503, {
      ok: false,
      error: "delivery_not_configured",
      message: "Keine Zustellung konfiguriert (KV, Webhook/Telegram oder Resend).",
      requestId,
      logged: true,
      notified: false,
      emailQueued: false,
    });
  }

  // 1) KV first – when KV is bound, visitor success requires a successful write.
  const kvBound = Boolean(env.INQUIRY_LOG);
  const kvResult = await storeInKv(env, record);

  if (kvBound && !kvResult.ok) {
    console.error("INQUIRY_STORAGE_FAILED", requestId, kvResult.reason || "");
    return json(500, {
      ok: false,
      error: "storage_failed",
      requestId,
      logged: true,
      stored: false,
      notified: false,
      emailQueued: false,
    });
  }

  // 2) Resend email after KV; failure keeps KV and still returns success.
  let resendResult = { ok: false, reason: "not_configured" };
  if (emailConfigured) {
    resendResult = await deliverViaResend(
      env,
      requestId,
      receivedAt,
      fields,
      sourcePath,
    );
    const emailStatus = resendResult.ok ? "sent" : "failed";
    await updateKvEmailStatus(env, kvResult.key, record, emailStatus);
    if (!resendResult.ok) {
      console.error("INQUIRY_NOTIFY_RESEND_FAILED", requestId, resendResult);
    }
  }

  // 3) Optional push notify (Telegram/Webhook). Failures must not wipe KV success.
  const telegramResult = await deliverViaTelegram(env, record);
  const webhookResult = await deliverViaWebhook(env, record);
  const notifyVias = [];
  if (telegramResult.ok) notifyVias.push("telegram");
  if (webhookResult.ok) notifyVias.push("webhook");
  if (resendResult.ok) notifyVias.push("resend");

  if (!telegramResult.ok && telegramResult.reason !== "not_configured") {
    console.error("INQUIRY_NOTIFY_TELEGRAM_FAILED", requestId, telegramResult);
  }
  if (!webhookResult.ok && webhookResult.reason !== "not_configured") {
    console.error("INQUIRY_NOTIFY_WEBHOOK_FAILED", requestId, webhookResult);
  }

  const durableOk =
    kvResult.ok || webhookResult.ok || telegramResult.ok || resendResult.ok;

  if (durableOk) {
    if (kvResult.ok && notifyVias.length === 0 && hasPushNotify(env)) {
      console.error("INQUIRY_STORED_BUT_NOTIFY_FAILED", requestId);
    } else if (kvResult.ok && !hasPushNotify(env)) {
      console.log("INQUIRY_STORED_NO_PUSH_CONFIGURED", requestId);
    }
    return json(200, {
      ok: true,
      requestId,
      via: kvResult.ok ? "kv" : notifyVias[0] || "ok",
      stored: Boolean(kvResult.ok),
      notified: notifyVias.length > 0,
      emailQueued: Boolean(resendResult.ok),
      email_notification_status: record.email_notification_status,
      notifyVias,
    });
  }

  console.error(
    "INQUIRY_ALL_PATHS_FAILED",
    requestId,
    "kv=",
    kvResult.reason || "",
    "telegram=",
    telegramResult.reason || "",
    "webhook=",
    webhookResult.reason || "",
    "resend=",
    resendResult.error || resendResult.reason || "",
  );
  return json(500, {
    ok: false,
    error: "delivery_failed",
    requestId,
    logged: true,
    notified: false,
    emailQueued: false,
  });
}

export async function onRequest(context) {
  if (context.request.method === "POST") {
    return onRequestPost(context);
  }
  if (context.request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        Allow: "POST, OPTIONS",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "content-type",
      },
    });
  }
  return json(405, { ok: false, error: "method_not_allowed" });
}
