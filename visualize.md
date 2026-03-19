# Visualize Shortlist Ideas

## Goal

Build an extremely lightweight local web app that visualizes the current `shortlist/` as a single high-signal interactive view.

The app is for internal strategy use, not external presentation.

The view should help answer:

- which ideas are strongest in their current form
- which ideas become much more interesting after reframing
- which ideas have large upside even if they are not yet strong
- which ideas have strong adjacency / option value and should not be thrown away too quickly

## Product Shape

Build exactly one view: an interactive `Idea Phase Space`.

This is not a dashboard suite, not a multi-page app, and not a framework-heavy frontend.

## Stack

Use the simplest stack with the highest bang-for-buck:

- static local web app
- plain `HTML`
- plain `CSS`
- plain `JavaScript`
- `d3` as the only visualization dependency

Do not use:

- React
- TypeScript
- Vite
- Next.js
- Svelte
- Vue
- a backend server
- a database

The app must be runnable locally with:

```bash
python3 -m http.server
```

## App Structure

Create a small app directory:

```text
viz/
  index.html
  styles.css
  app.js
  data/
    ontology.shortlist.json
```

Optional:

```text
scripts/
  validate_ontology.py
```

Only add the validator script if it stays tiny and only validates the ontology file.

## Core Visualization

Render one SVG scatterplot-like phase space.

### Axes

- x-axis: `product_leverage`
- y-axis: `independence`

Interpretation:

- left = feature / connector / services-heavy / low product leverage
- right = stronger standalone product / platform potential
- bottom = high platform dependency / vendor absorption risk
- top = greater independence / better chance of surviving as a company

### Node Encoding

Each idea is one node.

- node position = current or reframed coordinates
- node size = `upside`
- node fill color = `archetype`
- node outer ring / halo intensity = `adjacency`
- node opacity = confidence / survivability signal if useful, otherwise keep opacity constant

### Motion

Support exactly one mode switch:

- `Current`
- `Reframed`

In `Current` mode:

- nodes sit at `current.product_leverage` and `current.independence`
- show a motion arrow or ghost target toward `reframed`

In `Reframed` mode:

- animate nodes to `reframed.product_leverage` and `reframed.independence`
- hide arrows

This view must make it obvious which ideas improve materially when reframed.

## Interactions

Keep interactions minimal and high-signal.

### Required

1. `Current / Reframed` toggle
2. Hover tooltip or sidecard with ontology detail
3. Filter controls for:
   - `archetype`
   - `domain`
   - `status`
4. Label behavior:
   - default to labeling only highlighted / hovered nodes
   - allow optional `show all labels` toggle

### Not Required

Do not add in v1:

- pan / zoom
- search
- editable nodes
- drag interactions
- multiple charts
- force-directed graph layout
- persistence

## Ontology

Do not try to auto-extract the ontology in v1.

The shortlist is small and the important fields are judgment-heavy. Manual curation is the correct v1 approach.

Store one manually curated JSON file at:

```text
viz/data/ontology.shortlist.json
```

## Ontology Schema

Use one record per shortlist idea.

### Required Fields

```json
{
  "id": "sec-soc-agent-swarm",
  "label": "SOC Agent Swarm",
  "domain": "security",
  "archetype": "workflow_automation",
  "status": "strong_keep",
  "current": {
    "product_leverage": 0.72,
    "independence": 0.61,
    "upside": 0.86,
    "adjacency": 0.74
  },
  "reframed": {
    "product_leverage": 0.84,
    "independence": 0.79
  },
  "current_form": "multi-agent SOC investigation layer",
  "hidden_wedge": "cross-tool investigation brief generator",
  "end_state_company": "security operations control layer",
  "desperate_user": "SOC manager",
  "buyer": "security leadership",
  "job": "reduce investigation time across fragmented tools",
  "workaround": "manual cross-tool correlation",
  "moat_type": "integration_sprawl",
  "reframing_direction": "agents -> cross-platform workflow layer",
  "crazy_upside": "neutral operating layer for multi-vendor SOCs",
  "option_value": "high",
  "reason_alive": "Strong workflow pain and real cross-tool wedge.",
  "sources": {
    "shortlist": "shortlist/sec-soc-agent-swarm.md"
  }
}
```

### Numeric Fields

These must be normalized `0..1`:

- `current.product_leverage`
- `current.independence`
- `current.upside`
- `current.adjacency`
- `reframed.product_leverage`
- `reframed.independence`

