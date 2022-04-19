
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('mellomlager').then( function (cache) {
            return cache.addAll([
                './index.html',
                './',
                './noe.png',
                './manifest.json',
                './app.js',
                './app.css',
                './app.html',
                'http://localhost:8180/cgi-bin/diktbase.cgi/dikt/',
              ]);
        })
    );
});

self.addEventListener('fetch', function (event) {
    let online = navigator.onLine;
    if(!online){
    event.respondWith(
        caches.match(event.request)
    );
    }
});
