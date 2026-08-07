/**
 * Protected JSON list of recent inquiry KV records.
 * GET /api/inquiries?token=…&limit=20
 * Auth: Authorization Bearer OR ?token= matching INQUIRY_VIEW_TOKEN
 *       (fallback: INQUIRY_DIAG_TOKEN when VIEW is unset).
 * If neither secret is configured → 503 (never open access).
 * Wrong/missing token when secrets exist → 401.
 * HTML viewer: GET /api/inquiries/view (see inquiries/view.js).
 */
const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 50;
const LIST_FETCH = 200;
const KEY_PREFIX = "inquiry:";
const PREVIEW_LEN = 160;
const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;

function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

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

function preview(text) {
  const s = String(text ?? "").replace(/\s+/g, " ").trim();
  if (s.length <= PREVIEW_LEN) return s;
  return s.slice(0, PREVIEW_LEN - 1) + "…";
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

function summarize(key, record) {
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
    description: preview(fields.description),
    language: fields.language || record?.language || "",
    source: record?.source || record?.source_page || "",
    country: record?.country || "",
    email_notification_status: record?.email_notification_status || "",
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
    area: "",
    start: "",
    description: "",
    language: "",
    source: "",
    country: "",
    email_notification_status: "",
    ...extra,
  };
}

async function loadItems(env, limit) {
  const fetchLimit = Math.min(Math.max(limit, LIST_FETCH), 1000);
  let listed;
  try {
    listed = await env.INQUIRY_LOG.list({ prefix: KEY_PREFIX, limit: fetchLimit });
  } catch (err) {
    console.error("INQUIRIES_LIST_FAILED", String(err));
    return { error: "list_failed" };
  }

  const keys = listed?.keys || [];
  const items = [];

  for (const entry of keys) {
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
      items.push(summarize(key, record));
    } catch (err) {
      console.error("INQUIRIES_GET_FAILED", key, String(err));
      items.push(emptyItem(key, { error: "read_failed" }));
    }
  }

  items.sort((a, b) => {
    const ta = parseReceivedAt(a.receivedAt);
    const tb = parseReceivedAt(b.receivedAt);
    const na = Number.isFinite(ta) ? ta : 0;
    const nb = Number.isFinite(tb) ? tb : 0;
    return nb - na;
  });

  const last7 = countLast7Days(items);
  return { items: items.slice(0, limit), last7 };
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const required = viewToken(env);

  if (!required) {
    return json(503, {
      ok: false,
      error: "auth_not_configured",
      message:
        "INQUIRY_VIEW_TOKEN (or INQUIRY_DIAG_TOKEN) is not set in Production.",
    });
  }

  const provided =
    extractBearer(request) || String(url.searchParams.get("token") || "").trim();
  if (!provided || provided !== required) {
    return json(401, { ok: false, error: "unauthorized" });
  }

  if (!env.INQUIRY_LOG) {
    return json(503, {
      ok: false,
      error: "kv_not_bound",
      message: "INQUIRY_LOG KV binding missing.",
    });
  }

  const limit = parseLimit(url.searchParams.get("limit"));
  const loaded = await loadItems(env, limit);
  if (loaded.error === "list_failed") {
    return json(502, { ok: false, error: "list_failed" });
  }

  return json(200, {
    ok: true,
    count: loaded.items.length,
    last7Days: loaded.last7,
    items: loaded.items,
  });
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
  return json(405, { ok: false, error: "method_not_allowed" });
}
