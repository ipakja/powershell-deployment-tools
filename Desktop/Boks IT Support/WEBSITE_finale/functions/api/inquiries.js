/**
 * Protected list of recent inquiry KV records.
 * GET /api/inquiries?token=…&limit=20
 * Auth: Authorization Bearer OR ?token= matching INQUIRY_VIEW_TOKEN
 *       (fallback: INQUIRY_DIAG_TOKEN when VIEW is unset).
 */
const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 50;
const KEY_PREFIX = "inquiry:";
const PREVIEW_LEN = 160;

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
    area: fields.area || "",
    start: fields.start || "",
    employees: fields.employees || "",
    description: preview(fields.description),
    source: record?.source || "",
    country: record?.country || "",
  };
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const required = viewToken(env);

  if (!required) {
    return json(401, { ok: false, error: "unauthorized" });
  }

  const provided =
    extractBearer(request) || String(url.searchParams.get("token") || "").trim();
  if (provided !== required) {
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

  let listed;
  try {
    listed = await env.INQUIRY_LOG.list({ prefix: KEY_PREFIX, limit });
  } catch (err) {
    console.error("INQUIRIES_LIST_FAILED", String(err));
    return json(502, { ok: false, error: "list_failed" });
  }

  const keys = listed?.keys || [];
  const items = [];

  for (const entry of keys) {
    const key = entry.name;
    try {
      const raw = await env.INQUIRY_LOG.get(key);
      if (!raw) {
        items.push({
          key,
          receivedAt: "",
          requestId: "",
          company: "",
          contact: "",
          email: "",
          area: "",
          start: "",
          description: "",
          missing: true,
        });
        continue;
      }
      let record;
      try {
        record = JSON.parse(raw);
      } catch {
        items.push({
          key,
          receivedAt: "",
          requestId: "",
          company: "",
          contact: "",
          email: "",
          area: "",
          start: "",
          description: "",
          parseError: true,
        });
        continue;
      }
      items.push(summarize(key, record));
    } catch (err) {
      console.error("INQUIRIES_GET_FAILED", key, String(err));
      items.push({
        key,
        receivedAt: "",
        requestId: "",
        company: "",
        contact: "",
        email: "",
        area: "",
        start: "",
        description: "",
        error: "read_failed",
      });
    }
  }

  return json(200, {
    ok: true,
    count: items.length,
    items,
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
