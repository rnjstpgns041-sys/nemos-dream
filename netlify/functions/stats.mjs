// 사장님 통계 페이지(/admin/stats/)용: 비밀번호가 맞으면 최근 N일 기록을
// [날짜, 종류, 페이지, 유입, 모바일, 첫방문, 방문자ID, 검색어] 줄로 돌려준다.
import { getStore } from "@netlify/blobs";
import { pbkdf2Sync, timingSafeEqual } from "node:crypto";

// 비밀번호는 저장소에 원문 없이 해시로만 둔다.
const SALT = "86773a9f54ec7aa08fb3505b5584eccc";
const HASH = Buffer.from("086af0099539292707a7cfb59118630b77a73bb7d5e983e9bab7bd293abddd71", "hex");
const dec = (s) => { try { return decodeURIComponent(s || ""); } catch { return s || ""; } };

export default async (req) => {
  const u = new URL(req.url);
  const pin = (u.searchParams.get("pin") || "").slice(0, 12);
  if (!pin || !timingSafeEqual(pbkdf2Sync(pin, SALT, 300000, 32, "sha256"), HASH)) {
    await new Promise((r) => setTimeout(r, 800));
    return Response.json({ error: "pin" }, { status: 401 });
  }
  const days = Math.min(90, Math.max(1, +u.searchParams.get("days") || 7));
  const today = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
  const since = new Date(Date.parse(today) - (days - 1) * 864e5).toISOString().slice(0, 10);
  const { blobs } = await getStore("stats").list({ prefix: "d/" });
  const rows = [];
  for (const b of blobs) {
    // 키: d/YYYY-MM-DD/종류|페이지|유입|모바일|첫방문|방문자ID|검색어|난수 (예전 기록은 방문자ID·검색어 없음)
    const day = b.key.slice(2, 12);
    if (day < since) continue;
    const f = b.key.slice(13).split("|");
    const old = f.length < 8;
    rows.push([day, f[0], dec(f[1]), dec(f[2]), +f[3], +f[4], old ? "" : dec(f[5]), old ? "" : dec(f[6])]);
  }
  return Response.json({ today, since, days, rows }, { headers: { "cache-control": "no-store" } });
};

export const config = { path: "/api/stats" };
