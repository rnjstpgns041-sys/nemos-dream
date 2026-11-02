// 견적 폼: 손님이 '견적 보내기'를 누르면 내용과 사진을 저장하고, 사장님 휴대폰으로 문자(솔라피)를 보낸다.
// 문자 발송은 Netlify 환경변수 SOLAPI_API_KEY, SOLAPI_API_SECRET, SMS_FROM(등록한 발신번호)이 있을 때만 켜진다.
// 사진은 문자 안의 링크(비밀 토큰 포함)로만 볼 수 있다.
import { getStore } from "@netlify/blobs";
import { createHmac, randomBytes } from "node:crypto";

const env = (k) => (typeof Netlify !== "undefined" ? Netlify.env.get(k) : process.env[k]) || "";
const enabled = () => !!(env("SOLAPI_API_KEY") && env("SOLAPI_API_SECRET") && env("SMS_FROM"));
const SITE = "https://nemos-dream.com";
const MAX_PHOTOS = 5, MAX_PHOTO_BYTES = 1.5e6;
const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const esc = (s) => String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const cut = (s, n) => String(s || "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, n);

async function sendSms(text) {
  const key = env("SOLAPI_API_KEY"), secret = env("SOLAPI_API_SECRET");
  const date = new Date().toISOString(), salt = randomBytes(16).toString("hex");
  const signature = createHmac("sha256", secret).update(date + salt).digest("hex");
  const r = await fetch("https://api.solapi.com/messages/v4/send", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `HMAC-SHA256 apiKey=${key}, date=${date}, salt=${salt}, signature=${signature}` },
    body: JSON.stringify({ message: { to: (env("SMS_TO") || "01048353353").replace(/\D/g, ""), from: env("SMS_FROM").replace(/\D/g, ""), subject: "네모의꿈 견적 문의", text } }),
  });
  return r.ok;
}

function viewPage(q, id, k) {
  const rows = [["작업", q.job], ["지역", q.area], ["연락처", q.phone], ["냉장고", q.model], ["상황", (q.tags || []).join(", ")], ["내용", q.msg], ["받은 시각", q.at]]
    .filter((r) => r[1]).map((r) => `<tr><th>${r[0]}</th><td>${r[0] === "연락처" ? `<a href="tel:${esc(r[1])}">${esc(r[1])}</a>` : esc(r[1])}</td></tr>`).join("");
  const imgs = Array.from({ length: q.photos || 0 }, (_, n) => `<a href="/api/quote?img=${id}&n=${n}&k=${k}"><img src="/api/quote?img=${id}&n=${n}&k=${k}" alt="현장 사진 ${n + 1}"></a>`).join("");
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>견적 문의 사진</title>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#f4f5f7;color:#191f28}main{max-width:640px;margin:0 auto;padding:20px 16px 40px}h1{font-size:22px}table{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden}th,td{padding:12px;border-bottom:1px solid #eee;text-align:left;vertical-align:top;font-size:16px}th{width:80px;color:#6b7684;font-weight:600}img{width:100%;border-radius:14px;margin-top:12px;display:block}a{color:#00843d}</style></head>
<body><main><h1>네모의꿈 견적 문의</h1><table>${rows}</table>${imgs || "<p>사진 없이 보낸 문의예요.</p>"}</main></body></html>`;
}

export default async (req) => {
  const u = new URL(req.url), p = (k) => u.searchParams.get(k);
  const store = getStore("quotes");

  if (req.method === "GET") {
    if (p("cfg") !== null) return json({ enabled: enabled() });
    const id = (p("view") || p("img") || "").replace(/[^a-z0-9]/g, ""), k = p("k") || "";
    const q = id && (await store.get(`q/${id}.json`, { type: "json" }));
    if (!q || q.k !== k) return new Response("없는 문의예요.", { status: 404, headers: { "content-type": "text/plain; charset=utf-8" } });
    if (p("img") !== null) {
      const b = await store.get(`p/${id}/${parseInt(p("n")) || 0}`, { type: "arrayBuffer" });
      return b ? new Response(b, { headers: { "content-type": "image/jpeg", "cache-control": "private, max-age=86400" } }) : new Response(null, { status: 404 });
    }
    return new Response(viewPage(q, id, k), { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
  }

  if (req.method !== "POST") return new Response(null, { status: 405 });
  if (!enabled()) return json({ ok: false, error: "off" }, 503);
  let d;
  try { d = await req.json(); } catch { return json({ ok: false, error: "bad" }, 400); }
  if (d.website) return json({ ok: true }); // 스팸 봇용 빈칸
  const phone = cut(d.phone, 20).replace(/[^\d-]/g, "");
  if (phone.replace(/\D/g, "").length < 9) return json({ ok: false, error: "phone" }, 400);
  const photos = (Array.isArray(d.photos) ? d.photos : []).slice(0, MAX_PHOTOS)
    .map((s) => (/^data:image\/jpeg;base64,/.test(s) ? Buffer.from(s.split(",")[1], "base64") : null))
    .filter((b) => b && b.length <= MAX_PHOTO_BYTES);
  const id = Date.now().toString(36) + randomBytes(3).toString("hex"), k = randomBytes(9).toString("hex");
  const q = {
    job: cut(d.job, 30), area: cut(d.area, 60), model: cut(d.model, 60), msg: cut(d.msg, 500), phone,
    tags: (Array.isArray(d.tags) ? d.tags : []).slice(0, 8).map((t) => cut(t, 40)),
    photos: photos.length, k, at: new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 16).replace("T", " "),
  };
  await Promise.all(photos.map((b, n) => store.set(`p/${id}/${n}`, b)));
  await store.setJSON(`q/${id}.json`, q);
  const link = `${SITE}/api/quote?view=${id}&k=${k}`;
  const text = ["[네모의꿈 견적 문의]", `작업: ${q.job}`, `지역: ${q.area}`, `연락처: ${q.phone}`]
    .concat(q.model ? [`냉장고: ${q.model}`] : [], q.tags.length ? [`상황: ${q.tags.join(", ")}`] : [], q.msg ? [`내용: ${q.msg}`] : [])
    .concat([q.photos ? `사진 ${q.photos}장: ${link}` : `사진 없음 (자세히: ${link})`]).join("\n");
  const sent = await sendSms(text).catch(() => false);
  return json({ ok: sent, id }, sent ? 200 : 502);
};

export const config = { path: "/api/quote" };
