
# build bo4e-openapi.json
swagger-cli bundle bo4e-openapi.yaml --outfile _build/bo4e-openapi.json --dereference --type json &&

# minify bo4e-openapi.json
jq -c . _build/bo4e-openapi.json > _build/bo4e-openapi.min.json &&

# remove bo4e-openapi.json
rm _build/bo4e-openapi.json

# build event-openapi.json
swagger-cli bundle events-openapi.yaml --outfile _build/events-openapi.json --dereference --type json &&

# minify event-openapi.json
jq -c . _build/events-openapi.json > _build/events-openapi.min.json &&

# remove event-openapi.json
rm _build/events-openapi.json
