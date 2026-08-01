// Caution! Be sure you understand the caveats before publishing an application with
// offline support. See https://aka.ms/blazor-offline-considerations

self.importScripts('./service-worker-assets.js');
self.addEventListener('install', event => event.waitUntil(onInstall(event)));
self.addEventListener('activate', event => event.waitUntil(onActivate(event)));
self.addEventListener('fetch', event => event.respondWith(onFetch(event)));
self.addEventListener('message', event => {
    if (event.data === 'skipWaiting') self.skipWaiting();
});

const cacheNamePrefix = 'offline-cache-';
const cacheName = `${cacheNamePrefix}${self.assetsManifest.version}`;
const offlineAssetsInclude = [ /\.dll$/, /\.pdb$/, /\.wasm/, /\.html/, /\.js$/, /\.json$/, /\.css$/, /\.woff2?$/, /\.png$/, /\.jpe?g$/, /\.gif$/, /\.ico$/, /\.svg$/, /\.webp$/, /\.blat$/, /\.dat$/, /\.webmanifest$/ ];
const offlineAssetsExclude = [ /^service-worker\.js$/, /^service-worker-assets\.js$/ ];

// File extensions with Brotli pre-compressed (.br) versions on the server.
const brCacheExtensions = /\.(wasm|dat|pdb)$/;

// Replace with your base path if you are hosting on a subfolder. Ensure there is a trailing '/'.
const base = "/";
const baseUrl = new URL(base, self.origin);
const manifestUrlList = self.assetsManifest.assets.map(asset => new URL(asset.url, baseUrl).href);

async function onInstall(event) {
    console.info('Service worker: Install');

    const assets = self.assetsManifest.assets
        .filter(asset => offlineAssetsInclude.some(pattern => pattern.test(asset.url)))
        .filter(asset => !offlineAssetsExclude.some(pattern => pattern.test(asset.url)));

    const cache = await caches.open(cacheName);
    await Promise.all(assets.map(async asset => {
        try {
            const useBr = brCacheExtensions.test(asset.url);
            const fetchUrl = useBr ? asset.url + '.br' : asset.url;
            const response = await fetch(fetchUrl, { cache: 'no-cache' });
            if (response.ok) {
                await cache.put(fetchUrl, response);
            }
        } catch (e) {
            console.warn(`Service worker: Failed to cache ${asset.url}`, e);
        }
    }));
}

async function onActivate(event) {
    console.info('Service worker: Activate');

    const cacheKeys = await caches.keys();
    await Promise.all(cacheKeys
        .filter(key => key.startsWith(cacheNamePrefix) && key !== cacheName)
        .map(key => caches.delete(key)));

    await self.clients.claim();
}

async function onFetch(event) {
    let cachedResponse = null;
    if (event.request.method === 'GET') {
        const requestUrl = new URL(event.request.url);

        // Runtime caching for external CDN resources
        if (requestUrl.hostname === 'fonts.googleapis.com' ||
            requestUrl.hostname === 'fonts.gstatic.com') {
            const runtimeCache = await caches.open('runtime-cdn-cache');
            cachedResponse = await runtimeCache.match(event.request);
            const fetchPromise = fetch(event.request).then(response => {
                if (response.ok) {
                    runtimeCache.put(event.request, response.clone());
                }
                return response;
            }).catch(() => null);

            if (cachedResponse) {
                return cachedResponse;
            }
            const networkResponse = await fetchPromise;
            if (networkResponse) {
                return networkResponse;
            }
            return new Response('', { status: 503 });
        }

        const shouldServeIndexHtml = event.request.mode === 'navigate'
            && !manifestUrlList.some(url => url === event.request.url);

        const request = shouldServeIndexHtml ? 'index.html' : event.request;
        const cache = await caches.open(cacheName);
        cachedResponse = await cache.match(request, { ignoreSearch: true });
    }

    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        return await fetch(event.request);
    } catch {
        if (event.request.mode === 'navigate') {
            const cache = await caches.open(cacheName);
            const indexResponse = await cache.match('index.html');
            if (indexResponse) return indexResponse;
        }
        return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
    }
}
