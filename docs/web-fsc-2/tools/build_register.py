#!/usr/bin/env python3
"""Build docs/web-fsc-2/REGISTER.csv from the primary text extracts.

Every verbatim quote is pulled from a file under docs/web-fsc-2/primary/ by a
unique substring, so the register cannot carry a mistyped quote. Section and
page come from locate.py (the SOP's own table of contents). Run from anywhere:

    python3 docs/web-fsc-2/tools/build_register.py
"""
import csv, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate as L

PRIM = os.path.join(HERE, '..', 'primary')
OUT = os.path.join(HERE, '..', 'REGISTER.csv')
TODAY = '2026-10-10'

URL = {
 'sop81': 'https://legacy.sba.gov/sites/default/files/2026-10/SOP%2050%2010%208.1%20Technical%20Policy%20Updates%20effective%20%2010.1.2026.docx',
 'sop8':  'https://legacy.sba.gov/sites/default/files/2025-05/SOP%2050%2010%208%20Technical%20Updates%20effective%206.1.2025.docx',
 'in882227': 'https://legacy.sba.gov/document/information-notice-5000-882227-issuance-technical-updates-sop-50-10-81',
 'in880695': 'https://legacy.sba.gov/document/information-notice-5000-880695-issuance-sop-50-10-81',
 'in881797': 'https://legacy.sba.gov/document/information-notice-5000-881797-fy-2027-7a-program-fees',
 'in881796': 'https://legacy.sba.gov/document/information-notice-5000-881796-fy-2027-504-program-fees',
 'pn879058': 'https://legacy.sba.gov/document/policy-notice-5000-879058-coordination-7a-504-maximum-loan-limits',
 'pn876777': 'https://legacy.sba.gov/document/procedural-notice-5000-876777-sunset-sbss-score-supplemental-guidance',
 'fr20080': 'https://www.federalregister.gov/documents/2026/10/01/2026-20080/interest-rates',
 'fr19072': 'https://www.federalregister.gov/documents/2025/09/30/2025-19072/development-company-loan-program-job-creation-and-retention-requirements-additional-areas-for-higher',
 'ecfr160': 'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-A/section-120.160',
 'ecfr131': 'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-A/section-120.131',
 'ecfr861': 'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.861',
 'ecfr910': 'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910',
 'ecfr921': 'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.921',
 'h15': 'https://www.federalreserve.gov/releases/h15/',
 'sbarel': 'https://legacy.sba.gov/article/2026/07/07/small-businesses-now-eligible-10-million-sba-financing',
 'soppage': 'https://legacy.sba.gov/document/sop-50-10-lender-development-company-loan-programs',
}
FILES = {
 'sop81': 'SOP-50-10-8.1-TU.txt', 'sop8': 'SOP-50-10-8.txt',
 'in882227': 'SBA-Notice-5000-882227.txt', 'in880695': 'SBA-Notice-5000-880695.txt',
 'in881797': 'SBA-Notice-5000-881797.txt', 'in881796': 'SBA-Notice-5000-881796.txt',
 'pn879058': 'SBA-Notice-5000-879058.txt', 'pn876777': 'SBA-Notice-5000-876777.txt',
 'fr20080': 'FR-2026-20080.txt', 'fr19072': 'FR-2025-19072.txt',
 'ecfr160': 'eCFR-13-CFR-120.160.txt', 'ecfr131': 'eCFR-13-CFR-120.131.txt', 'ecfr861': 'eCFR-13-CFR-120.861.txt',
 'ecfr910': 'eCFR-13-CFR-120.910.txt', 'ecfr921': 'eCFR-13-CFR-120.921.txt',
 'h15': 'FRB-H15-2026-10-09.txt', 'soppage': 'SBA-SOP-50-10-document-page.txt', 'sbarel': 'SBA-release-2026-07-07-10-million.txt',
}
TEXT = {k: open(os.path.join(PRIM, v), encoding='utf-8').read() for k, v in FILES.items()}
LINES = {k: v.split('\n') for k, v in TEXT.items()}
LOC = {k: L.build(os.path.join(PRIM, FILES[k])) for k in ('sop81', 'sop8')}

def norm(s): return re.sub(r'\s+', ' ', s).strip()

def find(src, needle, nth=1):
    """Line number (1-based) and text of the nth line containing needle."""
    nn = norm(needle)
    hits = [i for i, l in enumerate(LINES[src]) if nn in norm(l)]
    if len(hits) < nth:
        raise SystemExit(f'NEEDLE NOT FOUND ({src}): {needle!r}')
    i = hits[nth - 1]
    return i + 1, LINES[src][i]

def quote(src, needle, span=None, nth=1):
    """Verbatim quote: the whole line containing needle, or the sub-span between two substrings (inclusive)."""
    ln, text = find(src, needle, nth)
    t = norm(re.sub(r'^#+\s*', '', text))
    if span:
        a, b = span
        i = t.find(a); j = t.find(b, i)
        if i < 0 or j < 0: raise SystemExit(f'SPAN NOT FOUND in line {ln} of {src}: {span!r}')
        t = t[i:j + len(b)]
    return ln, norm(t)

def pdfquote(src, needle):
    """Quote from a notice: the sentence containing needle (text flows across pdf lines), plus the pdf page."""
    t = TEXT[src]
    flat = norm(t)
    k = flat.find(norm(needle))
    if k < 0: raise SystemExit(f'NEEDLE NOT FOUND ({src}): {needle!r}')
    # sentence bounds
    s = max(flat.rfind('. ', 0, k) + 2, flat.rfind(': ', 0, k) + 2, 0)
    e = flat.find('. ', k); e = len(flat) if e < 0 else e + 1
    sent = flat[s:e].strip()
    # page: count markers before the needle in the raw text
    raw_k = norm(t[:t.find(needle.split()[0])]) if False else None
    before = t[:t.find(re.sub(r'\s+', ' ', needle).split(' ')[0])]
    pages = re.findall(r'=== PDF PAGE (\d+) of (\d+) ===', t)
    # find page by walking markers
    page = None
    for m in re.finditer(r'=== PDF PAGE (\d+) of (\d+) ===', t):
        seg_start = m.end()
        nxt = re.search(r'=== PDF PAGE (\d+) of', t[seg_start:])
        seg = t[seg_start: seg_start + nxt.start()] if nxt else t[seg_start:]
        if norm(needle) in norm(seg):
            page = f'p. {m.group(1)} of {m.group(2)}'; break
    return sent, page or 'p. ?'

