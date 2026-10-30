// The library as one walnut bookcase: which binding each composer's books wear, how the
// books are packed onto shared shelves, and how each title is fitted to its spine.
(function () {
  // Bindings, by composer surname: the material and its tone, all mixed from the palette.
  const BINDINGS = {
    Bach: "calf", Beethoven: "vellum", Borodin: "buckram", Brahms: "morocco", Chopin: "calf-dark",
    Debussy: "cloth-pale", "Dvořák": "buckram-warm", Haydn: "calf-light", Mendelssohn: "morocco-dark",
    Mozart: "vellum-warm", Schubert: "cloth", Suk: "cloth-gold", Tchaikovsky: "morocco-warm",
  };
  const binding = (surname) => "bind-" + (BINDINGS[surname] || "cloth");

  // ---- Packing ----
  const BOOKEND = 8, GAP = 1, GROUP_GAP = 7, LEAN = 6;   // px, px, px, degrees
  const width = (g) => g.books.reduce((s, b) => s + (b.flat ? b.tall : b.thick) + (b.lean || 0), 0)
    + GAP * (g.books.length - 1) + 2 * BOOKEND;

  // Groups of books, in order, onto shelves `inner` px wide. Each composer stays on one shelf.
  // The thickest group sets a scale, so a composer never has to be split.
  function pack(groups, inner) {
    groups = groups.map((g) => ({ ...g, books: g.books.map((b) => ({ ...b })) }));
    const scale = Math.min(1, inner / Math.max(...groups.map(width)));
    groups.forEach((g) => g.books.forEach((b) => (b.thick = Math.floor(b.thick * scale))));
    const shelves = [];
    let cur = null;
    for (const g of groups) {
      const w = width(g);
      if (!cur || cur.used + GROUP_GAP + w > inner) shelves.push((cur = { groups: [], used: -GROUP_GAP }));
      cur.groups.push(g);
      cur.used += GROUP_GAP + w;
    }
    const room = (s) => inner - s.used;

    // One book lies flat on a short shelf: the tallest book on the roomiest shelf, when there is
    // space for it on its side and laying it down lets that shelf be lower.
    let flat = null;
    for (const s of shelves) {
      const books = s.groups.flatMap((g) => g.books);
      if (books.length < 2) continue;
      const [top, next] = [...books].sort((a, b) => b.tall - a.tall);
      if (room(s) >= top.tall - top.thick + 4 && top.tall - next.tall >= 4 && (!flat || room(s) > room(flat.s)))
        flat = { s, top };
    }
    if (flat) {
      const g = flat.s.groups.find((g) => g.books.includes(flat.top));
      g.books.splice(g.books.indexOf(flat.top), 1);
      g.books.push(flat.top);
      flat.top.flat = true;
      flat.s.used += flat.top.tall - flat.top.thick;
      flat.s.short = true;
    }

    // A few loose books lean on their neighbour, where a shelf has the room.
    let leaning = 0;
    for (const s of shelves) {
      if (leaning >= 3) break;
      const g = [...s.groups].filter((g) => g.books.length >= 2 && !g.books.at(-1).flat)
        .sort((a, b) => b.books.length - a.books.length)[0];
      if (!g) continue;
      const [nb, b] = g.books.slice(-2);
      const gap = Math.ceil(Math.min(nb.tall, b.tall) * Math.tan((LEAN * Math.PI) / 180)) + 1;
      if (room(s) < gap + 6) continue;
      b.lean = gap;
      s.used += gap;
      leaning++;
    }

    const standing = (s) => Math.max(...s.groups.flatMap((g) => g.books.filter((b) => !b.flat).map((b) => b.tall)), 0);
    const tallest = Math.max(...shelves.map(standing));
    for (const s of shelves) {
      s.clear = s.short ? standing(s) + 12 : tallest + 24;
      for (const g of s.groups) g.bookend = Math.round(0.56 * Math.min(...g.books.filter((b) => !b.flat).map((b) => b.tall), 200));
    }
    return shelves;
  }

  // ---- Titles ----
  // Ways to set a title on a spine, fullest first; the full title is always the accessible name.
  const SHORTER = [
    [/^String Quartet/, "Str. Qt."], [/^Symphony/, "Sym."], [/^Piano Sonata/, "Pf. Sonata"],
    [/^Goldberg Variations/, "Goldberg Var."], [/^Suite bergamasque: /, ""],
    [/^Pf\. Sonata No\. 14 ‘Moonlight’/, "‘Moonlight’ Sonata"], [/^‘Moonlight’ Sonata/, "‘Moonlight’"],
    [/^Meditation on the Old Czech Chorale ‘St\. Wenceslas’/, "Meditation, ‘St. Wenceslas’"],
    [/^Meditation, /, "Medit. "],
  ];
  const curly = (s) => s.replace(/'([^']+)'/g, "‘$1’");
  function titleSets(w, horizontal) {
    const cat = (w.catalogue || w.key || "").replace(/,? Hob\..*$/, "");
    const catShort = cat.replace(/ Nos?\. /g, "/").replace(/, Op\. /g, ", ");   // Op. 9/1–3, 27/2
    const catTiny = catShort.includes(", ") ? catShort.replace(/\/[\d–]+/g, "") : catShort;   // Op. 9, 27
    const titles = [curly(w.work)];
    for (const [re, to] of SHORTER) {
      const t = titles.at(-1).replace(re, to);
      if (t !== titles.at(-1)) titles.push(t);
    }
    const sets = [], seen = new Set();
    const add = (...lines) => {
      lines = lines.filter(Boolean);
      if (!seen.has(lines.join("\n"))) { seen.add(lines.join("\n")); sets.push(lines); }
    };
    for (const t of titles) {
      if (horizontal) add(cat ? `${t}, ${cat}` : t);
      add(t, cat); add(t, catShort); add(t, catTiny);
    }
    // The title broken over the two lines, the catalogue riding on the second.
    for (const t of titles) {
      const m = / (No\. \d+)$/.exec(t) || /, (.+)$/.exec(t);
      if (m) add(t.slice(0, m.index), m[1] + (catShort ? ` · ${catShort}` : ""));
    }
    // Last, the title alone on two lines (the catalogue is still in the accessible name).
    for (const t of titles) {
      const m = / (No\. \d+)$/.exec(t) || /, (.+)$/.exec(t);
      if (m) add(t.slice(0, m.index), m[1]);
    }
    add(catShort ? `${titles.at(-1)}, ${catShort}` : titles.at(-1));
    return sets;
  }

  const LH = 1.02, SPACING = 0.02;
  const canvas = document.createElement("canvas").getContext("2d");
  const measured = new Map();
  function measure(text, size) {
    const key = size + "|" + text;
    if (!measured.has(key)) {
      canvas.font = `500 ${size}px Newsreader, Georgia, serif`;
      measured.set(key, canvas.measureText(text).width * 1.04 + SPACING * size * text.length);
    }
    return measured.get(key);
  }
  // Largest size, from 16 px down, at which a set fits the panel; full sets are tried at 12 px
  // and up before a shorter set is used, then at 10.5 px, and anything goes down to 9.5 px.
  function fit(el, work, horizontal) {
    const box = el.parentElement;
    const along = (horizontal ? box.clientWidth : box.clientHeight) - 8;
    const across = (horizontal ? box.clientHeight : box.clientWidth) - 5;
    const sets = titleSets(work, horizontal);
    for (const min of [12, 10.5, 9.5]) {
      for (const lines of sets) {
        for (let size = 16; size >= min; size -= 0.5) {
          if (lines.length * size * LH > across) continue;
          if (Math.max(...lines.map((l) => measure(l, size))) <= along) {
            el.textContent = lines.join("\n");
            el.style.fontSize = size + "px";
            return;
          }
        }
      }
    }
    el.textContent = sets.at(-1).join("\n");
    el.style.fontSize = "9.5px";
  }

  // Deckled paper edge: an irregular polygon, the same for a book every time it is opened.
  function deckle(seed) {
    let s = seed;
    const r = () => ((s = (s * 16807) % 2147483647) / 2147483647);
    const pts = ["0 0"];
    for (let x = 1; x < 100; x += 1 + r() * 1.5) pts.push(`${x.toFixed(1)}% ${(r() * 2.6).toFixed(1)}px`);
    for (let y = 0; y < 100; y += 0.6 + r() * 1.2) pts.push(`calc(100% - ${(r() * 3).toFixed(1)}px) ${y.toFixed(1)}%`);
    for (let x = 100; x > 1; x -= 1 + r() * 1.5) pts.push(`${x.toFixed(1)}% calc(100% - ${(r() * 2.6).toFixed(1)}px)`);
    pts.push("0 100%");
    return `polygon(${pts.join(", ")})`;
  }

  window.Bookcase = { binding, pack, fit, deckle };
})();
