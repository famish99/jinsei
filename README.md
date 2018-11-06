# jinsei

Automated resume generation tool that converts a YAML-defined resume into HTML via Jinja2 then converts the output to PDF via wkhtmltopdf.

## Setup

Expects `template/` directory with Jinja formatted HTML file and any associated files needed for rendering.

## Build instructions

Jinsei can run single shot or autobuild mode.

### Build once:

```bash
./jinsei.py <input yaml> <output pdf>
```

### Autobuild on change:

```bash
./jinsei.py --method auto <input yaml> <output pdf>
```

## Requires:
* Python 3 (targeting 3.5)
  * ruamel.yaml
  * Jinja2
* wkhtmltopdf - Needed for HTML to PDF conversion stage