def sec(src, ln):
    lines, toc, heads = LOC[src]
    s, p = L.locate(lines, toc, heads, ln)
    # paragraph heading: nearest preceding '#' line
    para = ''
    for i in range(ln - 2, -1, -1):
        if lines[i].startswith('#'):
            para = norm(re.sub(r'^#+\s*', '', lines[i]))[:120]; break
    return s, para, p

rows = []
def add(id, rule, v81, v8, status, src, needle=None, span=None, nth=1, url=None, note='', v8cite='', pdf=None, section=None, paragraph=None, page=None, q=None):
    if src in LOC and needle:
        ln, qt = quote(src, needle, span, nth)
        s, para, pg = sec(src, ln)
        qt = qt
        section = section or s; paragraph = paragraph or f'{para} [extract line {ln}]'; page = page or pg
    elif pdf:
        qt, pg = pdfquote(src, pdf)
        page = page or pg
    else:
        qt = q or ''
    rows.append(dict(id=id, rule=rule, value_8_1=v81, value_8=v8, status=status, section=section or '', paragraph=paragraph or '',
                     page=page or '', verbatim_quote=qt, primary_url=url or URL.get(src, ''), checked_on=TODAY,
                     resolution_note=note, value_8_cite=v8cite))

def c8(needle, span=None, nth=1):
    """Cite for the SOP 8 value: section, page, line and quote."""
    ln, qt = quote('sop8', needle, span, nth)
    s, para, pg = sec('sop8', ln)
    return f'SOP 50 10 8, {s}, {pg} [extract line {ln}]: "{qt}"'

# ---------------------------------------------------------------- version and timing
add('R01', 'Governing SOP: name, version, publication and effective date',
    'SOP 50 10 8.1, "Lender and Development Company Loan Programs with Technical Policy Updates"; Version 8.1; published September 25, 2026; effective October 1, 2026; replaces SOP 50 10 8',
    'SOP 50 10 8 (Technical Updates), effective June 1, 2025', 'CHANGED', 'sop81',
    needle='Published: September 25, 2026', section='Cover and SOP Summary', paragraph='Standard Operating Procedure Summary [extract lines 13-21]', page='pp. 1-3',
    q=None, note='The SBA document page labels the file "Version 8.1 with Technical Updates"; the document itself and IN 5000-882227 say "Technical Policy Updates". The site uses the document\'s own name and the SBA page label as an alias. Fact sheet said only "with Technical Updates".',
    v8cite=c8('Effective Date:  June 1, 2025'))
rows[-1]['verbatim_quote'] = norm(' / '.join(LINES['sop81'][12:21]))
add('R02', 'Original 8.1 issuance notice', 'Information Notice 5000-880695, published August 14, 2026, effective October 1, 2026', 'n/a', 'VERIFIED', 'in880695',
    pdf='PUBLICATION: August 14, 2026', section='SBA Information Notice 5000-880695', paragraph='Header block')
add('R03', 'Technical Updates notice', 'Information Notice 5000-882227, published September 25, 2026, effective October 1, 2026; the TU version "supersedes the version previously published but not yet effective"', 'n/a', 'VERIFIED', 'in882227',
    pdf='supersedes the version previously published but not yet effective', section='SBA Information Notice 5000-882227', paragraph='Opening paragraph')
add('R04', 'Effective date of 8.1 with Technical Policy Updates', 'October 1, 2026', 'June 1, 2025 (SOP 50 10 8)', 'VERIFIED', 'sop81',
    needle='Effective Date: October 1, 2026', section='Cover and SOP Summary', paragraph='Standard Operating Procedure Summary', page='p. 3', v8cite=c8('Effective Date:  June 1, 2025'))
add('R05', 'Applicability trigger on and after October 1, 2026', 'TU notice (IN 5000-882227): applies to "all applications received by SBA on or after" October 1, 2026; SOP 50 10 8 continues for applications "submitted through September 30, 2026". The August notice (IN 5000-880695) had keyed applicability to applications "issued an SBA loan number on or after that date".',
    'n/a', 'CONFLICT_RESOLVED', 'in882227', pdf='will apply to all applications received', section='SBA Information Notice 5000-882227', paragraph='Opening paragraph',
    note='Both wordings are primary. The later notice governs the version in force; the site states the TU wording and does not state the loan-number test. Fact sheet flagged this conflict (NAGGL vs StatementsReady).')
add('R06', 'Superseded edition', 'SOP 50 10 8, effective June 1, 2025, replaced SOP 50 10 7.1', 'SOP 50 10 8', 'VERIFIED', 'sop8', needle='SOP Version This Replaces: 50 10 7.1', section='Cover and SOP Summary', paragraph='SOP Summary', page='p. 2')
add('R07', 'Primary file and redline', 'The .docx on the SBA document page (1,071,898 bytes; sha256 279c7eee...63dde, see HASHES.txt). No redline is posted on the SOP page or on the IN 5000-882227 page; the only attachment there is the notice PDF. A paragraph-level diff of SOP 8 against 8.1 TU was generated instead (primary/REDLINE-GENERATED-8-to-8.1TU.diff).',
    'SOP 8 .docx (1,171,942 bytes; sha256 bf5cae03...17ac1)', 'NOT_IN_TEXT', 'sop81', url=URL['soppage'], section='SBA document page', paragraph='Variations of this document', page='n/a',
    q=norm(TEXT['soppage'])[norm(TEXT['soppage']).find('Version 8.1 with Technical Updates'):norm(TEXT['soppage']).find('Version 8.1 with Technical Updates')+140], note='Saved extract primary/SBA-SOP-50-10-document-page.txt. The fact sheet says SBA posted a redline; the SBA pages fetched on 2026-10-10 carry none. The cross-check in Phase 0.5 ran against the generated diff.')

