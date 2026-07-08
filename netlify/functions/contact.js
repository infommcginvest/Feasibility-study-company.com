/**
 * Netlify Function: POST /api/contact  (redirected to /.netlify/functions/contact)
 * Receives the site contact form and relays it via the Resend API to the
 * Feasibility Study Company inbox. Runs server-side, so the API key and the
 * destination address are never exposed to the browser.
 *
 * Required environment variables (set in Netlify: Site settings > Environment
 * variables, NOT in code):
 *   RESEND_API_KEY   Resend API key (starts with "re_")
 *   CONTACT_TO       Destination inbox, e.g. info@feasibility-study-company.com
 *   CONTACT_FROM     Verified sender, e.g. "Feasibility Study Company <inquiries@feasibility-study-company.com>"
 *
 * Firewall note: CONTACT_TO must be an FSC-domain address. Forward that inbox
 * to any downstream monitored mailbox at the email-provider level. Do not put
 * a downstream address here or in DNS.
 */

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return resp(405, { ok: false, error: "Method not allowed." }, { Allow: "POST" });
  }

  try {
    let data = {};
    try {
      data = JSON.parse(event.body || "{}");
    } catch (e) {
      return resp(400, { ok: false, error: "Malformed request." });
    }

    // Honeypot: real users never fill this. Silently accept and drop.
    if (data.company_website) {
      return resp(200, { ok: true });
    }

    const name = clean(data.name, 200);
    const email = clean(data.email, 254);
    const organization = clean(data.organization, 200);
    const projectType = clean(data.project_type, 100);
    const message = clean(data.message, 5000);

    if (!name || !email || !message) {
      return resp(400, { ok: false, error: "Please complete name, email, and message." });
    }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return resp(400, { ok: false, error: "Please enter a valid email address." });
    }

    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) {
      return resp(500, { ok: false, error: "Mail service is not configured." });
    }
    const to = process.env.CONTACT_TO || "info@feasibility-study-company.com";
    const from =
      process.env.CONTACT_FROM ||
      "Feasibility Study Company <inquiries@feasibility-study-company.com>";

    const subject = "New inquiry: " + name + (organization ? " (" + organization + ")" : "");

    const text =
      "New inquiry from the Feasibility Study Company website\n\n" +
      "Name: " + name + "\n" +
      "Email: " + email + "\n" +
      "Organization: " + (organization || "n/a") + "\n" +
      "Project type: " + (projectType || "n/a") + "\n\n" +
      "Message:\n" + message + "\n";

    const html =
      '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#111114;line-height:1.5">' +
      '<h2 style="font-size:17px;margin:0 0 14px">New inquiry from the website</h2>' +
      '<table style="border-collapse:collapse">' +
      row("Name", esc(name)) +
      row("Email", '<a href="mailto:' + esc(email) + '">' + esc(email) + "</a>") +
      row("Organization", esc(organization || "n/a")) +
      row("Project type", esc(projectType || "n/a")) +
      "</table>" +
      '<p style="margin:16px 0 6px;font-weight:bold">Message</p>' +
      '<p style="white-space:pre-wrap;margin:0">' + esc(message) + "</p>" +
      "</div>";

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + apiKey,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: from,
        to: [to],
        reply_to: email,
        subject: subject,
        text: text,
        html: html,
      }),
    });

    if (!res.ok) {
      const detail = await res.text().catch(() => "");
      console.log("Resend error", res.status, detail);
      return resp(502, {
        ok: false,
        error: "Your inquiry could not be sent. Please email info@feasibility-study-company.com.",
      });
    }

    return resp(200, { ok: true });
  } catch (err) {
    console.log("contact function error", err && err.message);
    return resp(500, {
      ok: false,
      error: "Server error. Please email info@feasibility-study-company.com.",
    });
  }
};

function clean(v, max) {
  if (typeof v !== "string") return "";
  return v.trim().slice(0, max);
}
function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
function row(label, value) {
  return (
    '<tr><td style="padding:4px 16px 4px 0;color:#6b6b6b;vertical-align:top">' +
    label +
    '</td><td style="padding:4px 0;color:#111114">' +
    value +
    "</td></tr>"
  );
}
function resp(statusCode, obj, extraHeaders) {
  return {
    statusCode: statusCode,
    headers: Object.assign({ "Content-Type": "application/json" }, extraHeaders || {}),
    body: JSON.stringify(obj),
  };
}
