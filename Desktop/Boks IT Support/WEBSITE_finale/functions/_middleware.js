/** www→apex 301; root → /de/; legacy hospitality/market → home/services; inactive langs → /de/. EN stays live. */

const INACTIVE_LANG = /^(fr|it|sr|bs|hr)(\/|$)/;
const MARKET_SLUGS = new Set([
  "market",
  "marche",
  "mercato",
  "trziste",
  "markt",
  "market-access",
]);
const HOSPITALITY_SLUG = "hospitality";

/**
 * Map first path segment after lang to a permanent redirect target.
 * Returns null when the path should fall through to static assets / _redirects.
 */
function legacyPathRedirect(lang, firstSeg) {
  if (firstSeg === HOSPITALITY_SLUG) {
    if (lang === "en") {
      return "https://boksitsupport.ch/en/services/";
    }
    return "https://boksitsupport.ch/de/leistungen/";
  }
  if (MARKET_SLUGS.has(firstSeg)) {
    if (lang === "en") {
      return "https://boksitsupport.ch/en/";
    }
    return "https://boksitsupport.ch/de/";
  }
  return null;
}

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.boksitsupport.ch") {
    url.hostname = "boksitsupport.ch";
    return Response.redirect(url.toString(), 301);
  }

  const pathname = url.pathname;
  if (pathname === "/" || pathname === "/index.html") {
    return Response.redirect("https://boksitsupport.ch/de/", 301);
  }

  const path = pathname.replace(/^\/+/, "");
  const segments = path.split("/").filter(Boolean);
  const lang = segments[0] || "";
  const firstSeg = segments[1] || "";

  // Active DE/EN: strip static hospitality/market if anything was left in deploy
  if (lang === "de" || lang === "en") {
    const target = legacyPathRedirect(lang, firstSeg);
    if (target) {
      return Response.redirect(target, 301);
    }
  }

  const match = path.match(INACTIVE_LANG);
  if (match) {
    const rest = path.slice(match[1].length).replace(/^\/+/, "");
    const inactiveFirst = rest.split("/")[0] || "";
    const legacy = legacyPathRedirect(match[1], inactiveFirst);
    if (legacy) {
      return Response.redirect(legacy, 301);
    }
    return Response.redirect("https://boksitsupport.ch/de/", 302);
  }

  return context.next();
}