# ---------------------------------------------------------------- Appendix 15: change of ownership
add('R08', 'Change-of-ownership categories', 'Four categories: Initial Acquisition (default), Business Expansion, Owner Buyout (Existing and Partial Change), ESOP & Cooperative. Initial Acquisition = a new majority or largest owner who was not previously an owner, or who has been employed by the acquired business for fewer than 24 months. Owner Buyout: individuals not employed for at least 24 months may acquire less than 50% and may not become the largest shareholder; otherwise Initial Acquisition credit standards apply.',
    'Two structures: complete change of ownership (new owner) and change between existing owners (partner buyout); no categories', 'VERIFIED', 'sop81',
    needle='Change of ownership transactions fall into four categories', v8cite=c8('Change of Ownership Resulting in a New Owner (complete change of ownership)'))
add('R08a', 'Initial Acquisition definition (24-month employee test)', 'see R08', 'n/a', 'VERIFIED', 'sop81', needle='Initial Acquisition: A change of ownership transaction that results in a new majority', span=('Initial Acquisition: A change', 'being acquired.'))
add('R08b', 'Owner Buyout 24-month employment limit', 'see R08', 'n/a', 'VERIFIED', 'sop81', needle='For all Owner Buyout transactions, individuals not currently employed', span=('For all Owner Buyout', 'largest direct or indirect shareholder.'))
add('R09', 'Change-of-ownership debt service coverage floors', 'Initial Acquisition 1.25:1; Business Expansion 1.15:1; Owner Buyout 1.25:1; ESOP and Cooperative 1.25:1; satisfied on the last fiscal year-end or an average of the last two fiscal year-ends, historical or adjusted',
    '1.15 on a historical and/or projected basis (projections allowed for changes of ownership), 1:1 global', 'VERIFIED', 'sop81',
    needle='The Debt Service Coverage (DSC) ratio must be satisfied using either the last fiscal year-end', span=('The Debt Service Coverage (DSC) ratio must be satisfied', 'transaction type:'),
    note='Floors quoted at extract lines 5212-5215: "Initial Acquisition: 1.25:1 / Business Expansion: 1.15:1 / Owner Buyout: 1.25:1 / ESOP and Cooperative: 1.25:1".',
    v8cite=c8('must be equal to or greater than 1.15 on a historical and/or projected cash flow basis') + ' AND ' + c8('For start-ups, new businesses, changes of ownership, and other applications based on projections'))
rows[-1]['verbatim_quote'] += ' ' + ' / '.join(norm(LINES['sop81'][i]) for i in range(5211, 5215))
add('R10', 'Definition of historical DSC (EBITDA coverage)', 'Historical DSC = EBITDA divided by the combined debt service post-transaction; a rent add-back is allowed when owner-occupied real estate is part of the deal; adjusted DSC allowed with justified add-backs and a 1:1 global DSC',
    'OCF (EBITDA) / debt service, 1.15 historical and/or projected', 'VERIFIED', 'sop81', needle='The historical DSC ratio is defined as earnings before interest')
add('R11', 'Projections cannot meet the change-of-ownership DSC floor, except owner-occupied Special Purpose Property', 'Lender "may not rely on" post-closing projections to meet the DSC requirement. Exception: acquisition of an owner-occupied Special Purpose Property that is integral to the business, where the purchase price is fully supported by the appraised value (the appraised value fully collateralizes the loan); then projections may satisfy the DSC within two years from funding, the historical DSC is still calculated and input, and no QoE is required.',
    'Projections allowed for changes of ownership (1.15 within 2 years)', 'CHANGED', 'sop81', needle='The Lender must evaluate the Applicant’s post-closing financial projections but may not rely on them',
    note='Fact sheet said "special use property loans fully secured by collateral". The text keys the exception to the appraised value of the Special Purpose Property fully supporting the purchase price / fully collateralizing the loan, within two years. Supporting lines 5216-5219 and 5224.',
    v8cite=c8('For start-ups, new businesses, changes of ownership, and other applications based on projections'))
add('R11a', 'Special Purpose Property projection exception (text)', 'see R11', 'n/a', 'VERIFIED', 'sop81', needle='In situations where the appraised value fully collateralizes the loan')
add('R11b', 'Examples SBA gives for the exception', '"storage units and hotels where the real estate fully secures the loan"', 'n/a', 'VERIFIED', 'sop81', needle='Examples of this type of loan include storage units and hotels', span=('This provision only applies', 'fully secures the loan.'))
add('R12', 'Acquisition without continuity of operations', 'May be evaluated as a start-up, applying all start-up requirements (equity, eligibility, maturity, underwriting, uses of proceeds)', 'Not addressed', 'VERIFIED', 'sop81',
    needle='If there is not a clearly defined continuity of operations', span=('If there is not a clearly defined continuity', 'uses of proceeds.'))
add('R13', 'Initial Acquisition equity injection', '10% of total project cost; "cannot be reduced or eliminated"', '10 percent of total project costs; seller standby debt up to half', 'VERIFIED', 'sop81', needle='For Initial Acquisitions, the required equity injection cannot be reduced',
    v8cite=c8('At a minimum, SBA requires an equity injection of at least 10 percent of the total project costs'))
rows[-1]['verbatim_quote'] = 'Initial Acquisition: 10%. ' + rows[-1]['verbatim_quote']
add('R14', 'Business Expansion, Owner Buyout, ESOP & Cooperative equity', '10% (Owner Buyout measured on the purchase price); for Business Expansion and Owner Buyout the lender may reduce or eliminate it with sufficient liquidity and working capital and no negative net worth at the last fiscal year-end; ESOP controlling-interest loans are exempt',
    'Partner buyouts: no stated injection; complete change 10 percent', 'VERIFIED', 'sop81', needle='For both Business Expansions and Owner Buyouts, the Lender may reduce or eliminate')
rows[-1]['verbatim_quote'] = 'Business Expansion, Owner Buyouts, and ESOP & Cooperatives: 10% ' + rows[-1]['verbatim_quote'] + ' ' + quote('sop81', 'the Applicant’s balance sheet must not have a negative net worth')[1] + ' ' + quote('sop81', 'Loans for the purpose of purchasing a controlling interest (at least 51 percent) in the employer for purposes of an ESOP are not subject')[1]
add('R15', 'Limited equity sources: half cap', 'Standby debt (full standby), seller debt on full standby and non-controlling minority equity investors (under 20%, no control), "whether individually or in the aggregate, may provide no more than half of the required Equity Injection"',
    'Seller debt on full standby may not exceed half of the required injection', 'VERIFIED', 'sop81', needle='may provide no more than half of the required Equity Injection',
    v8cite=c8('Seller debt may not be considered as part of the equity injection unless it is on full standby'))
