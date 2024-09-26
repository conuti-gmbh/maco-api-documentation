## How to generate a single openapi.yaml file from multiple openapi.yaml files using swagger-cli



### Developing
```
nodemon
```

### Build _build/openapi.yaml
```
swagger-cli bundle openapi.yaml --outfile _build/openapi.yaml --dereference  --type yaml
```


### updates schemas from bo4e-schema
```
git clone git@github.com:conuti-gmbh/bo4e-schema.git && \
cp -r bo4e-schema/schemas components && \
rm -rf bo4e-schema/ && \
python3 remove_unused_key_in_schemas.py && \ 
nodemon
```

## How to install swagger-cli
```
npm install -g swagger-cli
```