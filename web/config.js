// Personalise the player here. Colours and fonts live at the top of style.css.
window.PLAYER_CONFIG = {
  title: "Inside Jeem’s head",

  // Where audio comes from:
  //   "auto"    – your local files when served by `make serve`, otherwise archive.org
  //   "local"   – always ./media/ (needs `make serve`)
  //   "archive" – always stream from archive.org (what the live site uses)
  source: "auto",

  // When a work finishes, carry on with the next work in the current view.
  continuous: true,

  // Seconds skipped by the ← / → keys.
  seekStep: 10,
};