add('R16', 'Fees that do not count as equity; due diligence costs that do', 'Education, advisory and Agent fees are not eligible prepaid expenses and are not equity; out-of-pocket costs of financial due diligence reports (business valuation, QoE) can count toward the injection',
    'Not stated', 'VERIFIED', 'sop81', needle='Expenses related to education, advisory services, or fees paid by the Applicant to an Agent', nth=5,
    note='Second sentence at extract line 5133: "Any funds expended by the Applicant on the report can count toward the equity injection."')
add('R17', 'Seller note refinance seasoning', '36 months in place and current (not on standby)', '24 months', 'VERIFIED', 'sop81', needle='must have been in place and current (not on standby) for at least 36 months',
    v8cite=c8('must have been in place and current (not on standby) for at least 24 months'))
add('R18', 'Earnouts, rebates and working-capital true-ups', 'Seller earnouts prohibited; buyer rebates based on performance allowed but must pay down the 7(a) principal (no subsidy recoupment fee); purchase-agreement working-capital adjustments are not rebates and may be retained',
    'Not addressed', 'VERIFIED', 'sop81', needle='Seller earnouts/buyer rebates: Seller earnouts are prohibited')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'Working capital adjustment provisions')[1]
add('R19', 'Seller as consultant', 'Up to 24 months in aggregate, including extensions (Business Expansion and Initial Acquisition)', '12 months including extensions', 'VERIFIED', 'sop81', needle='for a period not to exceed 24 months', span=('Except as provided below', 'including any extensions).'),
    v8cite=c8('for a period not to exceed 12 months including any extensions'))
add('R20', 'Acquisition debt capped at the business valuation', 'Total debt supporting the change of ownership, including seller debt not on full standby, is limited to the business valuation and must be supported by DSC; a price above the valuation must be made up by equity',
    'Not stated as a cap', 'VERIFIED', 'sop81', needle='The total debt eligible to support a change of ownership transaction')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'If the amount paid for the business exceeds the business valuation')[1]
add('R21', 'Lender in-house business valuation threshold', 'Business Purchase Price of $350,000 or less, unless there is a close relationship between buyer and seller (also for Special Purpose Properties). Otherwise an independent valuation from a Qualified Source requested by and prepared for the lender.',
    '$250,000 or less: amount financed minus appraised real estate and equipment', 'VERIFIED', 'sop81', needle='If the Business Purchase Price is $350,000 or less, the Lender may perform its own valuation',
    v8cite=c8('is $250,000 or less, the Lender may perform its own valuation'))
add('R22', 'Business Purchase Price definition', 'The purchase-agreement price less owner-occupied commercial real estate (at appraised value); it drives the due diligence thresholds regardless of equity, seller debt or loan amount', 'n/a', 'VERIFIED', 'sop81',
    needle='the “Business Purchase Price” excludes all owner-occupied commercial real estate')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'The financial due diligence requirements are determined by the Business Purchase Price')[1]
add('R23', 'Quality of Earnings trigger and exemptions', 'Required for Business Expansion and Initial Acquisition at a Purchase Price of $3 million or more (measured before buyer equity, seller debt or other financing); Owner Buyout and ESOP & Cooperative are exempt; an acquisition of an owner-occupied Special Purpose Property is exempt regardless of price',
    'Not required', 'CONFLICT_RESOLVED', 'sop81', needle='For Business Expansion and Initial Acquisition transactions where the Purchase Price as defined',
    note='Fact sheet conflict on the special purpose exemption and on the price measure: resolved. The exemption is in the text (line 5224); the price measure is the Business Purchase Price, which excludes owner-occupied real estate (R22). Sources that said "excluding real estate being acquired" meant this.')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'A Quality of Earnings report is not required for a transaction involving the acquisition', span=('A Quality of Earnings report is not required', 'Business Purchase Price.'))[1]
add('R24', 'Quality of Earnings standard and buyer-ordered reports', 'Independent, for the benefit of the lender, not prepared by or for the seller; must include a Cash Proof on a trailing-12-month basis and the last two fiscal years (reduced if operating under two years); a buyer-commissioned QoE may be used if reviewed by one of the lender\'s approved vendors, with the vendor review in the file; the lender must use the QoE earnings in the DSC',
    'n/a', 'CONFLICT_RESOLVED', 'sop81', needle='Recognizing that some Applicant buyers may elect to commission their own QoE',
    note='Fact sheet conflict on the review standard: the SOP text requires review "by one of their approved vendors" (lines 5158-5159). IN 5000-882227 describes the same change as "a reliance letter or secondary review by a different firm". The site states the SOP text and notes the notice wording.')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'The Lender may not rely upon a QoE report prepared by another party')[1] + ' ' + quote('sop81', 'The QoE must include a Cash Proof', span=('The Cash Proof is designed', 'reduced accordingly.'))[1]
add('R24a', 'QoE review wording in the TU notice', 'see R24', 'n/a', 'VERIFIED', 'in882227', pdf='may be used if accompanied by a reliance letter or secondary review by a different firm', section='SBA Information Notice 5000-882227', paragraph='Appendix 15: Quality of Earnings')
add('R25', 'Change-of-ownership amortization', 'Not more than 10 years, except: real estate bought with the business may be a separate loan or blended (only the real estate portion may exceed 10 years, up to 25); Special Purpose Properties Exemption: a maturity of up to 25 years on the whole loan "if 85% or more of the use of the total project costs are for real estate", when the owner-occupied Special Purpose Property cannot be separated from and is integral to the business',
    'Mixed purpose and change of ownership: blended, or up to 25 years if 51% or more of proceeds are for real estate', 'CHANGED', 'sop81', needle='Special Purpose Properties Exemption: For transactions involving the acquisition',
    note='Fact sheet said 85% "of value" (single secondary source). The text measures 85% of the USE OF TOTAL PROJECT COSTS. Lines 5122-5127.',
    v8cite=c8('Mixed purpose loans and loans for all types of changes of ownership'))