### Enums

#### `status`

- `faint_pulse`
- `alive`
- `strong_keep`

#### `archetype`

- `control_plane`
- `integration_layer`
- `data_infrastructure`
- `workflow_automation`
- `migration_tool`
- `compliance_system`
- `domain_ai`

#### `moat_type`

- `workflow_lockin`
- `proprietary_data`
- `integration_sprawl`
- `compliance_knowledge`
- `operational_control`

#### `option_value`

- `low`
- `medium`
- `high`

## Shortlist Coverage

Populate records for every current shortlist item listed in `shortlist/README.md`.

At minimum, include:

- `cloud-customer-cloud-control-plane`
- `data-vertica-control-plane`
- `sec-security-data-labeling`
- `sec-soc-agent-swarm`
- `ai-autonomous-driving-rd-platform`
- `dev-ai-vulnerability-remediator`
- `sec-saas-telemetry-connectors`
- `sec-log-normalization-layer`
- `aiops-cmdb-intelligence-layer`
- `sec-threat-intel-integration-factory`
- `sec-security-data-lake`
- `cloud-mssp-control-plane`
- `cloud-secure-aws-landing-zone`
- `cloud-tenant-ops-control-plane`
- `itsm-it-helpdesk-agent`
- `obs-dynatrace-migration-accelerator`
- `obs-splunk-cloud-replatforming`
- `obs-splunk-dynatrace-migrator`
- `obs-sybase-datadog-integration`
- `sec-elastic-integration-hub`

If the shortlist changes later, update only the JSON file first.

## Tooltip / Detail Content

On hover or click, show a compact detail card with:

- `label`
- `status`
- `current_form`
- `hidden_wedge`
- `reframing_direction`
- `crazy_upside`
- `reason_alive`
- `option_value`
- `source` link or path reference

Keep the copy short and strategic.

## Visual Design

Optimize for clarity and intentionality, not presentation polish.

### Principles

- clean light background
- strong contrast
- restrained but expressive color system
- legible labels
- minimal chrome
- no decorative clutter

### Suggested Layout

- top bar with title and one-line explanation
- left or top controls for filters + mode toggle
- main SVG view centered and dominant
- floating detail panel or fixed side panel
- small legend for color = archetype and halo = adjacency

## Behavior Rules

### Position Logic

In `Current` mode:

- read from `current.product_leverage`
- read from `current.independence`

In `Reframed` mode:

- read from `reframed.product_leverage`
- read from `reframed.independence`

### Size Logic

- derive radius from `current.upside`
- keep node size constant across modes

### Halo Logic

- derive halo thickness, blur, or secondary stroke from `current.adjacency`
- adjacency should be visually apparent without overwhelming the node itself

### Labels

- always label hovered node
- always label filtered subset if small enough
- otherwise suppress most labels by default to avoid clutter

## Complexity Constraints

Keep the implementation aggressively simple.

### Allowed Complexity

- a single JSON fetch
- a single SVG render pipeline
- a small filter state object in JS
- a single tooltip / detail renderer

### Avoid

- state management libraries
- routing
- bundling
- schema generation
- markdown parsing inside the browser
- deriving ontology live from source files

## Optional Validator

If implemented, `scripts/validate_ontology.py` should only:

- load `viz/data/ontology.shortlist.json`
- ensure required fields exist
- ensure numeric fields are between `0` and `1`
- ensure referenced source paths exist

It must not generate data, only validate it.

## Acceptance Criteria

The implementation is done when:

- the app runs locally via static file hosting
- every shortlist idea appears as a node
- `Current / Reframed` toggle animates smoothly
- filters for `archetype`, `domain`, and `status` work
- hover or click shows useful ontology detail
- `upside` and `adjacency` are visible in the same view
- the app feels lightweight and understandable from reading the source

## Explicit Non-Goals

Do not build:

- an ontology editor
- a markdown ingestion pipeline
- a generalized graph exploration tool
- a polished external presentation site
- multiple alternative visualization modes
- authentication or persistence

## Recommended Implementation Order

1. Create the ontology JSON manually for all shortlist ideas.
2. Build the static page shell.
3. Render nodes in `Current` mode.
4. Add `Reframed` toggle and transitions.
5. Add hover detail card.
6. Add filters.
7. Add legends and label toggle.
8. Add optional ontology validator if needed.

## Key Principle

The ontology is the product. The chart is the interface.

Do not over-engineer the app before the ontology is useful.
