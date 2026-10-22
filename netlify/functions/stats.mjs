// 통계 페이지용: 최근 N일 기록을 [날짜, 종류, 페이지, 유입, 모바일, 첫방문] 줄로 돌려준다.
import { getStore } from "@netlify/blobs";

const KEY = "ffa224045666b883";
const dec = (s) => { try { return decodeURIComponent(s || ""); } catch { return s || ""; } };

export default async (req) => {
  const u = new URL(req.url);
  if (u.searchParams.get("k") !== KEY) return new Response("forbidden", { status: 403 });
  const days = Math.min(90, Math.max(1, +u.searchParams.get("days") || 30));
  const since = new Date(Date.now() + 9 * 3600e3 - (days - 1) * 864e5).toISOString().slice(0, 10);
  const { blobs } = await getStore("stats").list({ prefix: "d/" });
  const rows = [];
  for (const b of blobs) {
    // 키: d/YYYY-MM-DD/종류|페이지|유입|모바일|첫방문|난수 (페이지 안의 / 가 풀려서 저장될 수 있어 앞에서부터 자른다)
    const day = b.key.slice(2, 12);
    if (day < since) continue;
    const [e, p, r, m, f] = b.key.slice(13).split("|");
    rows.push([day, e, dec(p), dec(r), +m, +f]);
  }
  return Response.json({ since, days, rows }, { headers: { "cache-control": "no-store" } });
};

export const config = { path: "/api/stats" };