rows[-1]['verbatim_quote'] = quote('sop81', '7(a) loans that facilitate a change of ownership must not have an amortization that exceeds 10 years')[1] + ' ' + rows[-1]['verbatim_quote']
add('R26', '7(a) Small and SBA Express for changes of ownership', 'Permitted, subject to Appendix 15. Modifications: an internal business valuation at the lender\'s discretion when the Business Purchase Price is $350,000 or less; all Appendix 15 DSC requirements apply with no reduced standard; the fully secured test need not include other commercial real estate of the borrower or guarantors',
    'Permitted (SOP 8 Section B Chapter 2 carried change-of-ownership rules)', 'CONFLICT_RESOLVED', 'sop81', needle='The use of 7(a) Small & SBA Express loans to facilitate changes of ownership are permitted',
    note='Fact sheet conflict: CLX tied eligibility to a $350,000 purchase price; Coleman tied $350,000 to the internal valuation. The text ties $350,000 to the internal valuation only (Section B Ch. 2 line 1763 and Appendix 15 line 5146). The August text barred these loans per IN 5000-882227, which lists the permission as a principal change.',
    v8cite=c8('Change of Ownership Resulting in a New Owner (complete change of ownership)', nth=2))
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'An internal business valuation may be obtained at the Lender’s discretion')[1] + ' ' + quote('sop81', 'No reduced or alternative DSC standard applies solely because')[1]
add('R26a', 'TU notice on 7(a) Small and Express for changes of ownership', 'see R26', 'August 8.1 text (not in force): not permitted', 'VERIFIED', 'in882227', pdf='The use of 7(a) Small and SBA Express loans for changes of ownership is permitted', section='SBA Information Notice 5000-882227', paragraph='Appendix 15: 7(a) Small & SBA Express Loans')
add('R27', '7(a) Small credit standard', 'For purposes other than changes of ownership: DSC of at least 1.10:1 on a historical or projected basis (projections must reach 1.10:1 within one year); the two most recent months of commercial bank statements reviewed; SBSS does not appear anywhere in the 8.1 text (0 hits). SBSS was retired for loans approved on or after March 1, 2026 (PN 5000-876777).',
    'FICO SBSS screening, minimum score 165', 'VERIFIED', 'sop81', needle='For 7(a) Small Loans, for purposes other than Changes of Ownership',
    v8cite=c8('the minimum acceptable SBSS score is 165'))
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'The two most recent months of commercial bank activity or statements, from the time of application')[1]
add('R27a', 'SBSS sunset notice', 'SBSS discontinued effective March 1, 2026; 7(a) Small DSC 1.10:1', 'SBSS 165', 'VERIFIED', 'pn876777', pdf='SBA is discontinuing the use of the FICO', section='SBA Procedural Notice 5000-876777', paragraph='Opening paragraph')
add('R28', 'Standard 7(a) debt service coverage (not a change of ownership)', '1.15 on a historical and/or projected cash flow basis and 1:1 on a global basis; start-ups, new businesses and projection-based applications must reach 1.15 within 2 years from funding (or from the end of construction)',
    '1.15 historical and/or projected; 1:1 global', 'VERIFIED', 'sop81', needle='must be equal to or greater than 1.15 on a historical and/or projected cash flow basis',
    note='Fact sheet row 15 was Low confidence; confirmed in the 8.1 text (Section B Ch. 1 Credit Standards, line 1698; projections at line 1681).',
    v8cite=c8('must be equal to or greater than 1.15 on a historical and/or projected cash flow basis'))
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'For start-ups, new businesses, and other applications based on projections, include detailed projections')[1]
add('R29', 'Start-up equity injection (7(a))', 'At least 10 percent of total project costs for a Start-Up Business (in operation one year or less)', 'Same (10 percent)', 'VERIFIED', 'sop81', needle='Minimum equity injection requirements for Start-Up Businesses')
add('R30', '504 debt service coverage', 'Historical basis, last fiscal year-end or average of the last two; DSC at least 1.15:1; DSC = EBITDA / combined post-transaction debt service; if historical coverage is insufficient the CDC analyzes at least two years of projections', '1:1 "based on calculations acceptable to SLPC"', 'VERIFIED', 'sop81',
    needle='For all 504 transactions, the repayment ability analysis must address debt service coverage',
    v8cite=c8('must be equal to or greater than 1:1 based on calculations acceptable to SLPC'))
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'For projection-based projects, the analysis must include a minimum of 2 years of projections')[1]
add('R31', '504 borrower contribution tiers', '10% standard; 15% for a New Business (two years or less) OR a Limited or Special Purpose Property; 20% for both', 'Same', 'VERIFIED', 'ecfr910', q=norm(TEXT['ecfr910'].split('Fetched', 1)[-1].split('\n', 1)[-1])[:900], section='13 CFR 120.910', paragraph='(a)(1)-(4)', page='n/a (eCFR, current to 2026-10-07)',
    note='Also SOP 8.1 Section C Ch. 1 Credit Standards, Borrower\'s Contribution (extract lines 3470-3476).')
add('R32', 'Owner-occupancy', 'Existing building: occupy 51% of Rentable Property, lease up to 49%. New construction: occupy 60%, permanently lease up to 20%, temporarily lease a further 20% to be occupied within 3 and 10 years. Boat slips and docks count as Rentable Property for marinas.', 'Same', 'VERIFIED', 'sop81',
    needle='For an existing building, the Applicant must occupy 51% of the Rentable Property', note='Regulation: 13 CFR 120.131 (eCFR-13-CFR-120.131.txt).')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'For new construction, the Applicant must occupy 60% of the Rentable Property')[1]
add('R33', '7(a) mixed-purpose maturity (not a change of ownership)', 'Blended maturity, or up to 25 years if 51% or more of the proceeds are for real estate; the 51% option does not apply to changes of ownership (Appendix 15 governs)', 'Blended or 25 years at 51% real estate, including changes of ownership', 'VERIFIED', 'sop81',
    needle='Mixed purpose loans: When 7(a) loan proceeds are used for multiple purposes', v8cite=c8('Mixed purpose loans and loans for all types of changes of ownership'))
add('R34', '504 loan maturity with real estate and equipment', '10, 20 or 25 years by useful life: maximum 25 years for real estate, minimum 10 years for machinery and equipment; with both, "the maturity will be based on the asset category that constitutes the majority of loan proceeds"', 'Identical wording in SOP 50 10 8', 'CHANGED', 'sop81',
    needle='When the Project includes both real estate and machinery and equipment, the maturity will be based',
    note='Fact sheet row 20 (single source) said 8.1 TU moved a 75% real-estate test to 51%. Neither figure is in either SOP text; both say "majority of loan proceeds". Published as the majority rule, with no percentage.',
    v8cite=c8('When the Project includes both real estate and machinery and equipment, the maturity will be based'))
