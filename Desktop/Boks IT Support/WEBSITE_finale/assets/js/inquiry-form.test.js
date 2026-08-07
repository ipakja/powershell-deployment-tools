import { describe, expect, it } from "vitest";

import {
  buildMailtoHref,
  enforceOfflineSubmit,
  isInquiryOffline,
} from "./inquiry-form.js";

describe("inquiry mailto fallback", () => {
  it("encodes subject and all fields into the mailto body", () => {
    const href = buildMailtoHref({
      company: "Hotel Seeblick GmbH",
      first_name: "Anna",
      last_name: "Meier",
      email: "anna@example.ch",
      phone: "+41 44 000 00 00",
      location: "Zürich",
      industry: "Hospitality",
      employees: "11–25",
      workstations: "16–40",
      m365: "Ja",
      internal_it: "Nein",
      external_it: "Ja",
      area: "Benutzer und Zugänge",
      start: "innerhalb 2 Wochen",
      description: "Neuer Mitarbeiter braucht Outlook + MFA",
    });

    expect(href.startsWith("mailto:admin@boksitsupport.ch?")).toBe(true);
    expect(href).toContain(encodeURIComponent("BIT Anfrage: Hotel Seeblick GmbH"));
    expect(href).toContain(encodeURIComponent("Neuer Mitarbeiter braucht Outlook + MFA"));
    expect(href).toContain(encodeURIComponent("anna@example.ch"));
  });
});

describe("inquiry offline gating", () => {
  it("detects offline from data-inquiry-offline", () => {
    const form = document.createElement("form");
    form.dataset.inquiryOffline = "true";
    expect(isInquiryOffline(form)).toBe(true);
  });

  it("forces submit button HTML disabled when offline", () => {
    const form = document.createElement("form");
    form.dataset.inquiryOffline = "true";
    const button = document.createElement("button");
    button.type = "submit";
    button.disabled = false;
    form.append(button);

    enforceOfflineSubmit(form);

    expect(button.disabled).toBe(true);
    expect(button.getAttribute("disabled")).toBe("disabled");
    expect(button.getAttribute("aria-disabled")).toBe("true");
  });

  it("does not alter submit button when live", () => {
    const form = document.createElement("form");
    const button = document.createElement("button");
    button.type = "submit";
    form.append(button);

    enforceOfflineSubmit(form);

    expect(button.disabled).toBe(false);
  });
});
