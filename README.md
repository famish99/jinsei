# jinsei

Automated resume generation tool that converts a YAML-defined resume into HTML via Jinja2 then converts the output to PDF via wkhtmltopdf.

## Setup

### Prerequisites

Requires that you have Docker Desktop setup.

### Configure Run Parameters

Create an `.env` file with the following parameters:

```env
INPUT_FILE=<input resume YAML path>
METHOD=(once|auto)
OUTPUT_FILE=<output PDF path>
OVERRIDES=<optional: override resume YAML paths>
TEMPLATE_DIR=<template directory>
```

### Directory Structure

Expects directory with Jinja formatted HTML file and any associated files needed for rendering such as style sheets under your `TEMPLATE_DIR`.

### Running the Application

Jinsei can run single shot or autobuild mode which can be configured using the `METHOD` variable.

To run the application:

```bash
docker-compose up
```

## Resume Template Format

Top level keys for the resume YAML are the following:

 * `template`: Path of the HTML template file
 * `name`: Full name
 * `email`
 * `phone`
 * `address`: Primary street address line
 * `address_2`: (Optional) Second street address line
 * `city`
 * `state`
 * `zipcode`
 * `title`: Current Job title
 * `profile`: A summary line
 * `skills`: A list of technical skills
 * `experience`: Outlined in [Experience Fields](#experience-fields)
 * `education`: Outlined in [Education Fields](#experience-fields)
 * `projects`: Outlined in [Projects Fields](#experience-fields)

### Experience Fields

Each `experience` item expects the following fields:

 * `employer`
 * `title`
 * `location`
 * `start_date`
 * `end_date`
 * `tasks`: A list of projects and responsibilites held in the position

### Education Fields

Each `education` item expects the following fields:

 * `institution`
 * `location`
 * `start_date`
 * `end_date`
 * `degree`

### Projects Fields

Each `projects` item expects the following fields:

 * `title`
 * `description`
 * `link`: `https://` will automatically be prepended to this value, normalizing the printed vs pdf version.

### Overrides

`OVERRIDES` will allow you to specify multiple files that you may not want to track in the repo but hold data relevant to your resume for example:

```yaml
email: thats@secret.com
phone: 555-555-5555
address: 221B Baker Street
city: Westminster
state: London
zipcode: NW1
```

Entries under `skills`, `experience`, `education`, `project` will be appended to the base resume file, the rest will be replaced with the last specified file taking precedence.