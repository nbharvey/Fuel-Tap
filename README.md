# Fuel Tap v3

A phone-first PWA for estimating daily nutrition during endurance training without maintaining a food diary.

## What changed
- Starry dark-blue/purple theme.
- Breakfast, Lunch, Dinner, Snacks, and Drinks pickers.
- Selecting a food immediately adds its calorie/macronutrient/sodium/fluid/caffeine values.
- Food names are **not stored in the research log**.
- Added sugar removed.
- Manual quick-add buttons remain available as a fallback.
- Workout Nutrition mode remains available; workout amounts are included in daily totals and separately summarized.
- Date selector allows backfilling a prior day.
- Daily CSV = exactly one row per date.
- Export All Dates creates a flat multi-date CSV.

## Research columns
`local_date, energy_kcal, protein_g, carbs_g, fat_g, sodium_mg, caffeine_mg, water_oz, water_ml` plus workout-only versions of the same fields, optional workout labels, and the count of logging actions.

## Food library
Food serving values live in `food-library.js`. They are practical estimates. Brand- and recipe-specific values vary, so this file is intentionally easy to revise as your common foods become clearer.

## Install on iPhone
Host this entire folder on an HTTPS static host (Netlify, GitHub Pages, etc.), open the URL in Safari, tap Share, then **Add to Home Screen**.

If replacing an older Fuel Tap deployment, upload the full v3 folder to the same site. Because this version uses a new storage key, old v1 data is not automatically migrated into the new simplified daily-total architecture.

## Daily Python pipeline
`pipeline/nutrition_pipeline.py` scans a folder of `fuel-tap_YYYY-MM-DD.csv` exports and creates one master CSV with one row per date.

Example:

```bash
python3 pipeline/nutrition_pipeline.py \
  --input ~/Documents/Ironman/nutrition_exports \
  --output ~/Documents/Ironman/nutrition_master.csv
```

For a low-friction phone-to-computer workflow, save daily exports into a synced iCloud Drive or Google Drive folder. The Python step can then run against the synced local folder. Fully automatic background upload from an iPhone PWA would require a cloud endpoint/backend; the current app intentionally remains local/offline-first.
