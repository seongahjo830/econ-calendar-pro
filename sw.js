// 경제캘린더 PWA 서비스 워커 v1.1.0
// 전략: Network First → 캐시 폴백 (오프라인 동작 유지 + 업데이트 즉시 전파)
const CACHE = 'econ-cal-v1.1.0';
const PRECACHE = ['./', './index.html', './manifest.json',
                  './icon-192.png', './icon-512.png', './icon-maskable-512.png'];

self.addEventListener('install', e => {
  // 새 워커 즉시 활성화 (이전 버전 캐시 안 기다림)
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  // 옛날 캐시 삭제 + 즉시 모든 탭 제어
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  // 같은 origin만 처리 (외부 리소스는 건드리지 않음)
  if (url.origin !== self.location.origin) return;

  e.respondWith(
    // 1. 항상 네트워크 먼저
    fetch(e.request).then(res => {
      // 응답 캐시에 저장 (다음 오프라인 대비)
      const clone = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, clone));
      return res;
    }).catch(() =>
      // 2. 네트워크 실패(오프라인) 시 캐시 폴백
      caches.match(e.request).then(cached => cached || caches.match('./index.html'))
    )
  );
});

// 메시지로 즉시 갱신 트리거 가능
self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});
