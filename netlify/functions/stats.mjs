// 통계 페이지용: 최근 N일 기록을 [날짜, 종류, 페이지, 유입, 모바일, 첫방문] 줄로 돌려준다.
import { getStore } from "@netlify/blobs";

const KEY = "ffa224045666b883";

export default async (req) => {
  const u = new URL(req.url);
  if (u.searchParams.get("k") !== KEY) return new Response("forbidden", { status: 403 });
  const days = Math.min(90, Math.max(1, +u.searchParams.get("days") || 30));
  const since = new Date(Date.now() + 9 * 3600e3 - (days - 1) * 864e5).toISOString().slice(0, 10);
  const { blobs } = await getStore("stats").list({ prefix: "d/" });
  const rows = [];
  for (const b of blobs) {
    const [, day, rest] = b.key.split("/");
    if (day < since) continue;
    const [e, p, r, m, f] = rest.split("|");
    rows.push([day, e, decodeURIComponent(p), decodeURIComponent(r), +m, +f]);
  }
  return Response.json({ since, days, rows }, { headers: { "cache-control": "no-store" } });
};

export const config = { path: "/api/stats" };
