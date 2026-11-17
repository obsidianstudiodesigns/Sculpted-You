/* Sculpted You site settings.
   PayFast: these are PayFast's PUBLIC sandbox test credentials, so the full checkout can be tried without real money.
   Going live: replace merchantId and merchantKey with the client's live values and set sandbox to false, only
   after PayFast has approved the account in writing. Never put a live passphrase in this public file: when a
   passphrase is needed, signing and the ITN notify_url move to a small server function (see BUILD-PLAN.md, section 7).
   declarationEndpoint: an HTTPS endpoint that receives each signed declaration (JSON POST). Leave empty until the
   secure endpoint exists; the declaration is then shown on the review step and kept with the order reference only. */
window.SY_CONFIG = {
  payfast: {
    sandbox: true,
    merchantId: "10000100",
    merchantKey: "46f0cd694581a",
    // The shared sandbox merchant has a passphrase we don't know, so requests to it go unsigned (PayFast accepts that).
    // With the client's own account: set a passphrase in the PayFast dashboard and sign on a server, never here.
    sign: false,
    passphrase: "",
    notifyUrl: ""
  },
  shipping: 100,
  termsVersion: "2026-11-17",
  declarationEndpoint: ""
};
