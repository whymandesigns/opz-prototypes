/* Injects the designmd icon sprite.
 *
 * These pages link the stylesheets rather than being baked by inline.py, and
 * the stylesheets do not carry the sprite — so every <use href="#i-…"> draws
 * blank with no error until something fetches it. The guard means a page that
 * is later inlined, and so already has the sprite, skips the fetch.
 */
(function () {
  if (document.getElementById('i-check')) return;
  fetch('../../designmd/icons.svg')
    .then(function (r) { return r.ok ? r.text() : null; })
    .then(function (svg) {
      if (!svg) return;
      var host = document.createElement('div');
      host.hidden = true;
      host.innerHTML = svg;
      document.body.insertBefore(host, document.body.firstChild);
    })
    .catch(function () { /* opened from file:// — serve the folder to see icons */ });
})();
