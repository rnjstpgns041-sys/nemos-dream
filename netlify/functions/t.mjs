// 방문·클릭 기록: 한 번 들어올 때마다 키 하나를 남긴다(값은 비움). 이름·전화번호 같은 개인정보는 저장하지 않는다.
import { getStore } from "@netlify/blobs";

const EVENTS = ["view", "phone", "sms", "copy", "quote"];
const clean = (s, n) => encodeURIComponent((s || "").replace(/\|/g, " ").slice(0, n));

export default async (req) => {
  const u = new URL(req.url);
  const q = (k) => u.searchParams.get(k);
  const e = q("e");
  const ua = req.headers.get("user-agent") || "";
  if (!EVENTS.includes(e) || /bot|crawl|spider|headless|lighthouse/i.test(ua)) return new Response(null, { status: 204 });
  const day = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
  // 종류|페이지|유입|모바일|첫방문|방문자ID|검색어
  const parts = [e, clean(q("p"), 60), clean(q("r"), 40), q("m") === "1" ? 1 : 0, q("f") === "1" ? 1 : 0, clean((q("v") || "").replace(/[^a-z0-9]/g, ""), 10), clean(q("k"), 20)];
  const key = `d/${day}/${parts.join("|")}|${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
  await getStore("stats").set(key, "");
  return new Response(null, { status: 204 });
};

export const config = { path: "/api/t" };
