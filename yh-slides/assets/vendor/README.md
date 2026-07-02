# Local Vendor Assets

This directory contains front-end resources localized for `yh-slides` seeds and HTML outputs.

## Files

- `google-fonts-local.css` and `fonts/*.woff2`: localized font CSS and font shards for the seed templates.
- `js/lucide.js`, `js/lucide.min.js`: local Lucide UMD builds.
- `js/gsap.min.js`, `js/ScrollTrigger.min.js`: local GSAP runtime files for 2D / Path D.
- `js/motion.min.js`: local Motion ESM build for 2D / Path C magazine animations.

## Usage

When copying a 2D / Path C-D seed into an output directory, also copy this directory to:

```text
output/assets/vendor/
```

Seed files refer to these assets through `assets/vendor/...` paths. Do not replace them with CDN links.

## Notes

These are vendored runtime assets for offline use. API endpoints used by image generation scripts remain network endpoints by design and are not mirrored here.