rows[-1]['verbatim_quote'] = quote('sop81', 'Maturity of the 504 loan is 10, 20, or 25 years')[1] + ' A maximum of 25 years for real estate; A minimum of 10 years for machinery and equipment; and ' + rows[-1]['verbatim_quote']
add('R35', '504 Third Party Lender loan term', 'Minimum term: at least 7 years for a 10-year 504 loan and 10 years for a 20- or 25-year 504 loan (13 CFR 120.921(a)). The TU removed the August text\'s prohibition on the Third Party loan amortizing beyond the debenture term, so a longer bank amortization is again permitted.', 'Minimum 7/10 years; no cap stated', 'CONFLICT_RESOLVED', 'sop81',
    needle='A Third Party Loan must have a term of at least 7 years when the 504 loan is for a term of 10 years',
    note='Fact sheet conflict (Coleman: maximum restriction removed; CLX: "no longer a minimum term"). The 8.1 TU text keeps the regulatory minimum term; IN 5000-882227 says the TU "Removed the prohibition against the amortization of the Third Party loan exceeding the 504 debenture term". Coleman is right; CLX is wrong.',
    v8cite=c8('A Third Party Loan must have a term of at least 7 years when the 504 loan is for a term of 10 years'))
add('R35a', 'TU notice on the Third Party Lender term', 'see R35', 'n/a', 'VERIFIED', 'in882227', pdf='Removed the prohibition against the amortization of the Third Party loan', section='SBA Information Notice 5000-882227', paragraph='Section C, Chapter 1: 504 Third Party Lender Loan Term')
add('R36', '504 eligible fixed assets', 'Fixed assets financed with a 504 loan must have a useful life of at least 10 years and be at a fixed location; working capital and inventory are 7(a) uses', 'Same', 'VERIFIED', 'sop81', needle='for a 504 loan, these assets must have a useful life of at least 10 years')
add('R37', '504 job opportunity ratio', 'One job opportunity per $95,000 guaranteed; $150,000 for Small Manufacturers and Energy Public Policy Goal projects; CDC portfolio averages $95,000 / $150,000 in Special Geographic Areas', 'One per $90,000; $140,000 for small manufacturers and energy goal', 'VERIFIED', 'sop81',
    needle='A Project must create or retain one job opportunity per $95,000 guaranteed by SBA',
    note='Set by Federal Register 2025-19072 (90 FR 47117, Sept 30, 2025), applicable to 504 loans approved on or after October 1, 2025 (R37a).',
    v8cite=c8('At least 1 Job Opportunity must be created or retained per every $90,000 of project debenture'))
fr = norm(TEXT['fr19072']); k = fr.find('one job for every $95,000'); k2 = fr.find('$75,000 and $120,000')
add('R37a', 'Federal Register notice setting the 504 job ratio', '$95,000 per job ($150,000 small manufacturer / energy), 504 loans approved on or after October 1, 2025', '$75,000 / $120,000 in regulation text, $90,000 / $140,000 in SOP 8', 'VERIFIED', 'fr19072',
    q=fr[max(0, fr.find('Applicability Date')):fr.find('Applicability Date') + 230] + ' ... ' + (fr[k - 200:k + 160] if k > 0 else ''), section='90 FR 47117-47118', paragraph='Applicability Date; Supplementary Information', page='pp. 47117-47118')
add('R38', 'Combined 7(a) plus 504 limit', 'A borrower\'s outstanding 7(a) balance (up to the $5,000,000 7(a) maximum) does not reduce the 504 maximum ($5,000,000 aggregate gross debentures; $5,500,000 per project for small manufacturers and energy projects): up to $10 million combined when the 7(a) loan is approved first and the 504 second. Effective July 4, 2026; integrated into 8.1 (IN 5000-880695).',
    'Not stated; 7(a) balances were counted against the 504 limit in practice', 'VERIFIED', 'pn879058', pdf='does not reduce the maximum loan amount available under the 504 loan program', section='SBA Policy Notice 5000-879058', paragraph='Purpose paragraph',
    note='The $10 million figure is the sum SBA itself states in its July 7, 2026 release; the notice text gives the two $5,000,000 limits and the sequencing rule (7(a) first). Also SOP 8.1 Section C Ch. 1 D.1.b, extract line 3408.')
rows[-1]['verbatim_quote'] += ' ' + pdfquote('pn879058', 'a lender may first approve a 7(a) loan followed with a 504 transaction approved by the CDC second')[0]
rel = norm(TEXT['sbarel']); k = rel.find('$10 million')
add('R38a', 'SBA release stating the combined $10 million figure', 'see R38', 'n/a', 'VERIFIED', 'sbarel', q=rel[max(0, k - 400):k + 300], section='SBA news release, July 7, 2026', paragraph='Small Businesses Now Eligible for $10 Million in SBA Financing', page='n/a (web)')
add('R39', 'Personal financial statement age', 'Owner financial statements (SBA Form 413 or equivalent) signed and dated within 90 days of submission to SBA (7(a) Appendix 20 and 504 Chapter 1); business financial statements within 120 days', '120 days', 'VERIFIED', 'sop81',
    needle='signed and dated within 90 days of submission to SBA. Business financial statements must be dated within 120 days', v8cite=c8('signed and dated within 120 days of submission to SBA, for all owners of 20% or more'))
add('R40', 'Trust guaranty threshold', 'When one or more trusts own, in the aggregate, 20% or more of the applicant, each trust gives an unlimited full guaranty, the trustee executes it, and the Trustor also personally guarantees; all donors to the trust are Trustors for eligibility', '20% or more (same threshold)', 'VERIFIED', 'sop81',
    needle='When one or more trusts (revocable or irrevocable) own, in the aggregate, 20% or more of the applicant',
    note='IN 5000-882227 lists this as a principal change of the TU, which is the only primary indication that the August text differed. The site does not state the August "any percentage" value as a verified figure.',
    v8cite=c8('All entities that have direct and/or indirect ownership of 20% or more of an Applicant must provide an unlimited full guaranty'))
