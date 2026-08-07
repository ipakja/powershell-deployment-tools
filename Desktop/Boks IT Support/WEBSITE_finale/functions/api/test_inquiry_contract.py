"""Contract tests for inquiry API delivery paths (no secrets)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INQUIRY = (ROOT / "functions" / "api" / "inquiry.js").read_text(encoding="utf-8")
HEALTH = (ROOT / "functions" / "api" / "inquiry-health.js").read_text(encoding="utf-8")
INQUIRIES = (ROOT / "functions" / "api" / "inquiries.js").read_text(encoding="utf-8")
WRANGLER = (ROOT / "wrangler.toml").read_text(encoding="utf-8")
CLIENT = (ROOT / "assets" / "js" / "inquiry-form.js").read_text(encoding="utf-8")
DE_PRIVACY = (ROOT / "locales" / "de.json").read_text(encoding="utf-8")
EN_PRIVACY = (ROOT / "locales" / "en.json").read_text(encoding="utf-8")
NOTIFY_DOC = (ROOT / "docs" / "INQUIRY_NOTIFY.md").read_text(encoding="utf-8")
LIST_PS1 = (ROOT / "scripts" / "list_inquiries.ps1").read_text(encoding="utf-8")


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
    assert "notified" in INQUIRY
    assert "notifyVias" in INQUIRY
    assert "INQUIRY_STORED_BUT_NOTIFY_FAILED" in INQUIRY
    assert "delivery_not_configured" in INQUIRY
    assert "60 * 60 * 24 * 365" in INQUIRY
    assert 'vias.push("formsubmit")' not in INQUIRY
    assert '"employees"' in INQUIRY
    assert '"area"' in INQUIRY
    assert "OPTIONAL" in INQUIRY


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
    assert "kv_not_bound" in INQUIRIES
    assert "Bearer" in INQUIRIES
    assert "MAX_LIMIT" in INQUIRIES or "50" in INQUIRIES
    assert "FormSubmit" not in INQUIRIES


def test_wrangler_binds_inquiry_log_kv() -> None:
    assert 'binding = "INQUIRY_LOG"' in WRANGLER
    assert "d6f0c62cf7a14b199355315aa0dec76c" in WRANGLER
    assert "FormSubmit" not in WRANGLER
    assert "TELEGRAM_BOT_TOKEN" in WRANGLER


def test_client_no_formsubmit() -> None:
    assert "formsubmit.co" not in CLIENT.lower()
    assert "notifyFormSubmitBrowser" not in CLIENT
    assert "FormSubmit" not in CLIENT


def test_privacy_mentions_messaging_notify_no_secrets() -> None:
    for text in (DE_PRIVACY, EN_PRIVACY):
        assert "FormSubmit" not in text
        assert "formsubmit" not in text.lower()
        assert "INQUIRY_LOG" not in text
        assert "INQUIRY_NOTIFY_EMAIL" not in text
        assert "TELEGRAM_BOT_TOKEN" not in text
        assert "INQUIRY_WEBHOOK_URL" not in text
    assert "dauerhaft" not in DE_PRIVACY
    assert "zwölf Monate" in DE_PRIVACY or "zwoelf Monate" in DE_PRIVACY
    assert "twelve months" in EN_PRIVACY.lower()
    assert "Messaging" in DE_PRIVACY or "Telegram" in DE_PRIVACY
    assert "messaging" in EN_PRIVACY.lower() or "Telegram" in EN_PRIVACY


def test_notify_docs_and_list_script_exist() -> None:
    assert "TELEGRAM_BOT_TOKEN" in NOTIFY_DOC
    assert "TELEGRAM_CHAT_ID" in NOTIFY_DOC
    assert "INQUIRY_VIEW_TOKEN" in NOTIFY_DOC
    assert "/api/inquiries" in NOTIFY_DOC
    assert "BotFather" in NOTIFY_DOC
    assert "list_inquiries.ps1" in NOTIFY_DOC
    assert "INQUIRY_VIEW_TOKEN" in LIST_PS1 or "Token" in LIST_PS1
    assert "/api/inquiries" in LIST_PS1
