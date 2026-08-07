export default {
  async fetch(request) {
    const url = new URL(request.url);
    url.hostname = "boksitsupport.ch";
    return Response.redirect(url.toString(), 301);
  },
};
