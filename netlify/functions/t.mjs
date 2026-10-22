// 방문·클릭 기록: 한 번 들어올 때마다 키 하나를 남긴다(값은 비움). 개인정보는 저장하지 않는다.
import { getStore } from "@netlify/blobs";

const EVENTS = ["view", "phone", "sms", "copy", "quote"];
const clean = (s) => encodeURIComponent((s || "").slice(0, 80));

export default async (req) => {
  const u = new URL(req.url);
  const e = u.searchParams.get("e");
  const ua = req.headers.get("user-agent") || "";
  if (!EVENTS.includes(e) || /bot|crawl|spider|headless|lighthouse/i.test(ua)) return new Response(null, { status: 204 });
  const day = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
  const parts = [e, clean(u.searchParams.get("p")), clean(u.searchParams.get("r")), u.searchParams.get("m") === "1" ? 1 : 0, u.searchParams.get("f") === "1" ? 1 : 0];
  const key = `d/${day}/${parts.join("|")}|${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
  await getStore("stats").set(key, "");
  return new Response(null, { status: 204 });
};

export const config = { path: "/api/t" };
