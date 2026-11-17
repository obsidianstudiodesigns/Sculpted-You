/* Sculpted You: cart, menu, age gate, shop filter, BMI calculator and checkout. No dependencies
   (blueimp-md5 is loaded on the checkout page only, for the PayFast signature). */
(function () {
  "use strict";
  var ROOT = new URL("../../", document.currentScript.src).href;
  var PRODUCTS = window.SY_PRODUCTS || {};
  var CFG = window.SY_CONFIG || { shipping: 100, payfast: {} };
  var SHIP = CFG.shipping || 100;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key));
      if (val === null) localStorage.removeItem(key); else localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }
  function rand(n) { return "R " + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function icon(name) {
    var paths = {
      plus: "M228,128a12,12,0,0,1-12,12H140v76a12,12,0,0,1-24,0V140H40a12,12,0,0,1,0-24h76V40a12,12,0,0,1,24,0v76h76A12,12,0,0,1,228,128Z",
      minus: "M228,128a12,12,0,0,1-12,12H40a12,12,0,0,1,0-24H216A12,12,0,0,1,228,128Z",
      x: "M204.24,195.76a6,6,0,1,1-8.48,8.48L128,136.49,60.24,204.24a6,6,0,0,1-8.48-8.48L119.51,128,51.76,60.24a6,6,0,0,1,8.48-8.48L128,119.51l67.76-67.75a6,6,0,0,1,8.48,8.48L136.49,128Z"
    };
    return '<svg class="ic" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="' + paths[name] + '"/></svg>';
  }

  /* ---------------------------------------------------------------- toast */
  var toastEl = $("[data-toast]"), toastT;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  }

  /* ---------------------------------------------------------------- cart */
  function cart() {
    var c = store("sy-cart") || {};
    Object.keys(c).forEach(function (k) { if (!PRODUCTS[k] || !(c[k] > 0)) delete c[k]; });
    return c;
  }
  function saveCart(c) { store("sy-cart", c); renderCart(); }
  function cartLines() {
    var c = cart();
    return Object.keys(c).map(function (slug) {
      var p = PRODUCTS[slug];
      return { slug: slug, p: p, qty: c[slug], total: p.price * c[slug] };
    });
  }
  function subtotal() { return cartLines().reduce(function (s, l) { return s + l.total; }, 0); }
  function count() { return cartLines().reduce(function (s, l) { return s + l.qty; }, 0); }
  function title(p) { return p.name + (p.strength ? " " + p.strength : ""); }

  function add(slug, qty) {
    var c = cart();
    c[slug] = Math.min(20, (c[slug] || 0) + (qty || 1));
    saveCart(c);
    var badge = $("[data-cart-count]");
    if (badge) { badge.classList.remove("bump"); void badge.offsetWidth; badge.classList.add("bump"); }
    toast(title(PRODUCTS[slug]) + " added to your cart");
  }
  function setQty(slug, qty) {
    var c = cart();
    if (qty <= 0) delete c[slug]; else c[slug] = Math.min(20, qty);
    saveCart(c);
  }

  function renderCart() {
    var n = count(), badge = $("[data-cart-count]");
    if (badge) { badge.textContent = n; badge.hidden = n === 0; }
    var box = $("[data-cart-items]"), foot = $("[data-cart-foot]");
    if (box) {
      var lines = cartLines();
      if (!lines.length) {
        box.innerHTML = '<div class="cart-empty"><svg class="ic" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,42H40A14,14,0,0,0,26,56V200a14,14,0,0,0,14,14H216a14,14,0,0,0,14-14V56A14,14,0,0,0,216,42Zm2,158a2,2,0,0,1-2,2H40a2,2,0,0,1-2-2V56a2,2,0,0,1,2-2H216a2,2,0,0,1,2,2ZM174,88a46,46,0,0,1-92,0,6,6,0,0,1,12,0,34,34,0,0,0,68,0,6,6,0,0,1,12,0Z"/></svg><p>Your cart is empty.</p><a class="btn btn-gold" href="' + ROOT + 'shop/">Shop peptides</a></div>';
        if (foot) foot.hidden = true;
      } else {
        box.innerHTML = lines.map(function (l) {
          return '<div class="line-item"><img src="' + ROOT + l.p.img + '" alt="" width="64" height="80" loading="lazy">' +
            '<div><a class="li-name" href="' + ROOT + l.p.url + '">' + esc(l.p.name) + '</a><span class="li-meta">' + esc(l.p.strength) + '</span>' +
            '<div class="li-qty"><button type="button" data-dec="' + l.slug + '" aria-label="Decrease">' + icon("minus") + '</button><span>' + l.qty + '</span>' +
            '<button type="button" data-inc="' + l.slug + '" aria-label="Increase">' + icon("plus") + '</button></div></div>' +
            '<div class="li-price"><span class="price">' + rand(l.total) + '</span><button class="li-remove" type="button" data-remove="' + l.slug + '" aria-label="Remove ' + esc(title(l.p)) + '">' + icon("x") + '</button></div></div>';
        }).join("");
        if (foot) foot.hidden = false;
      }
    }
    var st = subtotal();
    $$("[data-cart-subtotal]").forEach(function (el) { el.textContent = rand(st); });
    $$("[data-cart-total]").forEach(function (el) { el.textContent = rand(st + SHIP); });
    renderSummary();
  }

  var drawer = $("[data-drawer]"), lastFocus;
  function openCart() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.hidden = false;
    document.body.style.overflow = "hidden";
    var c = $("[data-cart-close].icon-btn", drawer); if (c) c.focus();
  }
  function closeCart() {
    if (!drawer || drawer.hidden) return;
    drawer.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener("click", function (ev) {
    var t = ev.target.closest("button, a");
    if (!t) return;
    if (t.hasAttribute("data-add")) {
      var q = 1;
      if (t.hasAttribute("data-add-qty")) { var inp = $("[data-qty-input]"); q = Math.max(1, Math.min(20, parseInt(inp && inp.value, 10) || 1)); }
      add(t.getAttribute("data-add"), q);
      t.classList.add("added");
      setTimeout(function () { t.classList.remove("added"); }, 900);
    } else if (t.hasAttribute("data-cart-open")) { openCart(); }
    else if (t.hasAttribute("data-cart-close")) { closeCart(); }
    else if (t.hasAttribute("data-inc")) { var s = t.getAttribute("data-inc"); setQty(s, (cart()[s] || 0) + 1); }
    else if (t.hasAttribute("data-dec")) { var d = t.getAttribute("data-dec"); setQty(d, (cart()[d] || 0) - 1); }
    else if (t.hasAttribute("data-remove")) { setQty(t.getAttribute("data-remove"), 0); }
  });
  var scrim = $(".drawer-scrim"); if (scrim) scrim.addEventListener("click", closeCart);
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeCart(); closeMenu(); } });

  /* ---------------------------------------------------------------- menu */
  var menu = $("[data-menu]"), menuBtn = $("[data-menu-open]");
  function openMenu() { menu.hidden = false; menu.setAttribute("data-open", ""); menuBtn.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden"; $("[data-menu-close]").focus(); }
  function closeMenu() { if (!menu || menu.hidden) return; menu.hidden = true; menu.removeAttribute("data-open"); menuBtn.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; menuBtn.focus(); }
  if (menu && menuBtn) {
    menuBtn.addEventListener("click", openMenu);
    $("[data-menu-close]").addEventListener("click", closeMenu);
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menu.hidden = true; document.body.style.overflow = ""; }); });
  }

  /* ---------------------------------------------------------------- age gate */
  var age = $("[data-age]");
  if (age && !store("sy-age") && typeof age.showModal === "function") {
    age.showModal();
    age.addEventListener("cancel", function (e) { e.preventDefault(); });
    $("[data-age-yes]").addEventListener("click", function () { store("sy-age", Date.now()); age.close(); });
  }

  /* ---------------------------------------------------------------- product rail */
  var rail = $("[data-rail]");
  if (rail) {
    var step = function (dir) { var card = rail.firstElementChild; rail.scrollBy({ left: dir * (card ? card.offsetWidth + 18 : 300) * 2, behavior: "smooth" }); };
    $("[data-rail-prev]").addEventListener("click", function () { step(-1); });
    $("[data-rail-next]").addEventListener("click", function () { step(1); });
  }

  /* ---------------------------------------------------------------- shop filter */
  var grid = $("[data-grid]");
  if (grid) {
    var chips = $$("[data-filter]");
    var apply = function (f) {
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === f)); });
      $$(".pcard", grid).forEach(function (card) { card.hidden = f !== "all" && card.getAttribute("data-cat") !== f; });
    };
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var f = c.getAttribute("data-filter");
        apply(f);
        history.replaceState(null, "", f === "all" ? location.pathname : "#" + f);
      });
    });
    var h = location.hash.slice(1);
    if (h && $('[data-filter="' + h + '"]')) apply(h);
  }

  /* ---------------------------------------------------------------- product page */
  var qty = $("[data-qty]");
  if (qty) {
    var qi = $("[data-qty-input]", qty);
    var clamp = function (v) { qi.value = Math.max(1, Math.min(20, v || 1)); };
    $("[data-qty-dec]", qty).addEventListener("click", function () { clamp(parseInt(qi.value, 10) - 1); });
    $("[data-qty-inc]", qty).addEventListener("click", function () { clamp(parseInt(qi.value, 10) + 1); });
    qi.addEventListener("change", function () { clamp(parseInt(qi.value, 10)); });
  }
  var sticky = $("[data-sticky-buy]"), buy = $(".buy");
  if (sticky && buy && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { sticky.hidden = e.isIntersecting || e.boundingClientRect.top > 0; });
    }).observe(buy);
  }

  /* ---------------------------------------------------------------- BMI */
  var bmiForm = $("[data-bmi]");
  if (bmiForm) {
    var BANDS = [
      { max: 18.5, name: "Underweight", msg: "Weight-loss peptides aren't suitable in this range. Speak to a doctor about healthy weight gain. Recovery and brain health peptides may still interest you.", picks: [] },
      { max: 25, name: "Healthy range", msg: "Weight-loss peptides are generally not needed in this range. People here more often look at recovery, skin or energy.", picks: ["ghk-cu-100mg", "bpc-157-10mg", "nad-500mg"] },
      { max: 30, name: "Overweight", msg: "GLP-1 medicines are usually considered from a BMI of 27 with a weight-related condition, such as high blood pressure or prediabetes. Gentler metabolic support is another option. People in this range most often ask about:", picks: ["semaglutide-10mg", "5-amino-1mq", "aod9604-2mg"] },
      { max: 35, name: "Obesity class 1", msg: "This is the range where GLP-1 peptides are typically considered. Most people start with semaglutide; tirzepatide suits insulin resistance. People in this range most often ask about:", picks: ["semaglutide-10mg", "tirzepatide-30mg"] },
      { max: 40, name: "Obesity class 2", msg: "Stronger GLP-1 options are often discussed in this range, with a doctor monitoring you. People in this range most often ask about:", picks: ["tirzepatide-30mg", "retatrutide-30mg", "semaglutide-10mg"] },
      { max: 999, name: "Obesity class 3", msg: "Please work closely with a doctor in this range. The strongest GLP-1 options are often discussed. People in this range most often ask about:", picks: ["retatrutide-30mg", "tirzepatide-30mg"] }
    ];
    bmiForm.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var hEl = bmiForm.h, wEl = bmiForm.w, ok = true;
      [hEl, wEl].forEach(function (el) {
        var f = el.closest(".field"), good = el.value !== "" && el.checkValidity();
        f.classList.toggle("invalid", !good); ok = ok && good;
      });
      if (!ok) return;
      var m = parseFloat(hEl.value) / 100, bmi = parseFloat(wEl.value) / (m * m);
      var band = BANDS.filter(function (b) { return bmi < b.max; })[0];
      var pos = Math.max(2, Math.min(98, (bmi - 15) / (45 - 15) * 100));
      var picks = band.picks.map(function (s) { var p = PRODUCTS[s]; return '<a class="chip" href="' + ROOT + p.url + '">' + esc(title(p)) + "</a>"; }).join("");
      $("[data-bmi-result]").innerHTML =
        '<div><p class="bmi-num">' + bmi.toFixed(1) + '</p><p class="bmi-band">' + band.name + '</p>' +
        '<div class="scale" role="img" aria-label="BMI scale with your result marked"><span class="scale-mark" style="left:' + pos + '%"></span></div>' +
        '<div class="scale-labels"><span>15</span><span>25</span><span>35</span><span>45</span></div>' +
        '<p class="bmi-msg">' + band.msg + "</p>" + (picks ? '<div class="bmi-picks">' + picks + "</div>" : "") +
        '<p class="fine" style="margin-top:18px">This is not medical advice. Start with bloodwork and speak to a doctor.</p></div>';
    });
  }

  /* ---------------------------------------------------------------- checkout */
  function renderSummary() {
    var box = $("[data-summary-items]");
    if (!box) return;
    box.innerHTML = cartLines().map(function (l) {
      return '<div class="sum-item"><span>' + l.qty + " x " + esc(title(l.p)) + "</span><span>" + rand(l.total) + "</span></div>";
    }).join("");
    var st = subtotal();
    $("[data-sum-subtotal]").textContent = rand(st);
    $("[data-sum-total]").textContent = rand(st + SHIP);
  }

  var co = $("[data-checkout]");
  if (co) initCheckout();

  function initCheckout() {
    var steps = $$("[data-step]", co), details = store("sy-details") || {}, decl = null;
    if (CFG.payfast && CFG.payfast.sandbox) $("[data-test-banner]").hidden = false;

    function show(n) {
      if (!cartLines().length) {
        steps.forEach(function (s) { s.hidden = true; });
        $("[data-co-empty]").hidden = false;
        return;
      }
      steps.forEach(function (s) { s.hidden = s.getAttribute("data-step") !== String(n); });
      $$("[data-step-dot]").forEach(function (d) {
        var k = +d.getAttribute("data-step-dot");
        d.classList.toggle("done", k < n);
        if (k === n) d.setAttribute("aria-current", "step"); else d.removeAttribute("aria-current");
      });
      window.scrollTo({ top: co.offsetTop - 80, behavior: "smooth" });
    }

    function validate(form) {
      var ok = true;
      $$("input[required], select[required]", form).forEach(function (el) {
        if (el.type === "checkbox" || el.closest("[hidden]")) return;
        var good = el.value.trim() !== "" && el.checkValidity();
        var f = el.closest(".field"); if (f) f.classList.toggle("invalid", !good);
        ok = ok && good;
      });
      return ok;
    }

    // Step 1: details
    var f1 = $('[data-step="1"]');
    Object.keys(details).forEach(function (k) { if (f1.elements[k]) f1.elements[k].value = details[k]; });
    f1.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!validate(f1)) { var bad = $(".invalid input, .invalid select", f1); if (bad) bad.focus(); return; }
      details = {};
      ["name_first", "name_last", "email", "cell", "address", "suburb", "city", "province", "postal", "notes"].forEach(function (k) { details[k] = f1.elements[k].value.trim(); });
      store("sy-details", details);
      var sn = $('[name="sign_name"]'); if (sn && !sn.value) sn.value = details.name_first + " " + details.name_last;
      show(2);
    });

    // Step 2: declaration
    var f2 = $('[data-step="2"]'), pp = $("[data-passport]"), idField = $("[data-id-field]");
    $("[data-passport-toggle]").addEventListener("change", function (e) {
      pp.hidden = !e.target.checked; idField.hidden = e.target.checked;
    });
    var sig = initSignature($("[data-sig]"));
    $("[data-sig-clear]").addEventListener("click", sig.clear);

    f2.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var ok = true, usePassport = !pp.hidden, idNum = "", dob = "";
      if (usePassport) {
        var ppEl = f2.elements.passport, dobEl = f2.elements.dob;
        var ppOk = ppEl.value.trim().length >= 5;
        ppEl.closest(".field").classList.toggle("invalid", !ppOk);
        var dobOk = dobEl.value && ageFrom(new Date(dobEl.value)) >= 18;
        dobEl.closest(".field").classList.toggle("invalid", !dobOk);
        ok = ppOk && dobOk; idNum = ppEl.value.trim().toUpperCase(); dob = dobEl.value;
      } else {
        var v = f2.elements.id_number.value.replace(/\s/g, ""), r = checkSAID(v);
        idField.classList.toggle("invalid", !r);
        ok = !!r; idNum = v; if (r) dob = r;
      }
      var nameEl = f2.elements.sign_name, nameOk = nameEl.value.trim().length > 2;
      nameEl.closest(".field").classList.toggle("invalid", !nameOk);
      var sigOk = sig.hasInk();
      $("[data-sig-err]").classList.toggle("show", !sigOk);
      var boxes = ["c_terms", "c_risk", "c_doctor"].every(function (n) { return f2.elements[n].checked; });
      $("[data-checks-err]").classList.toggle("show", !boxes);
      if (!(ok && nameOk && sigOk && boxes)) { var bad = $(".invalid input, .err.show", f2); if (bad) bad.scrollIntoView({ block: "center", behavior: "smooth" }); return; }
      decl = {
        idType: usePassport ? "passport" : "sa_id", idNumber: idNum, dateOfBirth: dob,
        signedName: nameEl.value.trim(), signature: sig.data(), termsVersion: CFG.termsVersion,
        acceptedAt: new Date().toISOString(), userAgent: navigator.userAgent,
        statements: ["terms", "own_risk", "bloodwork_and_doctor"]
      };
      renderReview();
      show(3);
    });
    $$("[data-back]").forEach(function (b) { b.addEventListener("click", function () { show(+b.getAttribute("data-back")); }); });

    function renderReview() {
      var lines = cartLines(), st = subtotal();
      var masked = decl.idNumber.replace(/.(?=.{4})/g, "*");
      $("[data-review]").innerHTML =
        "<h3>Items</h3>" + lines.map(function (l) { return '<div class="sum-item"><span>' + l.qty + " x " + esc(title(l.p)) + "</span><span>" + rand(l.total) + "</span></div>"; }).join("") +
        '<div class="sum-item"><span>Courier</span><span>' + rand(SHIP) + '</span></div><div class="sum-item"><strong>Total</strong><strong>' + rand(st + SHIP) + "</strong></div>" +
        "<h3>Deliver to</h3><dl><dt>Name</dt><dd>" + esc(details.name_first + " " + details.name_last) + "</dd><dt>Address</dt><dd>" +
        esc([details.address, details.suburb, details.city, details.province, details.postal].join(", ")) + "</dd><dt>Contact</dt><dd>" + esc(details.email + ", " + details.cell) + "</dd></dl>" +
        "<h3>Declaration</h3><dl><dt>Signed by</dt><dd>" + esc(decl.signedName) + "</dd><dt>" + (decl.idType === "sa_id" ? "SA ID" : "Passport") + "</dt><dd>" + esc(masked) +
        "</dd><dt>Accepted</dt><dd>" + new Date(decl.acceptedAt).toLocaleString("en-ZA") + " (terms " + esc(decl.termsVersion) + ")</dd></dl>";
    }

    // Step 3: pay
    $("[data-pay]").addEventListener("click", function () {
      var btn = this, pf = CFG.payfast || {};
      if (!decl) { show(2); return; }
      if (pf.sign !== false && typeof window.md5 !== "function") { toast("Payment is still loading. Please try again in a moment."); return; }
      btn.disabled = true;
      var ref = "SY-" + Date.now().toString(36).toUpperCase();
      var lines = cartLines(), total = subtotal() + SHIP;
      var desc = lines.map(function (l) { return l.qty + "x " + title(l.p); }).join(", ");
      var fields = [
        ["merchant_id", pf.merchantId], ["merchant_key", pf.merchantKey],
        ["return_url", ROOT + "order/thank-you/?ref=" + ref], ["cancel_url", ROOT + "order/cancelled/"], ["notify_url", pf.notifyUrl || ""],
        ["name_first", details.name_first], ["name_last", details.name_last], ["email_address", details.email],
        ["m_payment_id", ref], ["amount", total.toFixed(2)],
        ["item_name", "Sculpted You order " + ref], ["item_description", desc.slice(0, 250)],
        ["custom_str1", "declaration " + decl.termsVersion + " " + decl.acceptedAt]
      ].filter(function (f) { return f[1] !== undefined && String(f[1]).trim() !== ""; });
      if (pf.sign !== false) {
        var sigStr = fields.map(function (f) { return f[0] + "=" + pfEncode(f[1]); }).join("&");
        if (pf.passphrase) sigStr += "&passphrase=" + pfEncode(pf.passphrase);
        fields.push(["signature", window.md5(sigStr)]);
      }

      store("sy-last-order", { ref: ref, total: total, items: lines.map(function (l) { return { name: title(l.p), qty: l.qty, total: l.total }; }), name: details.name_first, email: details.email, at: new Date().toISOString() });

      var send = Promise.resolve();
      if (CFG.declarationEndpoint) {
        var payload = JSON.stringify({ ref: ref, total: total, items: lines.map(function (l) { return { slug: l.slug, qty: l.qty }; }), customer: details, declaration: decl });
        send = Promise.race([
          fetch(CFG.declarationEndpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: payload, keepalive: true }).catch(function () {}),
          new Promise(function (r) { setTimeout(r, 5000); })
        ]);
      }
      send.then(function () {
        var form = $("[data-payfast]");
        form.action = pf.sandbox ? "https://sandbox.payfast.co.za/eng/process" : "https://www.payfast.co.za/eng/process";
        form.innerHTML = fields.map(function (f) { return '<input type="hidden" name="' + f[0] + '" value="' + esc(String(f[1]).trim()) + '">'; }).join("");
        form.submit();
      });
    });

    show(1);
  }

  /* PayFast expects PHP urlencode(): spaces as +, uppercase hex, and !'()*~ escaped. */
  function pfEncode(v) {
    return encodeURIComponent(String(v).trim()).replace(/%20/g, "+").replace(/[!'()*~]/g, function (c) { return "%" + c.charCodeAt(0).toString(16).toUpperCase(); });
  }

  function ageFrom(d) {
    var now = new Date(), a = now.getFullYear() - d.getFullYear();
    if (now.getMonth() < d.getMonth() || (now.getMonth() === d.getMonth() && now.getDate() < d.getDate())) a--;
    return a;
  }
  /* South African ID: YYMMDD SSSS C A Z, Luhn checksum. Returns ISO date of birth when valid and 18+. */
  function checkSAID(id) {
    if (!/^\d{13}$/.test(id)) return false;
    var yy = +id.slice(0, 2), mm = +id.slice(2, 4), dd = +id.slice(4, 6);
    var cur = new Date().getFullYear() % 100, year = yy > cur ? 1900 + yy : 2000 + yy;
    var d = new Date(year, mm - 1, dd);
    if (d.getFullYear() !== year || d.getMonth() !== mm - 1 || d.getDate() !== dd) return false;
    var sum = 0;
    for (var i = 0; i < 13; i++) {
      var n = +id[12 - i];
      if (i % 2 === 1) { n *= 2; if (n > 9) n -= 9; }
      sum += n;
    }
    if (sum % 10 !== 0) return false;
    if (ageFrom(d) < 18) return false;
    return year + "-" + id.slice(2, 4) + "-" + id.slice(4, 6);
  }

  function initSignature(canvas) {
    var ctx = canvas.getContext("2d"), ink = false, drawing = false, last = null;
    function size() {
      var r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
      if (!r.width) return;
      var keep = ink ? canvas.toDataURL() : null;
      canvas.width = r.width * dpr; canvas.height = r.height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.lineWidth = 2.2; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = "#efe9df";
      if (keep) { var im = new Image(); im.onload = function () { ctx.drawImage(im, 0, 0, r.width, r.height); }; im.src = keep; }
    }
    function pos(e) { var r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
    canvas.addEventListener("pointerdown", function (e) { if (!canvas.width) size(); drawing = true; last = pos(e); canvas.setPointerCapture(e.pointerId); ctx.beginPath(); ctx.arc(last.x, last.y, 1.1, 0, Math.PI * 2); ctx.fillStyle = "#efe9df"; ctx.fill(); ink = true; });
    canvas.addEventListener("pointermove", function (e) {
      if (!drawing) return;
      var p = pos(e); ctx.beginPath(); ctx.moveTo(last.x, last.y); ctx.lineTo(p.x, p.y); ctx.stroke(); last = p; ink = true;
      $("[data-sig-err]").classList.remove("show");
    });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { canvas.addEventListener(t, function () { drawing = false; }); });
    new ResizeObserver(size).observe(canvas);
    return {
      hasInk: function () { return ink; },
      clear: function () { ctx.clearRect(0, 0, canvas.width, canvas.height); ink = false; },
      data: function () { return canvas.toDataURL("image/png"); }
    };
  }

  /* ---------------------------------------------------------------- thank-you page */
  var thanks = $("[data-thanks]");
  if (thanks) {
    var o = store("sy-last-order"), box = $("[data-thanks-summary]");
    if (o && box) {
      box.innerHTML = '<dl><dt>Order reference</dt><dd><strong>' + esc(o.ref) + "</strong></dd></dl>" +
        o.items.map(function (i) { return '<div class="sum-item"><span>' + i.qty + " x " + esc(i.name) + "</span><span>" + rand(i.total) + "</span></div>"; }).join("") +
        '<div class="sum-item"><span>Courier</span><span>' + rand(SHIP) + '</span></div><div class="sum-item"><strong>Total</strong><strong>' + rand(o.total) + "</strong></div>";
    } else if (box) { box.hidden = true; }
    store("sy-cart", null);
  }

  renderCart();
})();
