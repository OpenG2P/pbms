{{/*
Overriding Odoo's templates. All the variable names here match ones in Odoo's
values.yaml, not this chart's values.yaml. The templates here will be available
to Odoo's chart.
*/}}

{{- define "odoo.databaseHost" -}}
{{- tpl .Values.externalDatabase.host . -}}
{{- end -}}

{{- define "odoo.databaseName" -}}
{{- tpl .Values.externalDatabase.database . -}}
{{- end -}}

{{- define "odoo.databaseUser" -}}
{{- tpl .Values.externalDatabase.user . -}}
{{- end -}}

{{- define "odoo.databaseSecretPasswordKey" -}}
{{- tpl .Values.externalDatabase.existingSecretPasswordKey . -}}
{{- end -}}

{{- define "odoo.databaseSecretName" -}}
{{- tpl .Values.externalDatabase.existingSecret . -}}
{{- end -}}

{{/*
Expand the name of the chart.
*/}}
{{- define "pbms.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "pbms.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "pbms.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "pbms.labels" -}}
helm.sh/chart: {{ include "pbms.chart" . }}
{{ include "pbms.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "pbms.selectorLabels" -}}
app.kubernetes.io/name: {{ include "pbms.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Render Env values section
*/}}
{{- define "pbms.baseEnvVars" -}}
{{- $context := .context -}}
{{- range $k, $v := .envVars }}
{{- if or (kindIs "int64" $v) (kindIs "float64" $v) (kindIs "bool" $v) }}
- name: {{ $k }}
  value: {{ $v | quote }}
{{- else if kindIs "string" $v }}
- name: {{ $k }}
  value: {{ include "common.tplvalues.render" ( dict "value" $v "context" $context ) | squote }}
{{- else }}
{{- $vEnabled := "true" }}
{{- if hasKey $v "enabled" }}
{{- $vEnabled = kindIs "bool" $v.enabled | ternary ($v.enabled | squote) (include "common.tplvalues.render" (dict "value" $v.enabled "context" $context)) }}
{{- $v = omit $v "enabled" }}
{{- end }}
{{- if eq $vEnabled "true" }}
- name: {{ $k }}
  valueFrom: {{- include "common.tplvalues.render" ( dict "value" $v "context" $context ) | nindent 4}}
{{- end }}
{{- end }}
{{- end }}
{{- end -}}

{{/*
Templates for openg2p-pbms-bg-task-celery-beat-producers
*/}}

{{/*
Create the name of the service account to use
*/}}
{{- define "pbms.beat-producers.serviceAccountName" -}}
{{- if .Values.beatProducers.serviceAccount.create -}}
{{ default (include "common.names.fullname" .) .Values.beatProducers.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.beatProducers.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "pbms.beat-producers.imagePullSecrets" -}}
{{- include "common.images.pullSecrets" (dict "images" (list .Values.beatProducers.image .Values.beatProducers.postgresCheckerInit.image) "global" .Values.global) -}}
{{- end -}}

{{/*
Render Env values section for beat-producers
*/}}
{{- define "pbms.beat-producers.envVars" -}}
{{- $envVars := merge (deepCopy .Values.beatProducers.envVars) (deepCopy .Values.beatProducers.envVarsFrom) -}}
{{- include "pbms.baseEnvVars" (dict "envVars" $envVars "context" $) }}
{{- end -}}

{{/*
Templates for openg2p-pbms-bg-task-celery-workers
*/}}

{{/*
Create the name of the service account to use
*/}}
{{- define "pbms.celery-workers.serviceAccountName" -}}
{{- if .Values.celeryWorkers.serviceAccount.create -}}
{{ default (include "common.names.fullname" .) .Values.celeryWorkers.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.celeryWorkers.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "pbms.celery-workers.imagePullSecrets" -}}
{{- include "common.images.pullSecrets" (dict "images" (list .Values.celeryWorkers.image .Values.celeryWorkers.postgresCheckerInit.image) "global" .Values.global) -}}
{{- end -}}

{{/*
Render Env values section for celery-workers
*/}}
{{- define "pbms.celery-workers.envVars" -}}
{{- $envVars := merge (deepCopy .Values.celeryWorkers.envVars) (deepCopy .Values.celeryWorkers.envVarsFrom) -}}
{{- include "pbms.baseEnvVars" (dict "envVars" $envVars "context" $) }}
{{- end -}}

{{/*
Templates for openg2p-pbms-staff-portal-api
*/}}

{{/*
Create the name of the service account to use
*/}}
{{- define "pbms.staff-portal-api.serviceAccountName" -}}
{{- if .Values.staffPortalApi.serviceAccount.create -}}
{{ default (include "common.names.fullname" .) .Values.staffPortalApi.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.staffPortalApi.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "pbms.staff-portal-api.imagePullSecrets" -}}
{{- include "common.images.pullSecrets" (dict "images" (list .Values.staffPortalApi.image .Values.staffPortalApi.postgresCheckerInit.image) "global" .Values.global) -}}
{{- end -}}

{{/*
Render Env values section for staff-portal-api
*/}}
{{- define "pbms.staff-portal-api.envVars" -}}
{{- $envVars := merge (deepCopy .Values.staffPortalApi.envVars) (deepCopy .Values.staffPortalApi.envVarsFrom) -}}
{{- include "pbms.baseEnvVars" (dict "envVars" $envVars "context" $) }}
{{- end -}}

{{/*
Templates for openg2p-pbms-bene-portal-api
*/}}

{{/*
Create the name of the service account to use
*/}}
{{- define "pbms.bene-portal-api.serviceAccountName" -}}
{{- if .Values.benePortalApi.serviceAccount.create -}}
{{ default (include "common.names.fullname" .) .Values.benePortalApi.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.benePortalApi.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "pbms.bene-portal-api.imagePullSecrets" -}}
{{- include "common.images.pullSecrets" (dict "images" (list .Values.benePortalApi.image .Values.benePortalApi.postgresCheckerInit.image) "global" .Values.global) -}}
{{- end -}}

{{/*
Render Env values section for bene-portal-api
*/}}
{{- define "pbms.bene-portal-api.envVars" -}}
{{- $envVars := merge (deepCopy .Values.benePortalApi.envVars) (deepCopy .Values.benePortalApi.envVarsFrom) -}}
{{- include "pbms.baseEnvVars" (dict "envVars" $envVars "context" $) }}
{{- end -}}
