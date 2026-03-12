# Static Site Portfolio Generator

[< Back to Projects](/projects/)

This site is powered by a custom **static site generator** built in Python and maintained in this repository.

## Problem

I wanted a portfolio that:

- Uses simple Markdown files for content.
- Can be built and deployed automatically.
- Keeps the generation logic under my control instead of relying on a large framework.

## Solution

- A small static site generator that:
  - Reads content from the `/content` directory.
  - Produces a static site suitable for deployment (for example, to GitHub Pages).
  - Integrates with a simple build script.

## Tech Stack

- **Language**: Python
- **Content format**: Markdown files under `/content`
- **Deployment**: GitHub Actions workflow in this repo

## Highlights

- Minimal, easy-to-understand content model.
- Git-based workflow: open a PR to change content or behavior.
- Good starting point for experimenting with custom static site features.

## Links

- Repository: https://github.com/ssuish/ssuish-portfolio

