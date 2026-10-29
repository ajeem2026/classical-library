// Loads the 3D stage once the player is usable. If anything here fails, the
// hatched SVG placeholder stays and the music is unaffected.
const host = document.getElementById("stage-canvas");

function webglAvailable() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGL2RenderingContext && c.getContext("webgl2"));
  } catch { return false; }
}

async function start() {
  if (!webglAvailable()) return;
  try {
    const { createStage } = await import("./scene.js");
    window.__stage = await createStage(host); // handy in the console: __stage.bands
    host.classList.add("live");
  } catch (err) {
    console.warn("[stage] staying on the placeholder:", err);
  }
}

const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 200));
if (document.readyState === "complete") idle(start);
else window.addEventListener("load", () => idle(start), { once: true });
