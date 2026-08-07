/**
 * Protected notify test — sends Telegram/webhook without writing KV.
 *
 * POST /api/inquiry-notify-test
 * Auth: Authorization: Bearer <token> OR ?token= / JSON body.token
 * Token: INQUIRY_VIEW_TOKEN, else INQUIRY_DIAG_TOKEN
 * If neither secret is configured → 503 (never unauthenticated Telegram send).
 * Wrong/missing token when secrets exist → 401.
 *
 * Does NOT call INQUIRY_LOG.put.
 */
import { deliverPushNotify, hasPushNotify } from "./inquiry.js";

function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function authToken(env) {
  const view = String(env?.INQUIRY_VIEW_TOKEN || "").trim();
  if (view) return view;
  return String(env?.INQUIRY_DIAG_TOKEN || "").trim();
}

function extractBearer(request) {
  const header = request.headers.get("authorization") || "";
  const match = /^Bearer\s+(.+)$/i.exec(header.trim());
  return match ? match[1].trim() : "";
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const required = authToken(env);
  if (!required) {
    return json(503, {
      ok: false,
      error: "auth_not_configured",
      message:
        "INQUIRY_VIEW_TOKEN (or INQUIRY_DIAG_TOKEN) is not set in Production.",
      stored: false,
    });
  }

  const url = new URL(request.url);
  let bodyToken = "";
  let note = "";
  try {
    const raw = await request.text();
    if (raw) {
      const data = JSON.parse(raw);
      bodyToken = String(data?.token || "").trim();
      note = String(data?.note || "").trim().slice(0, 200);
    }
  } catch {
    return json(400, { ok: false, error: "invalid_json" });
  }

  const provided =
    extractBearer(request) ||
    String(url.searchParams.get("token") || "").trim() ||
    bodyToken;
  if (!provided || provided !== required) {
    return json(401, { ok: false, error: "unauthorized" });
  }

  if (!hasPushNotify(env)) {
    return json(503, {
      ok: false,
      error: "notify_not_configured",
      message:
        "Kein Push-Notify konfiguriert (TELEGRAM_BOT_TOKEN+TELEGRAM_CHAT_ID oder INQUIRY_WEBHOOK_URL).",
      stored: false,
    });
  }

  const receivedAt = new Date().toISOString();
  const requestId = crypto.randomUUID();
  const record = {
    requestId,
    receivedAt,
    source: "boksitsupport.ch/api/inquiry-notify-test",
    fields: {
      company: "BIT Notify-Test",
      first_name: "Stefan",
      last_name: "Test",
      email: "admin@boksitsupport.ch",
      area: "notify-test",
      employees: "—",
      description:
        note ||
        "Dies ist ein Notify-Test ohne KV-Eintrag. Wenn Sie diese Nachricht sehen, funktioniert Push-Notify.",
    },
  };

  console.log("INQUIRY_NOTIFY_TEST_START", requestId);
  const result = await deliverPushNotify(env, record);
  console.log(
    "INQUIRY_NOTIFY_TEST_DONE",
    requestId,
    "ok=",
    result.ok,
    "vias=",
    result.notifyVias.join(","),
  );

  if (!result.ok) {
    return json(502, {
      ok: false,
      error: "notify_failed",
      requestId,
      stored: false,
      notified: false,
      notifyVias: [],
    });
  }

  return json(200, {
    ok: true,
    requestId,
    stored: false,
    notified: true,
    notifyVias: result.notifyVias,
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
        "Access-Control-Allow-Headers": "content-type, authorization",
      },
    });
  }
  return json(405, { ok: false, error: "method_not_allowed" });
}
