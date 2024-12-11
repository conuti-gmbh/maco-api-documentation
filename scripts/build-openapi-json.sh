#!/bin/bash

# Define input and output files
BO4E_OPENAPI_YAML="bo4e/bo4e-openapi.yaml"
EVENTS_OPENAPI_YAML="events/events-openapi.yaml"
MALOIDENT_OPENAPI_YAML="maloidentevent/events-maloident.yaml"
OUTPUT_DIR="_build"

# Define a function to build and minify OpenAPI JSON
build_and_minify_openapi() {
  local input_yaml=$1
  local output_filename=$2

  # Build OpenAPI JSON
  swagger-cli bundle "$input_yaml" --outfile "${OUTPUT_DIR}/${output_filename}.json" --dereference --type json &&

  # Minify OpenAPI JSON
  jq -c . "${OUTPUT_DIR}/${output_filename}.json" > "${OUTPUT_DIR}/${output_filename}.min.json" &&

  # Remove original OpenAPI JSON
  rm "${OUTPUT_DIR}/${output_filename}.json"
}


build_and_minify_openapi "$MALOIDENT_OPENAPI_YAML" "events-maloident"

# Build and minify bo4e-openapi.json
build_and_minify_openapi "$BO4E_OPENAPI_YAML" "bo4e-openapi"

# Build and minify events-openapi.json
build_and_minify_openapi "$EVENTS_OPENAPI_YAML" "events-openapi"

