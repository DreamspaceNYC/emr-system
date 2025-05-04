export default {
  async fetch(request, env, ctx) {
    return new Response("EMR Worker Deployed Successfully!", { status: 200 });
  }
}
