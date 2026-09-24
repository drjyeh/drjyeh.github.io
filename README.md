# drjyeh.github.io
# drjyeh.com

Personal website of Dr. James Hsi-Jen Yeh, Dean of the College of Business and Technology at Seattle Pacific University.

**Live site:** https://drjyeh.com

## About this site

A single-page static site covering his biography, leadership, career, research, publications and patents, personal projects, and contact information. It is plain HTML, CSS, and JavaScript with no build step or framework, hosted on GitHub Pages with a custom domain.

## Structure

```
index.html            Page content
style.css             Styles, including mobile layout
script.js             Mobile menu and publication filter
CNAME                 Custom domain (drjyeh.com); do not delete
assets/
  headshot.jpg        Portrait (also used for link previews)
  CV.pdf              Curriculum vitae
  publications.pdf    Full publications and patents list
```

## Updating the site

- **Text:** edit `index.html` and commit. GitHub Pages republishes automatically, usually within a minute or two.
- **CV or publications list:** replace the PDF in `assets/` with a new file of the same name.
- **Photo:** replace `assets/headshot.jpg` with a square image of about 800–1024 px, ideally under 200 KB.
- **New publication:** copy an existing `<li>` in the publications list, update it, and set `data-topic` to `iot`, `energy`, or `photonics` so the filter buttons include it.

## Previewing locally

From the repo folder:

```
python3 -m http.server
```

Then open http://localhost:8000.

## Copyright

© 2026 James Hsi-Jen Yeh. All rights reserved. Site content, text, and images may not be reused without permission.
