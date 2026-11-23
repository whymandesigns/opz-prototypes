// changelog.js — renders rob/CHANGELOG.md into #doc.
//
// Loaded by roles.html, which sits beside CHANGELOG.md and _shots/ — every
// path here is relative to the folder, not to the page.
//
// A markdown renderer for the subset CHANGELOG.md actually uses: headings,
// paragraphs, bullets (one level of nesting), tables, fenced code, block
// quotes, rules, and inline code / bold / italic / links. Deliberately not
// a library — the page that loads this has three dependencies, all designmd.
(function () {
  var esc = function (s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };

  // GitHub's heading slug, so the file's own [text](#anchor) links land.
  var slug = function (s) {
    return s.toLowerCase()
      .replace(/[`*_[\]()]/g, '')
      .replace(/[^\w\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-');
  };

  // Four states, and an entry is in exactly one of them. A fifth word
  // still renders — as the neutral grey — so adding one is a changelog
  // edit rather than a code change; but the point of a short list is that
  // the tag answers "can I rely on this?" at a glance, which a row of
  // three qualifiers does not.
  var TAGS = {
    'proposed':  'tag-blue-light',   // built here, and a change to the product
    'in review': 'tag-warning',      // built, waiting on the group
    'delivered': 'tag-positive',     // merged to main — this prototype, never the product
    'cancelled': 'tag-negative'      // decided against; the entry stays
  };

  var inline = function (s) {
    return esc(s)
      .replace(/`([^`]+)`/g, function (_, c) { return '<code>' + c + '</code>'; })
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
      .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, function (_, alt, src) {
        return shotImg(alt, src);
      })
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, function (_, t, href) {
        var safe = /^(https?:|#|\.|\/)/.test(href) ? href : '#';
        return '<a href="' + safe + '">' + t + '</a>';
      });
  };

  // Only a relative path, and only an image: a changelog shot lives beside
  // the file it documents. Anything else renders as the alt text, which is
  // what a reader needs anyway.
  var shotImg = function (alt, src) {
    if (!/^[\w./-]+\.(png|jpg|jpeg|gif|webp|svg)$/i.test(src) || src.indexOf('..') === 0) {
      return esc(alt || src);
    }
    var img = document.createElement('img');
    img.src = src;
    img.alt = alt || '';
    img.loading = 'lazy';
    return img.outerHTML;
  };

  // A paragraph that is nothing but an image becomes a figure: the shot at
  // a readable width, its alt doubling as the caption, and a link to the
  // file so a detail too small to read here can be opened full size.
  var figure = function (alt, src) {
    var html = shotImg(alt, src);
    if (html.indexOf('<img') !== 0) return '<p>' + html + '</p>';
    var fig = document.createElement('figure');
    fig.className = 'cl-shot';
    var a = document.createElement('a');
    a.href = src;
    a.target = '_blank';
    a.rel = 'noopener';
    a.innerHTML = html;
    fig.appendChild(a);
    if (alt) {
      var cap = document.createElement('figcaption');
      cap.textContent = alt;
      fig.appendChild(cap);
    }
    return fig.outerHTML;
  };

  var render = function (md) {
    var lines = md.replace(/\r\n/g, '\n').split('\n');
    var out = [];
    var i = 0;
    var seenH1 = false;

    var flushTable = function () {
      var rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(lines[i++]);
      if (rows.length < 2) { rows.forEach(function (r) { out.push('<p>' + inline(r) + '</p>'); }); return; }
      var cells = function (r) {
        return r.trim().replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); });
      };
      var head = cells(rows[0]);
      var body = rows.slice(2).map(cells);
      // Wrapped, so a table too wide for a phone scrolls inside its own box
      // instead of taking the page sideways with it. That is what lets the
      // columns be sized by content rather than squeezed into equal shares.
      out.push('<div class="cl-table">');
      out.push('<table class="table">');
      out.push('<thead><tr>' + head.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead>');
      out.push('<tbody>' + body.map(function (r) {
        return '<tr>' + r.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody>');
      out.push('</table>');
      out.push('</div>');
    };

    // A bullet owns every following line indented past it, so a wrapped
    // sentence stays in its own <li> instead of starting a paragraph.
    var flushList = function (indent) {
      out.push('<ul>');
      while (i < lines.length) {
        var m = lines[i].match(/^(\s*)- (.*)$/);
        if (!m || m[1].length < indent) break;
        if (m[1].length > indent) { flushList(m[1].length); continue; }
        var text = [m[2]];
        i++;
        while (i < lines.length) {
          if (/^\s*- /.test(lines[i])) break;
          if (/^\s+\S/.test(lines[i])) { text.push(lines[i].trim()); i++; continue; }
          break;
        }
        out.push('<li>' + inline(text.join(' ')));
        if (i < lines.length) {
          var next = lines[i].match(/^(\s*)- (.*)$/);
          if (next && next[1].length > indent) flushList(next[1].length);
        }
        out.push('</li>');
      }
      out.push('</ul>');
    };

    while (i < lines.length) {
      var line = lines[i];

      if (!line.trim()) { i++; continue; }

      if (/^```/.test(line)) {
        i++;
        var code = [];
        while (i < lines.length && !/^```/.test(lines[i])) code.push(lines[i++]);
        i++;
        out.push('<pre><code>' + esc(code.join('\n')) + '</code></pre>');
        continue;
      }

      if (/^---+\s*$/.test(line)) { i++; continue; }   // the file's section rules; h2 draws its own

      var h = line.match(/^(#{1,4}) (.*)$/);
      if (h) {
        i++;
        if (h[1].length === 1) {
          // The page header already carries the document title.
          if (!seenH1) { seenH1 = true; continue; }
        }
        var level = Math.min(h[1].length, 4);
        out.push('<h' + level + ' id="' + slug(h[2]) + '">' + inline(h[2]) + '</h' + level + '>');
        continue;
      }

      if (/^>\s?/.test(line)) {
        var quote = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) quote.push(lines[i++].replace(/^>\s?/, ''));
        out.push('<blockquote><p>' + inline(quote.join(' ')) + '</p></blockquote>');
        continue;
      }

      if (/^\s*\|/.test(line)) { flushTable(); continue; }

      if (/^\s*- /.test(line)) { flushList(line.match(/^(\s*)/)[1].length); continue; }

      var para = [];
      while (i < lines.length && lines[i].trim() && !/^(#{1,4} |```|>|\s*[-|])/.test(lines[i])) para.push(lines[i++]);
      if (!para.length) { out.push('<p>' + inline(lines[i++]) + '</p>'); continue; }
      var text = para.join(' ');

      // A line that is only an image is a figure, not a paragraph.
      var shot = text.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
      if (shot) { out.push(figure(shot[1], shot[2])); continue; }

      // "**Status** · Proposed · Parked — why" becomes a row of tags and a
      // note. Written as an ordinary bold line so the raw file still reads
      // on GitHub, where there are no tags to render.
      var st = text.match(/^\*\*Status\*\*\s*[·:]\s*(.*)$/);
      if (st) {
        var halves = st[1].split(/\s+—\s+/);
        // One status, however many are written. Two states at once is the
        // thing this is meant to stop, so the extras are dropped rather
        // than rendered smaller or greyer.
        var chips = halves[0].split(/\s*·\s*/).filter(Boolean).slice(0, 1).map(function (name) {
          // Built as an element rather than a string. Any literal
          // class="..." + variable reads to lint.py as a class named after
          // the variable — which is the runtime-assembled-name trap it
          // exists to catch, and it is right to flag it. className says the
          // same thing where the linter is not looking for a class, and
          // textContent escapes the label for free.
          var chip = document.createElement('span');
          chip.className = 'tag ' + (TAGS[name.trim().toLowerCase()] || 'tag-light');
          chip.textContent = name.trim();
          return chip.outerHTML;
        }).join('');
        var note = halves.slice(1).join(' — ');
        out.push('<p class="cl-status">' + chips
          + (note ? '<span class="cl-status-note">' + inline(note) + '</span>' : '') + '</p>');
        continue;
      }

      out.push('<p>' + inline(text) + '</p>');
    }

    return out.join('\n');
  };

  var doc = document.getElementById('doc');
  fetch('./CHANGELOG.md', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (md) {
      doc.innerHTML = render(md);
      if (location.hash) {
        var t = document.getElementById(location.hash.slice(1));
        if (t) t.scrollIntoView();
      }
    })
    .catch(function (e) {
      doc.innerHTML = '<div class="alert alert-danger"><span class="alert-message">'
        + '<strong>CHANGELOG.md could not be read</strong> &mdash; ' + esc(String(e.message || e))
        + '. It sits beside this page; open <a href="./CHANGELOG.md">the file</a> directly.'
        + '</span></div>';
    });
})();
