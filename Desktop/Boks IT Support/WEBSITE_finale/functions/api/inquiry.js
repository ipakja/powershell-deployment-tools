/**
 * Inquiry form API – KV store (durable) + push notify (webhook/Telegram) + optional Resend.
 *
 * Success for the visitor: KV write succeeds (or webhook/Resend if KV missing).
 * Notification is attempted after KV; webhook failure is logged and does NOT fail the user.
 *
 * Notify options (any):
 *   - TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
 *   - INQUIRY_WEBHOOK_URL (Slack Incoming Webhook, Discord, or generic JSON)
 *   - RESEND_API_KEY (email, optional)
 */
const MAX_BODY = 32_000;
const HONEYPOT = "website";
/** ~12 months; aligns with privacy retention wording. */
const KV_TTL_SECONDS = 60 * 60 * 24 * 365;
const WEBHOOK_TIMEOUT_MS = 8_000;
const DEFAULT_NOTIFY_EMAIL = "admin@boksitsupport.ch";

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

function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function sanitize(value) {
  return String(value ?? "")
    .replace(/\r/g, "")
    .trim()
    .slice(0, 4000);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 200;
}

function notifyEmail(env) {
  const raw = String(env?.INQUIRY_NOTIFY_EMAIL || DEFAULT_NOTIFY_EMAIL).trim();
  return isEmail(raw) ? raw : DEFAULT_NOTIFY_EMAIL;
}

function buildTextBody(requestId, receivedAt, fields) {
  const lines = Object.entries(fields)
    .filter(([k]) => k !== "privacy")
    .map(([k, v]) => `${k}: ${v}`);
  return [`Request-ID: ${requestId}`, `Empfangen: ${receivedAt}`, "", ...lines].join(
    "\n",
  );
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
async function deliverViaTelegram(env, record) {
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
async function deliverViaWebhook(env, record) {
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

async function deliverViaResend(env, requestId, receivedAt, fields) {
  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    return { ok: false, reason: "not_configured" };
  }

  const to = env.INQUIRY_TO || notifyEmail(env);
  const from = env.INQUIRY_FROM || "BIT Anfrage <anfrage@boksitsupport.ch>";
  const mirror = env.INQUIRY_MIRROR_TO || "";

  const emailBody = {
    from,
    to: [to],
    subject: `BIT Anfrage: ${fields.company} · ${fields.area}`,
    text: buildTextBody(requestId, receivedAt, fields),
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

  if (sanitize(data[HONEYPOT])) {
    return json(200, { ok: true, requestId, notified: false });
  }

  const fields = {};
  for (const key of REQUIRED) {
    fields[key] = sanitize(data[key]);
    if (!fields[key]) {
      return json(400, { ok: false, error: "missing_field", field: key });
    }
  }
  for (const key of OPTIONAL) {
    fields[key] = sanitize(data[key]).slice(0, key === "phone" ? 40 : 4000);
  }
  fields.privacy = Boolean(data.privacy);

  if (!fields.privacy) {
    return json(400, { ok: false, error: "privacy_required" });
  }
  if (!isEmail(fields.email)) {
    return json(400, { ok: false, error: "invalid_email" });
  }

  const record = {
    requestId,
    receivedAt,
    source: "boksitsupport.ch/de/anfrage/",
    ip: request.headers.get("cf-connecting-ip") || "",
    country: request.cf?.country || "",
    fields,
  };

  console.log("INQUIRY_SUBMISSION", JSON.stringify(record));

  if (!hasDurableDelivery(env)) {
    console.log("INQUIRY_NO_DURABLE_PATH", requestId);
    return json(503, {
      ok: false,
      error: "delivery_not_configured",
      message: "Keine Zustellung konfiguriert (KV, Webhook/Telegram oder Resend).",
      requestId,
      logged: true,
      notified: false,
    });
  }

  // 1) Always try KV first – visitor success depends on durable store when KV is bound.
  const kvResult = await storeInKv(env, record);

  // 2) Push notify – failures must not wipe KV success.
  const telegramResult = await deliverViaTelegram(env, record);
  const webhookResult = await deliverViaWebhook(env, record);
  const resendResult = env.RESEND_API_KEY
    ? await deliverViaResend(env, requestId, receivedAt, fields)
    : { ok: false, reason: "not_configured" };

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
  if (!resendResult.ok && resendResult.reason !== "not_configured") {
    console.error("INQUIRY_NOTIFY_RESEND_FAILED", requestId, resendResult);
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
  return json(502, {
    ok: false,
    error: "delivery_failed",
    requestId,
    logged: true,
    notified: false,
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
