# PBMS

Programme & Beneficiary Management System (PBMS) for OpenG2P — a consolidated
monorepo bringing together the Odoo modules, the decoupled eligibility &
entitlement engine, the portal APIs, Docker packaging, and a single Helm chart.

## Layout

| Path | Description | License |
|------|-------------|---------|
| `odoo/` | Odoo modules — core (`g2p_pbms`, `g2p_pbms_program_access`), `extensions/`, and `community-addons/` | LGPL-3.0 |
| `core/` | Background-task engine — PBMS + bg-task models, Celery workers and beat producers | MPL-2.0 |
| `extensions/` | Registry adapter extensions for the background-task engine | MPL-2.0 |
| `apis/` | Staff Portal and Beneficiary Portal FastAPI services | MPL-2.0 |
| `docker/` | Dockerfiles for the Odoo (`core`), API, and Celery images | MPL-2.0 |
| `deployment/` | Single consolidated Helm chart (`charts/openg2p-pbms`) | MPL-2.0 |

## Images

Built from local source by the workflows under `.github/workflows/`, tagged with
the branch name (a push to `develop` publishes `:develop`):

- `openg2p/openg2p-pbms-core` (Odoo)
- `openg2p/openg2p-pbms-staff-portal-api`
- `openg2p/openg2p-pbms-bene-portal-api`
- `openg2p/openg2p-pbms-bg-task-celery-workers`
- `openg2p/openg2p-pbms-bg-task-celery-beat-producers`

## Helm

The chart under `deployment/charts/openg2p-pbms` installs and runs all of PBMS.
Chart versions are published to
[openg2p-helm](https://openg2p.github.io/openg2p-helm) by the `helm-publish`
workflow, versioned from the branch (`develop` → `0.0.0-develop.<run-number>`).

```sh
helm install pbms deployment/charts/openg2p-pbms
```

External OpenG2P libraries (e.g. `openg2p-fastapi-common`) are tracked at their
`develop` branch.
