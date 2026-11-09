// Grow the embedded booklet's iframe to the full height of its 16 pages, so the page scrolls as one
// (no scroll box inside a scroll box on a phone). Without this, or if the frame cannot be read, the
// iframe keeps its CSS height (80vh) and scrolls on its own.
(function () {
  function fit(frame) {
    try {
      // the body's own height, not the document's scrollHeight: that is never less than the frame's
      // current height, so it could only ever grow
      var body = frame.contentWindow.document.body;
      var h = body ? Math.ceil(body.getBoundingClientRect().height) : 0;
      if (h > 0) frame.style.height = h + "px";
    } catch (e) { /* not readable: keep the CSS height */ }
  }
  function setup() {
    var frames = document.querySelectorAll("iframe.booklet-frame");
    frames.forEach(function (frame) {
      frame.addEventListener("load", function () {
        fit(frame);
        try {
          var win = frame.contentWindow;
          if ("ResizeObserver" in win) {
            new win.ResizeObserver(function () { fit(frame); }).observe(win.document.body);
          }
          // pictures arrive after load on a slow connection
          win.document.querySelectorAll("img").forEach(function (img) {
            img.addEventListener("load", function () { fit(frame); });
          });
        } catch (e) { /* not readable */ }
      });
      fit(frame);
    });
    window.addEventListener("resize", function () { frames.forEach(fit); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", setup);
  else setup();
})();
