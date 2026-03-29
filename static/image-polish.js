document.addEventListener("DOMContentLoaded", () => {
  const article = document.querySelector(".content");
  if (!article) return;

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  initImagePolish(article);
  initZoom(article);
  if (!prefersReduced) initGSAP(article);
});

function initImagePolish(article) {
  const images = Array.from(article.querySelectorAll("img"));

  images.forEach((img) => {
    if (!img.hasAttribute("loading")) img.setAttribute("loading", "lazy");
    if (!img.hasAttribute("decoding")) img.setAttribute("decoding", "async");

    img.classList.add("img-loading");
    const markReady = () => {
      img.classList.remove("img-loading");
      img.classList.add("img-ready");
    };
    if (img.complete) markReady();
    else {
      img.addEventListener("load", markReady, { once: true });
      img.addEventListener(
        "error",
        () => img.classList.remove("img-loading"),
        { once: true },
      );
    }

    if (!img.closest(".image-frame")) {
      const frame = document.createElement("figure");
      frame.className = "image-frame";
      img.parentNode.insertBefore(frame, img);
      frame.appendChild(img);

      const maybeCaptionP = frame.nextElementSibling;
      if (maybeCaptionP && maybeCaptionP.tagName === "P") {
        const em = maybeCaptionP.querySelector("em");
        const onlyText =
          maybeCaptionP.textContent.trim() === em?.textContent.trim();
        if (em && onlyText) {
          const cap = document.createElement("figcaption");
          cap.className = "image-caption";
          cap.textContent = em.textContent.trim();
          frame.appendChild(cap);
          maybeCaptionP.remove();
        }
      }
    }
  });
}

function initZoom(article) {
  if (!window.mediumZoom) return;
  mediumZoom(".content img", {
    margin: 24,
    background: "rgba(17, 24, 39, 0.85)",
  });
  article
    .querySelectorAll("img")
    .forEach((img) => img.classList.add("zoomable"));
}

function initGSAP(article) {
  if (!window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);

  gsap.utils.toArray(".nav-links a, .brand").forEach((el) => {
    el.addEventListener("mouseenter", () =>
      gsap.to(el, { y: -2, duration: 0.18, ease: "power2.out" }),
    );
    el.addEventListener("mouseleave", () =>
      gsap.to(el, { y: 0, duration: 0.18, ease: "power2.out" }),
    );
  });

  gsap.utils.toArray(".content a").forEach((el) => {
    el.addEventListener("mouseenter", () =>
      gsap.to(el, { y: -1, duration: 0.14, ease: "power2.out" }),
    );
    el.addEventListener("mouseleave", () =>
      gsap.to(el, { y: 0, duration: 0.14, ease: "power2.out" }),
    );
  });

  gsap.utils.toArray(".image-frame img").forEach((img) => {
    img.addEventListener("mouseenter", () =>
      gsap.to(img, { scale: 1.02, duration: 0.22, ease: "power2.out" }),
    );
    img.addEventListener("mouseleave", () =>
      gsap.to(img, { scale: 1, duration: 0.22, ease: "power2.out" }),
    );
  });

  const revealTargets = article.querySelectorAll(
    "h1, h2, h3, p, ul, ol, blockquote, pre, .image-frame",
  );

  gsap.set(revealTargets, { opacity: 0, y: 10 });

  revealTargets.forEach((el) => {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.45,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 88%",
        once: true,
      },
    });
  });
}
