#!/bin/bash

# Definition der Eingabe- und Ausgabedateien
EVENTS_OPENAPI_YAML="events/events-openapi.yaml"
MALOIDENT_OPENAPI_YAML="maloident-macoapp/maloident-macoapp.yaml"
MALOIDENT_NB_YAML="maloident-netzbetreiber/maloident-netzbetreiber.yaml"
MALOIDENT_LF_YAML="maloident-lieferant/maloident-lieferant.yaml"
MACOAPP_TRIGGER_YAML="macoapp-trigger/macoapp-trigger.yaml"
MACOAPP_LESEN_YAML="macoapp-lesen/macoapp-lesen.yaml"
MACOAPP_SCHREIBEN_YAML="macoapp-schreiben/macoapp-schreiben.yaml"
OUTPUT_DIR="_build"
SCHEMAS_DIR="_schemas"
BO4E_COMPONENTS_YAML="${SCHEMAS_DIR}/bo4ecomponents.yml"
OPENAPI_URL="https://raw.githubusercontent.com/conuti-gmbh/bo4e-schema/refs/heads/master/docs/openapi.yaml"

# Erstellen der notwendigen Verzeichnisse
mkdir -p "$OUTPUT_DIR"
mkdir -p "$SCHEMAS_DIR"

# Herunterladen der openapi.yaml-Datei
curl -o "${SCHEMAS_DIR}/openapi.yml" "$OPENAPI_URL"

OPENAPI_FILE="${SCHEMAS_DIR}/openapi.yml"

# Überprüfen, ob die Quelldatei existiert
if [[ ! -f "$OPENAPI_FILE" ]]; then
  echo "Die Datei $OPENAPI_FILE existiert nicht."
  exit 1
fi

echo "OpenAPI-Datei erfolgreich heruntergeladen."

# Funktion zum Erstellen und Minifizieren von OpenAPI JSON
build_and_minify_openapi() {
  local input_yaml=$1
  local output_filename=$2

  # Erstellen von OpenAPI JSON
  npx @redocly/openapi-cli bundle "$input_yaml" -o "${OUTPUT_DIR}/${output_filename}.yaml"
  npx @redocly/openapi-cli bundle "$input_yaml" --ext json -f -o "${OUTPUT_DIR}/${output_filename}.json"  
  # Minifizieren von OpenAPI JSON
  jq -c . "${OUTPUT_DIR}/${output_filename}.json" > "${OUTPUT_DIR}/${output_filename}.min.json"

  # Entfernen der ursprünglichen OpenAPI JSON
  #rm "${OUTPUT_DIR}/${output_filename}.json"
}

# Verarbeiten jeder YAML-Datei
build_and_minify_openapi "$MACOAPP_SCHREIBEN_YAML" "macoapp-schreiben"
build_and_minify_openapi "$MACOAPP_TRIGGER_YAML" "macoapp-trigger"
build_and_minify_openapi "$MACOAPP_LESEN_YAML" "macoapp-lesen"
build_and_minify_openapi "$MALOIDENT_OPENAPI_YAML" "maloident-macoapp"
build_and_minify_openapi "$MALOIDENT_NB_YAML" "maloident-netzbetreiber"
build_and_minify_openapi "$MALOIDENT_LF_YAML" "maloident-lieferant"
build_and_minify_openapi "$MACOAPP_TRIGGER_YAML" "events-openapi"
