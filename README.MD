## How to generate a single openapi.yaml file from multiple openapi.yaml files using swagger-cli

```
swagger-cli bundle openapi.yaml --outfile _build/openapi.yaml --type yaml
```

```
swagger-cli bundle openapi.yaml --outfile _build/openapi.yaml --dereference  --type yaml
```


## How to install swagger-cli
```
npm install -g swagger-cli
```