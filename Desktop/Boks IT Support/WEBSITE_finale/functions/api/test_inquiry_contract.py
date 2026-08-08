"""Contract tests for inquiry API delivery paths (no secrets)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INQUIRY = (ROOT / "functions" / "api" / "inquiry.js").read_text(encoding="utf-8")
HEALTH = (ROOT / "functions" / "api" / "inquiry-health.js").read_text(encoding="utf-8")
INQUIRIES = (ROOT / "functions" / "api" / "inquiries.js").read_text(encoding="utf-8")
INQUIRIES_VIEW = (ROOT / "functions" / "api" / "inquiries" / "view.js").read_text(
    encoding="utf-8"
)
WRANGLER = (ROOT / "wrangler.toml").read_text(encoding="utf-8")
CLIENT = (ROOT / "assets" / "js" / "inquiry-form.js").read_text(encoding="utf-8")
DE_PRIVACY = (ROOT / "locales" / "de.json").read_text(encoding="utf-8")
EN_PRIVACY = (ROOT / "locales" / "en.json").read_text(encoding="utf-8")
NOTIFY_DOC = (ROOT / "docs" / "INQUIRY_NOTIFY.md").read_text(encoding="utf-8")
VIEWER_DOC = (ROOT / "docs" / "INQUIRY_VIEWER.md").read_text(encoding="utf-8")
LIST_PS1 = (ROOT / "scripts" / "list_inquiries.ps1").read_text(encoding="utf-8")
NOTIFY_TEST = (ROOT / "functions" / "api" / "inquiry-notify-test.js").read_text(
    encoding="utf-8"
)
ROBOTS = (ROOT / "robots.txt").read_text(encoding="utf-8")


def test_inquiry_kv_webhook_telegram_no_formsubmit() -> None:
    assert "formsubmit.co" not in INQUIRY.lower()
    assert "FormSubmit" not in INQUIRY
    assert "deliverViaFormSubmit" not in INQUIRY
    assert "INQUIRY_LOG" in INQUIRY
    assert "INQUIRY_WEBHOOK_URL" in INQUIRY
    assert "TELEGRAM_BOT_TOKEN" in INQUIRY
    assert "TELEGRAM_CHAT_ID" in INQUIRY
    assert "RESEND_API_KEY" in INQUIRY
    assert "INQUIRY_RESEND_HTTP" in INQUIRY
    assert "buildNotifyText" in INQUIRY
    assert "hasDurableDelivery" in INQUIRY
    assert "hasPushNotify" in INQUIRY
    assert "export function buildNotifyText" in INQUIRY
    assert "export function hasPushNotify" in INQUIRY
    assert "export function escapeHtml" in INQUIRY
    assert "email_notification_status" in INQUIRY
    assert "Neue BIT-Anfrage" in INQUIRY
    assert "INQUIRY_FROM_EMAIL" in INQUIRY
    assert "INQUIRY_NOTIFY_EMAIL" in INQUIRY
    assert "invalid_content_type" in INQUIRY
    assert "unexpected_fields" in INQUIRY
    assert "rate_limited" in INQUIRY
    assert "storage_failed" in INQUIRY
    assert "notified" in INQUIRY
    assert "notifyVias" in INQUIRY
    assert "INQUIRY_STORED_BUT_NOTIFY_FAILED" in INQUIRY
    assert "delivery_not_configured" in INQUIRY
    assert "60 * 60 * 24 * 365" in INQUIRY
    assert 'vias.push("formsubmit")' not in INQUIRY
    assert '"employees"' in INQUIRY
    assert '"area"' in INQUIRY
    assert "OPTIONAL" in INQUIRY


def test_client_sends_meta_and_endpoint() -> None:
    assert 'fetch("/api/inquiry"' in CLIENT
    assert "timestamp" in CLIENT
    assert "source_page" in CLIENT
    assert "showFailure" in CLIENT
    assert "buildMailtoHref" in CLIENT
    assert "formsubmit.co" not in CLIENT.lower()


def test_viewer_shows_email_notification_status() -> None:
    assert "email_notification_status" in INQUIRIES
    assert "email_notification_status" in INQUIRIES_VIEW
    assert "E-Mail-Benachrichtigung" in INQUIRIES_VIEW


def test_health_reports_push_booleans_no_secrets() -> None:
    assert "hasResendKey" in HEALTH
    assert "hasKv" in HEALTH
    assert "hasWebhook" in HEALTH
    assert "hasTelegram" in HEALTH
    assert "hasPushNotify" in HEALTH
    assert "hasFormSubmitNotify" not in HEALTH
    assert "FormSubmit" not in HEALTH
    assert "INQUIRY_FROM" not in HEALTH
    assert "TELEGRAM_BOT_TOKEN" in HEALTH
    assert "from:" not in HEALTH


def test_inquiries_viewer_auth_and_kv() -> None:
    assert "INQUIRY_VIEW_TOKEN" in INQUIRIES
    assert "INQUIRY_DIAG_TOKEN" in INQUIRIES
    assert 'prefix: "inquiry:"' in INQUIRIES or "prefix: KEY_PREFIX" in INQUIRIES
    assert "inquiry:" in INQUIRIES
    assert "cache-control" in INQUIRIES
    assert "no-store" in INQUIRIES
    assert "unauthorized" in INQUIRIES
    assert "auth_not_configured" in INQUIRIES
    assert "503" in INQUIRIES
    assert "kv_not_bound" in INQUIRIES
    assert "Bearer" in INQUIRIES
    assert "MAX_LIMIT" in INQUIRIES or "50" in INQUIRIES
    assert "FormSubmit" not in INQUIRIES
    # Never open when secrets missing: early 503 before KV read
    assert INQUIRIES.index("auth_not_configured") < INQUIRIES.index("kv_not_bound")
    assert "last7Days" in INQUIRIES


def test_html_viewer_escape_auth_and_fields() -> None:
    assert "export function escapeHtml" in INQUIRIES_VIEW
    assert "export function countLast7Days" in INQUIRIES_VIEW
    assert "export function isRecent48h" in INQUIRIES_VIEW
    assert "text/html" in INQUIRIES_VIEW
    assert "noindex" in INQUIRIES_VIEW
    assert "no-store" in INQUIRIES_VIEW
    assert "mailto:" in INQUIRIES_VIEW
    assert "tel:" in INQUIRIES_VIEW
    assert "Einträge der letzten 7 Tage" in INQUIRIES_VIEW
    assert "Neueste Anfrage" in INQUIRIES_VIEW
    assert "Sprachversion" in INQUIRIES_VIEW
    assert "Geschäftliche E-Mail" in INQUIRIES_VIEW
    assert "inquiry.recent" in INQUIRIES_VIEW or "class=\"inquiry recent\"" in INQUIRIES_VIEW
    assert "INQUIRY_VIEW_TOKEN" in INQUIRIES_VIEW
    assert "auth_not_configured" in INQUIRIES_VIEW or "Viewer nicht konfiguriert" in INQUIRIES_VIEW
    assert "unauthorized" in INQUIRIES_VIEW or "Nicht autorisiert" in INQUIRIES_VIEW
    assert "503" in INQUIRIES_VIEW
    assert "401" in INQUIRIES_VIEW
    # Escape covers XSS-sensitive characters
    assert "&amp;" in INQUIRIES_VIEW and "&lt;" in INQUIRIES_VIEW
    assert INQUIRIES_VIEW.index("viewToken") < INQUIRIES_VIEW.index("INQUIRY_LOG.list")


def test_inquiry_kv_required_when_bound_and_language() -> None:
    assert "INQUIRY_STORAGE_FAILED" in INQUIRY
    assert 'fields.language' in INQUIRY or "fields.language =" in INQUIRY
    assert "boksitsupport.ch/en/inquiry/" in INQUIRY
    assert "boksitsupport.ch/de/anfrage/" in INQUIRY
    assert "60 * 60 * 24 * 365" in INQUIRY


def test_wrangler_binds_inquiry_log_kv() -> None:
    assert 'binding = "INQUIRY_LOG"' in WRANGLER
    assert "d6f0c62cf7a14b199355315aa0dec76c" in WRANGLER
    assert "FormSubmit" not in WRANGLER
    assert "TELEGRAM_BOT_TOKEN" in WRANGLER


def test_client_no_formsubmit() -> None:
    assert "formsubmit.co" not in CLIENT.lower()
    assert "notifyFormSubmitBrowser" not in CLIENT
    assert "FormSubmit" not in CLIENT


def test_privacy_mentions_pipeline_no_secrets() -> None:
    for text in (DE_PRIVACY, EN_PRIVACY):
        assert "FormSubmit" not in text
        assert "formsubmit" not in text.lower()
        assert "INQUIRY_LOG" not in text
        assert "INQUIRY_NOTIFY_EMAIL" not in text
        assert "TELEGRAM_BOT_TOKEN" not in text
        assert "INQUIRY_WEBHOOK_URL" not in text
        assert "RESEND_API_KEY" not in text
    assert "dauerhaft" not in DE_PRIVACY
    assert "zwölf Monate" in DE_PRIVACY or "zwoelf Monate" in DE_PRIVACY
    assert "twelve months" in EN_PRIVACY.lower()
    assert "Cloudflare-Endpunkt" in DE_PRIVACY or "Cloudflare" in DE_PRIVACY
    assert "Cloudflare endpoint" in EN_PRIVACY or "Cloudflare" in EN_PRIVACY
    assert "Resend" in DE_PRIVACY
    assert "Resend" in EN_PRIVACY
    assert "admin@boksitsupport.ch" in DE_PRIVACY
    assert "admin@boksitsupport.ch" in EN_PRIVACY


def test_notify_docs_and_list_script_exist() -> None:
    assert "INQUIRY_VIEW_TOKEN" in NOTIFY_DOC
    assert "/api/inquiries" in NOTIFY_DOC
    assert "/api/inquiry-notify-test" in NOTIFY_DOC
    assert "list_inquiries.ps1" in NOTIFY_DOC
    assert "HTML viewer" in NOTIFY_DOC or "HTML-Viewer" in NOTIFY_DOC or "INQUIRY_VIEWER" in NOTIFY_DOC
    assert "optional" in NOTIFY_DOC.lower() or "Optional" in NOTIFY_DOC
    assert "TOKEN_PLACEHOLDER" in VIEWER_DOC
    assert "/api/inquiries/view" in VIEWER_DOC
    assert "INQUIRY_VIEW_TOKEN" in VIEWER_DOC
    assert "Workers & Pages" in VIEWER_DOC or "website" in VIEWER_DOC
    assert "Redeploy" in VIEWER_DOC or "redeploy" in VIEWER_DOC
    assert "INQUIRY_VIEW_TOKEN" in LIST_PS1 or "Token" in LIST_PS1
    assert "/api/inquiries" in LIST_PS1
    assert "/api/inquiries" in ROBOTS or "/api/inquiries/view" in ROBOTS
    assert "Disallow: /api/inquiries" in ROBOTS


def test_notify_test_endpoint_no_kv() -> None:
    assert "inquiry-notify-test" in NOTIFY_TEST or "NOTIFY_TEST" in NOTIFY_TEST
    assert "deliverPushNotify" in NOTIFY_TEST
    assert ".put(" not in NOTIFY_TEST
    assert 'stored: false' in NOTIFY_TEST
    assert "INQUIRY_VIEW_TOKEN" in NOTIFY_TEST
    assert "INQUIRY_DIAG_TOKEN" in NOTIFY_TEST
    assert "auth_not_configured" in NOTIFY_TEST
    assert "unauthorized" in NOTIFY_TEST
    assert "503" in NOTIFY_TEST
    # Auth gate before any Telegram/webhook send (import may appear earlier)
    assert NOTIFY_TEST.index("auth_not_configured") < NOTIFY_TEST.index(
        "await deliverPushNotify"
    )
    assert "export async function deliverPushNotify" in INQUIRY
    assert "INQUIRY_STORED_BUT_NOTIFY_FAILED" in INQUIRY


def test_health_never_exposes_secrets_or_contents() -> None:
    assert "hasKv" in HEALTH
    assert "hasPushNotify" in HEALTH
    # Response payload is booleans only — no secret values, chat IDs, or inquiry bodies
    assert "chat.id" not in HEALTH
    assert "TELEGRAM_CHAT_ID" in HEALTH  # presence check only
    assert "INQUIRY_VIEW_TOKEN" not in HEALTH
    assert "requestId" not in HEALTH
    assert "receivedAt" not in HEALTH
    assert "never returns secret values" in HEALTH


def test_client_preserves_fields_on_failure() -> None:
    assert "showFailure" in CLIENT
    assert "buildMailtoHref" in CLIENT
    assert "form.reset()" in CLIENT
    # reset only on success path; failure must not clear
    assert "Stattdessen per E-Mail senden" in CLIENT
    assert "reportValidity" in CLIENT
    assert "Keep all field values" not in CLIENT or "do not claim send failure" in CLIENT or "Browser shows field errors" in CLIENT