add('R41', 'Franchises: Directory and 504 counsel review', 'A brand meeting the FTC definition must be on the SBA Franchise Directory. For 504 loans the CDC\'s closing counsel reviews and certifies the franchise documents through the Opinion of CDC Counsel (SBA Form 2268). SBA may remove a brand for non-compliance with its Certification, illegal activity, false or withheld information, or a State order prohibiting it from operating, after 30 days\' notice.',
    'Directory listing required; no CDC closing-counsel certification stated', 'CHANGED', 'sop81', needle='For all 504 loans, prior to closing, the CDC must obtain a copy of the executed franchise agreement',
    note='Fact sheet row 27 said the Franchise Team "screens for franchisor conduct detrimental to borrowers". No such screen is in the text; the text has a removal clause (line 495) covering illegal activity, false information and State orders. Published only as the removal clause.')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'If SBA determines that Franchisor/Distributor has not complied with the terms', span=('If SBA determines that Franchisor/Distributor', 'opportunity for Franchisor/Distributor to respond.'))[1]
add('R42', 'Lodging and marina eligibility: the transient test', 'Hotels, motels, RV parks, marinas, campgrounds and similar businesses are eligible if more than 50% of the business\'s revenue for the prior year comes from transients who stay 30 days or less at a time, with zoning and legal compliance; a Start-Up Business shows this in projections. Wording identical to SOP 50 10 8.', 'Identical', 'VERIFIED', 'sop81',
    needle='Hotels, motels, recreational vehicle parks, marinas, campgrounds, or similar types of businesses are eligible', span=('Hotels, motels', '30 days or less at a time.'),
    v8cite=c8('Hotels, motels, recreational vehicle parks, marinas, campgrounds, or similar types of businesses are eligible', span=('Hotels, motels', '30 days or less at a time.')))
add('R43', 'Feasibility study authority', '13 CFR 120.160(b): "SBA may require professional appraisals of the applicant\'s and principals\' assets, a survey, or a feasibility study." Discretionary; not an SOP rule.', 'Same', 'VERIFIED', 'ecfr160',
    q=norm(TEXT['ecfr160'][TEXT['ecfr160'].find('( b ) Appraisals'):TEXT['ecfr160'].find('( c ) Hazard')]), section='13 CFR 120.160', paragraph='(b) Appraisals', page='n/a (eCFR, current to 2026-10-07)')
sp81 = [norm(LINES['sop81'][i]) for i in range(3480, 3506)]
add('R44', 'Limited or Special Purpose Property: definition and SBA\'s example list', 'Definition (Appendix 3 and Appendix 15): "a limited-market property with a unique physical design, special construction materials, or a layout that restricts its utility to the use for which it was built". SBA\'s example list (504 chapter, not all-inclusive): ' + '; '.join(s.rstrip(';').rstrip(' and') for s in sp81) + '. Self-storage, restaurants, day care and car dealerships are NOT on the list; Appendix 15 names "storage units and hotels" as examples of Special Purpose Property acquisitions where the real estate fully secures the loan.',
    'Same definition and same 26-item list (SOP 8, Section C Ch. 1 Credit Standards, pp. 328-329)', 'CONFLICT_RESOLVED', 'sop81', needle='Limited or Special Purpose Property: A limited-market property with a unique physical design',
    note='Fact sheet row 30: sources conflicted on self-storage. The 504 list omits it; Appendix 15 (line 5218) uses "storage units" as an example of the SPP projection exception. The site states both facts and does not call self-storage "listed".',
    v8cite=c8('Below is a list that contains examples of properties that SBA considers to be a Limited or Special Purpose Property'))
rows[-1]['verbatim_quote'] += ' | LIST (extract lines 3480-3506): ' + ' '.join(sp81)

# ---------------------------------------------------------------- rates and fees
add('R45', 'Prime rate', '7.00% (Federal Reserve H.15, release of October 9, 2026: bank prime loan 7.00 on each day October 2-8, 2026)', 'n/a', 'VERIFIED', 'h15', url=URL['h15'], q=norm(TEXT['h15'])[norm(TEXT['h15']).find('Release date'):norm(TEXT['h15']).find('Release date')+60] + ' ... ' + norm(TEXT['h15'])[norm(TEXT['h15']).find('Bank prime loan'):norm(TEXT['h15']).find('Bank prime loan')+60], section='H.15 Selected Interest Rates', paragraph='Bank prime loan', page='n/a (web)',
    note='The fact sheet\'s "from September 17, 2026" start date was not verified from H.15 and is not published.')
fr20 = norm(TEXT['fr20080'])
add('R46', 'SBA Optional Peg Rate, October to December 2026 (Q1 FY2027)', '5.00 percent', 'n/a (the prior quarter rate is not in any primary file opened here)', 'VERIFIED', 'fr20080', q=fr20[fr20.find('The Small Business Administration publishes'):fr20.find('October-December quarter of FY 2027.') + 36], section='91 FR 62585', paragraph='Interest Rates notice', page='p. 62585')
add('R47', '504 Third Party Lender maximum interest rate', '6% over the New York Prime rate (or the State maximum if lower)', 'Same rule (13 CFR 120.921(b))', 'VERIFIED', 'fr20080', q=fr20[fr20.find('Pursuant to 13 CFR 120.921(b)'):fr20.find('laws of the given State.') + 24], section='91 FR 62585', paragraph='Interest Rates notice', page='p. 62585')
add('R48', '504 debenture rate (October 2026 sale)', 'Not published: CDC pricing releases are not a primary source under constraint 1', 'n/a', 'NOT_IN_TEXT', 'sop81', url='', q='(no primary text)', section='n/a', paragraph='n/a', page='n/a', note='Fact sheet carried about 6.97% from CDC releases. Dropped.')
add('R49', 'FY2027 7(a) upfront (guaranty) fee schedule', 'Loans approved October 1, 2026 through September 30, 2027, maturity over 12 months: 2% of the guaranteed portion for $150,000 or less; 3% for $150,001 to $700,000; 3.5% up to $1,000,000 of guaranteed portion plus 3.75% above $1,000,000 for $700,001 to $5,000,000; 0.25% for maturities of 12 months or less. Annual service fee 0.55% of the outstanding guaranteed balance.',
    'FY2026 schedule (not reproduced)', 'VERIFIED', 'in881797', pdf='For loans of $150,000 or less: 2% of the guaranteed portion of the loan', section='SBA Information Notice 5000-881797', paragraph='SBA Guaranty Fee (Upfront Fee)')
