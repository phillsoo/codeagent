# Cloud pricing-change presentation pattern

Use this pattern when a deck compares cloud service pricing before and after a cutoff date.

## Evidence hierarchy

1. Compare dated snapshots of the vendor's machine-readable price data by stable SKU/part number.
2. Cross-check the surrounding contract/service-description revisions and their effective dates.
3. Use the current human-readable price page only as a secondary presentation source.
4. Distinguish four change types:
   - existing SKU price increase/decrease,
   - new or retired SKU,
   - billing-unit conversion,
   - component separation (for example, infrastructure + license + storage).
5. State when the vendor did not publish a separate price-change notice. Do not equate a contract effective date, price-data build timestamp, and customer billing transition date.
6. If a public price cell is blank, report the limitation and require an ordering document or quote; never infer “unchanged.”

## Deck structure

A concise executive deck works well in seven slides:

1. Cover with 3–4 headline changes.
2. One-sentence thesis and three executive takeaways.
3. Product-level before/after table.
4. Ranked percentage-change chart.
5. Product-specific cost drivers and minimum/commitment conditions.
6. Timeline separating old price build, contract effective date, new price build, and order-form verification.
7. Sources, confidence level, and commercial caveat.

## Content controls

- Label all values with currency, billing unit, and list-price model.
- Preserve unchanged license/BYOL rates separately from infrastructure and storage increases.
- Recalculate every percentage from source values; do not copy rounded percentages without checking.
- Add a plain-language caveat that actual billing may depend on region, currency, committed-use discount, price protection, and ordering document.
- Keep a machine-readable evidence table or JSON beside the deck for independent review.

## QA thresholds that worked

- Bottom safe margin for every text box: at least 0.50 in; 0.58–0.60 in is safer.
- Source/footer text: at least 10.5 pt.
- Chart axis and unit text: at least 10 pt; terminal percentage labels at least 12 pt.
- Source URLs and legal caveats: at least 11 pt.
- Normal-text contrast: at least 4.5:1.
- Verify PPTX ZIP integrity, slide count, 16:9 dimensions, PDF page count, and full-slide renders.
- After fixing a visual defect, regenerate PPTX, PDF, and images and require a fresh independent review; a prior conditional pass does not carry forward automatically.
