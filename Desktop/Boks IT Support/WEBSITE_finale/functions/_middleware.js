/** Redirect www to apex to avoid duplicate content. */
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === "www.boksitsupport.ch") {
    url.hostname = "boksitsupport.ch";
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