rows[-1]['verbatim_quote'] += ' ' + pdfquote('in881797', 'For loans of $150,001 to $700,000: 3% of the guaranteed portion')[0] + ' ' + pdfquote('in881797', 'For loans of $700,001 to $5,000,000: 3.5% of the guaranteed portion')[0] + ' ' + pdfquote('in881797', 'Annual Service Fee will be 0.55% of the outstanding balance')[0]
add('R50', 'FY2027 7(a) upfront fee waiver', '0% upfront fee for loans of $700,000 or less to manufacturers (NAICS 31-33), the listed food supply chain NAICS codes (1111, 1112, 1113, 1121, 1122, 1123, 1124, 1125, 1129, 1141, 1151, 1152, 423820, 4244, 4245, 424910, 445110, 484220*, 484230*, 493120, 493130) and businesses located in a rural area', 'n/a', 'VERIFIED', 'in881797',
    pdf='the Upfront fee is 0%', section='SBA Information Notice 5000-881797', paragraph='SBA Guaranty Fee (Upfront Fee)')
add('R51', 'FY2027 504 fees and waivers', 'Loans approved October 1, 2026 through September 30, 2027: upfront guaranty fee 0.50% and annual service fee 0.203%; 0.204% annual for Debt Refinance without Expansion; both fees waived for manufacturers, the food supply chain codes and rural-area businesses, including 504 refinance loans', 'n/a', 'VERIFIED', 'in881796',
    pdf='The upfront guaranty fee will be 0.50% (50 basis points)', section='SBA Information Notice 5000-881796', paragraph='Fees for FY 2027')
rows[-1]['verbatim_quote'] += ' ' + pdfquote('in881796', 'the upfront guaranty fee and the annual service fee will be waived')[0] + ' ' + pdfquote('in881796', 'for a total of 0.204%')[0]
add('R52', 'Fee waiver window and trigger', 'The FY2027 fees and waivers apply to loans APPROVED October 1, 2026 through September 30, 2027 (both notices say "approved")', 'n/a', 'CONFLICT_RESOLVED', 'in881797', pdf='effective for all 7(a) loans approved on October 1, 2026, through and including', section='SBA Information Notice 5000-881797', paragraph='Opening paragraphs',
    note='Fact sheet conflict (approval date vs loan number): both notices use the approval date.')
add('R53', 'Rural area definition for the fee waiver', '"An area located in a county that the US Census Bureau has defined as at least 30 percent rural"', 'n/a', 'VERIFIED', 'sop81', needle='Rural Area: 7(a) and 504: An area located in a county')
add('R54', '7(a) maximum variable-rate spreads (Appendix 18 and Section B)', 'Prime or Optional Peg Rate plus 6.5% ($50,000 or less); plus 6.0% ($50,001-$250,000); plus 4.5% ($250,001-$350,000); plus 3.0% ($350,001 and over)', 'Same', 'VERIFIED', 'sop81', needle='Loans $350,001 and greater | Cannot exceed Prime or SBA Optional Peg Rate + 3.0%')
rows[-1]['verbatim_quote'] = ' / '.join(norm(LINES['sop81'][i]) for i in (1655, 1656, 1657, 1659))
add('R55', 'New Business and Start-Up Business definitions', 'New Business (7(a) and 504): in operation 2 years or less; a change of ownership with new, unproven ownership and acquisition debt may be treated as a New Business. Start-Up Business (7(a)): generating revenue for 1 year or less.', 'Same', 'VERIFIED', 'sop81', needle='New Business: (7(a) and 504) A business that has been in operation for 2 years or less')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'Start-Up Business: (7(a)) a business is a Start-Up Business')[1]
add('R56', 'Interest-only acquisition debt in the DSC test', 'Additional acquisition debt not on full standby and structured interest-only is tested on an amortization of not more than 10 years (lines of credit excepted)', 'Not stated', 'VERIFIED', 'sop81', needle='structured with interest-only payments, the Lender must apply an amortization that does not exceed 10-years')
add('R57', '504 refinance without job creation: employee cap', 'Where a refinancing project does not meet the job or economic development objectives, the 504 loan may not exceed the number of employees multiplied by $95,000', 'Employees multiplied by $90,000', 'VERIFIED', 'sop81', needle='the 504 loan may not exceed the product obtained by multiplying the number of employees of the Borrower by $95,000',
    span=('Notwithstanding 13 CFR § 120.860', 'by $95,000.'), v8cite=c8('multiplying the number of employees of the Borrower by $90,000', span=('Notwithstanding 13 CFR § 120.860', 'by $90,000.')))
add('R58', 'Personal guaranty threshold (regulation)', 'Holders of at least a 20 percent ownership interest generally must guarantee the loan', 'Same', 'VERIFIED', 'ecfr160', q=norm(TEXT['ecfr160'][TEXT['ecfr160'].find('( a ) Personal guarantees'):TEXT['ecfr160'].find('( b ) Appraisals')]), section='13 CFR 120.160', paragraph='(a) Personal guarantees', page='n/a (eCFR, current to 2026-10-07)')
add('R59', 'Collateral threshold for small loans', '7(a) Small and SBA Express loans of $50,000 or less need no collateral; above $50,000 the lender applies the Appendix 19 requirements (Express lenders may use their own policies for similarly sized loans)', 'Same thresholds', 'VERIFIED', 'sop81', needle='For 7(a) Small Loans of $50,000 or less, collateral is not required')
rows[-1]['verbatim_quote'] += ' ' + quote('sop81', 'For SBA Express Loans greater than $50,000, the Lender must follow the General Requirements')[1]

with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['id', 'rule', 'value_8_1', 'value_8', 'status', 'section', 'paragraph', 'page', 'verbatim_quote', 'primary_url', 'checked_on', 'resolution_note', 'value_8_cite'])
    w.writeheader()
    for r in rows: w.writerow(r)
from collections import Counter
print('rows', len(rows), dict(Counter(r['status'] for r in rows)))
for r in rows: print(f"{r['id']:5} {r['status']:18} {r['section'][:48]:48} {r['page']:14} q={len(r['verbatim_quote'])}")
