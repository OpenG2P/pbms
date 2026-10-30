# PBMS

Programme & Beneficiary Management System (PBMS) for OpenG2P — a consolidated
monorepo bringing together the Odoo modules, the decoupled eligibility &
entitlement engine, the portal APIs, Docker packaging, and a single Helm chart.

## Layout

| Path | Description | License |
|------|-------------|---------|
| `odoo/` | Odoo modules — core (`g2p_pbms`, `g2p_pbms_program_access`) and `community-addons/` | LGPL-3.0 |
| `core/` | Background-task engine — PBMS + bg-task models, Celery workers and beat producers | MPL-2.0 |
| `apis/` | Staff Portal and Beneficiary Portal FastAPI services | MPL-2.0 |
| `docker/` | Dockerfiles for the Odoo, API, and Celery base images | MPL-2.0 |
| `deployment/` | Platform Helm chart (`charts/openg2p-pbms-platform`) | MPL-2.0 |

## Images

Built from local source by the workflows under `.github/workflows/`, tagged with
the branch name (a push to `develop` publishes `:develop`). Names ending in
`-base` are extended by `pbms-connectors`. The beneficiary API is installed as-is.

- `openg2p/openg2p-pbms-odoo-base`
- `openg2p/openg2p-pbms-celery-base` (worker and beat, selected by `CELERY_APP`)
- `openg2p/openg2p-pbms-staff-api-base`
- `openg2p/openg2p-pbms-beneficiary-api`

## Helm

`deployment/charts/openg2p-pbms-platform` holds the Kubernetes templates and the
base image tags. Install `openg2p-pbms` from `pbms-connectors`, which depends on
this chart. Chart versions are published to
[openg2p-helm](https://openg2p.github.io/openg2p-helm) by the build workflow,
versioned from the branch (`develop` → `0.0.0-develop.<run-number>`).

External OpenG2P libraries (e.g. `openg2p-fastapi-common`) are tracked at their
`develop` branch.
