#!/bin/bash

# Define input and output files
BO4E_OPENAPI_YAML="bo4e/bo4e-openapi.yaml"
EVENTS_OPENAPI_YAML="events/events-openapi.yaml"
MALOIDENT_OPENAPI_YAML="maloident-macoapp/maloident-macoapp.yaml"
MALOIDENT_NB_YAML="maloident-netzbetreiber/maloident-netzbetreiber.yaml"
MALOIDENT_LF_YAML="maloident-lieferant/maloident-lieferant.yaml"
MACOAPP_TRIGGER_YAML="macoapp-trigger/macoapp-trigger.yaml"
MACOAPP_LESEN_YAML="macoapp-lesen/macoapp-lesen.yaml"
MACOAPP_SCHREIBEN_YAML="macoapp-schreiben/macoapp-schreiben.yaml"
OUTPUT_DIR="_build"

# Define a function to build and minify OpenAPI JSON
build_and_minify_openapi() {
  local input_yaml=$1
  local output_filename=$2

  # Build OpenAPI JSON
  swagger-cli bundle "$input_yaml" --outfile "${OUTPUT_DIR}/${output_filename}.json" --dereference --type json

  # Minify OpenAPI JSON
 # jq -c . "${OUTPUT_DIR}/${output_filename}.json" > "${OUTPUT_DIR}/${output_filename}.min.json" &&

  # Remove original OpenAPI JSON
  #rm "${OUTPUT_DIR}/${output_filename}.json"

}



build_and_minify_openapi "$MACOAPP_TRIGGER_YAML" "macoapp-trigger"
build_and_minify_openapi "$MACOAPP_LESEN_YAML" "macoapp-lesen"
build_and_minify_openapi "$MACOAPP_SCHREIBEN_YAML" "macoapp-schreiben"

build_and_minify_openapi "$MALOIDENT_OPENAPI_YAML" "maloident-macoapp"
build_and_minify_openapi "$MALOIDENT_NB_YAML" "maloident-netzbetreiber"
build_and_minify_openapi "$MALOIDENT_LF_YAML" "maloident-lieferant"
build_and_minify_openapi "$BO4E_OPENAPI_YAML" "bo4e-openapi"

# Build and minify bo4e-openapi.json


# Build and minify events-openapi.json
build_and_minify_openapi "$EVENTS_OPENAPI_YAML" "events-openapi"

