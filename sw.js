/* Hanzi Drill service worker (template).
 *
 * build_site.py replaces the two placeholders below:
 *   VERSION - a content hash, so the cache name changes whenever any file does
 *   FILES   - JSON array of every URL to precache (relative to this file)
 *
 * Everything is precached at install, so the app works fully offline and an
 * update is atomic: the new worker only takes over the next time the app is
 * opened after all its pages are closed (no skipWaiting on purpose), so one
 * session never mixes old and new files.
 *
 * The origin (oliverjward.github.io) is shared with other projects, so this
 * worker only ever touches caches whose name starts with "hanzi-drill-".
 */
const VERSION = '__VERSION__';
const FILES = __FILES__;
const PREFIX = 'hanzi-drill-';
const CACHE = PREFIX + VERSION;

// Install: precache everything. addAll is atomic: if any file fails, the
// install fails and the old version keeps running.
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)));
});

// Activate: drop old hanzi-drill caches (and only those), then take control.
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names
          .filter((n) => n.startsWith(PREFIX) && n !== CACHE)
          .map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: serve from this version's own precache. Nothing is ever written at runtime.
// Always look in CACHE, not caches.match() across all caches: while an update is
// waiting, the next version's cache already exists, and the running version must
// not be handed its files.
self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  if (!request.url.startsWith(self.registration.scope)) return; // same origin + in scope

  // Single-page app: every navigation gets the cached start page.
  const key = request.mode === 'navigate' ? './' : request;
  event.respondWith(
    caches.open(CACHE)
      .then((cache) => cache.match(key, { ignoreSearch: true }))
      .then((hit) => hit || fetch(request))
  );
});
