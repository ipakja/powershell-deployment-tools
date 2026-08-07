/**
 * Inquiry delivery diagnostics – never returns secret values,
 * tokens, chat IDs, or inquiry contents.
 * GET /api/inquiry-health
 * Public for boolean flags when INQUIRY_DIAG_TOKEN is unset.
 * Optional: ?token=… must match env.INQUIRY_DIAG_TOKEN when that secret is set.
 * Booleans only: hasKv, hasResendKey, hasWebhook, hasTelegram, hasPushNotify.
 */
function json(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function hasTelegram(env) {
  return Boolean(
    String(env?.TELEGRAM_BOT_TOKEN || "").trim() &&
      String(env?.TELEGRAM_CHAT_ID || "").trim(),
  );
}

function hasWebhook(env) {
  return Boolean(String(env?.INQUIRY_WEBHOOK_URL || "").trim());
}

function hasResendKey(env) {
  return Boolean(env?.RESEND_API_KEY);
}

/** True when any push/notify path is configured (webhook OR telegram OR resend). */
function hasPushNotify(env) {
  return hasWebhook(env) || hasTelegram(env) || hasResendKey(env);
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const requiredToken = String(env.INQUIRY_DIAG_TOKEN || "").trim();

  if (requiredToken) {
    const provided = url.searchParams.get("token") || "";
    if (provided !== requiredToken) {
      return json(401, { ok: false, error: "unauthorized" });
    }
  }

  return json(200, {
    ok: true,
    hasKv: Boolean(env.INQUIRY_LOG),
    hasResendKey: hasResendKey(env),
    hasWebhook: hasWebhook(env),
    hasTelegram: hasTelegram(env),
    hasPushNotify: hasPushNotify(env),
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
        "Access-Control-Allow-Headers": "content-type",
      },
    });
  }
  return json(405, { ok: false, error: "method_not_allowed" });
}
