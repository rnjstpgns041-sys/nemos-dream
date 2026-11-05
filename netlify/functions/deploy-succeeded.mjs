// 배포가 끝날 때마다 Netlify가 자동으로 부르는 함수.
// 이번 배포에서 새로 생긴 페이지 주소(new-urls.txt)를 IndexNow로 네이버·빙에 알린다. 결과는 /api/t?idx 로 볼 수 있다.
import { connectLambda, getStore } from "@netlify/blobs";

const SITE = "https://nemos-dream.com";
const KEY = "3b803cc3c386e3ddf55fc1e0c6734db0";
const ENDPOINTS = ["https://searchadvisor.naver.com/indexnow", "https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"];

export const handler = async (event) => {
  let log = { at: new Date().toISOString(), urls: 0, res: {} };
  try {
    const txt = await (await fetch(`${SITE}/new-urls.txt?t=${Date.now()}`)).text();
    const urls = txt.split("\n").map((s) => s.trim()).filter((s) => s.startsWith(SITE + "/"));
    log.urls = urls.length;
    if (urls.length) {
      const body = JSON.stringify({ host: "nemos-dream.com", key: KEY, keyLocation: `${SITE}/${KEY}.txt`, urlList: urls.concat(`${SITE}/sitemap.xml`) });
      for (const e of ENDPOINTS) {
        try { log.res[e] = (await fetch(e, { method: "POST", headers: { "content-type": "application/json; charset=utf-8" }, body })).status; }
        catch (x) { log.res[e] = String(x).slice(0, 80); }
      }
    }
  } catch (x) { log.error = String(x).slice(0, 120); }
  try { connectLambda(event); await getStore("indexnow").setJSON("last", log); } catch (x) {}
  console.log("indexnow", JSON.stringify(log));
  return { statusCode: 200 };
};
