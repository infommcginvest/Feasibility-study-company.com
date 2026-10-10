# Site-wide byline and signature: spec

One author record drives every byline, signature block and `author` JSON-LD node on the site. Change the record once and every page updates.

## 1. Author record

File: `src/data/authors/mark-otava.json` (adjust the path to the site's data folder).

```json
{
  "id": "mark-otava",
  "name": "Mark Otava",
  "role": "Principal, Market Research",
  "profile_url": "/the-practice/#who-stands-behind-the-research",
  "person_id": "https://feasibility-study-company.com/#mark-otava",
  "bio_short": "",
  "credentials": [
    { "abbr": "Ph.D.", "name": "", "issuer": "", "verify_url": "" },
    { "abbr": "MAI",   "name": "MAI designation", "issuer": "Appraisal Institute", "verify_url": "" },
    { "abbr": "CCIM",  "name": "CCIM designation", "issuer": "CCIM Institute", "verify_url": "" }
  ],
  "same_as": []
}
```

**Display rule (enforced in the template, not by hand):** a credential renders only when its `verify_url` is a live public link: a university repository or ProQuest record for the degree, the Appraisal Institute directory for the MAI, the CCIM directory for the CCIM, and the ASC National Registry for any state license. With empty URLs the byline reads "Mark Otava, Principal, Market Research". Once the links are filled in it reads as the name followed by each verified abbreviation, with each abbreviation linked to its record. [Example REDACTED IN THIS COPY under charter constraint 2; the owner's original has sha256 5407cfb3902236ff7043f50635ffebf358a76212a139d2f609855e66921b0b45.]

```js
// pseudo-code for the template
const shown = author.credentials.filter(c => c.verify_url && c.verify_url.startsWith("https://"));
const suffix = shown.map(c => c.abbr).join(", ");
const displayName = suffix ? `${author.name}, ${suffix}` : author.name;
```

## 2. Where it appears

| Page type | Placement | Text |
|---|---|---|
| Homepage | Under the hero, one line | "Research directed by {displayName}" linking to the profile |
| Case studies | `{{byline}}` under the H1; `{{signature}}` after the related links | Byline: "Market analysis by {displayName} · Published {date_published} · Data as of {data_as_of}". Signature: see section 3 |
| Research notes and articles | Byline under the H1; signature at the end | Same as case studies |
| Asset-class landing pages | Line above the sources list | "Methodology and market data reviewed by {displayName} · Updated {date_modified}" |
| Practice-area pages | Line above the sources list | Same as asset-class pages |
| Analytical framework and methodology pages | Byline under the H1 | "Written by {displayName}" |
| State and metro pages | Line above the sources list | "Market data reviewed by {displayName} · Updated {date_modified}" |
| About / The Practice | "Who stands behind the research" section | Full name, role, credentials table with verify links |

## 3. Signature block (case studies, research notes, methodology)

```html
<aside class="signature" aria-label="Signed by">
  <p class="signature__name"><a href="{profile_url}">{displayName}</a></p>
  <p class="signature__role">{role}, Feasibility Study Company</p>
  <p class="signature__note">The market conclusion on this page is signed by the principal. Every figure is sourced and dated in the list above. Worked cases are representative examples built from public data, not client engagements.</p>
</aside>
```

## 4. JSON-LD on every bylined page

```json
"author": { "@type": "Person", "@id": "https://feasibility-study-company.com/#mark-otava", "name": "Mark Otava" },
"publisher": { "@id": "https://feasibility-study-company.com/#org" }
```

The single Person node, with `hasCredential` filled only from verified entries, lives on the About page. Every other page references it by `@id`.

## 5. Before launch

- [ ] Fill `verify_url` for each credential from the issuing body's public directory, then confirm every link opens.
- [ ] Add the documented bio facts (`bio_short`) and replace the [VERIFY] and [BIO] slots on the About page.
- [ ] Add a professional headshot at `/img/mark-otava.jpg` and reference it in the Person node.
- [ ] Add any public profiles (LinkedIn, directory listings) to `same_as`.
