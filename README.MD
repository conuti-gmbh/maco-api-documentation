## How to generate a single openapi.yaml file from multiple openapi.yaml files using swagger-cli
the files will be merged into one file. The files are located in the components/schemas/v1 directory. The merged file will be located in the _build directory.
```
_build/bo4e-openapi.yaml
```

### requiments
- nodejs
- nodemon
- swagger-cli
- python3


### Developing
if you need to change some thing in this repo, you can run the following command to start the development server.
```
nodemon
```

### Build _build/openapi.yaml
```
swagger-cli bundle bo4e-openapi.yaml --outfile _build/bo4e-openapi.yaml --dereference  --type yaml
```

## How to install swagger-cli
```
npm install -g swagger-cli
```

## How to install nodemon
```
npm install -g nodemon
```

## How to install nodejs
```
sudo apt install nodejs
```

## How to install python3
```
sudo apt install python3
```

## Notes
All files in components/schemas/v1 are generated from github.com:conuti-gmbh/bo4e-schema.git. We try to keep them up to date.

### run this updates schemas from bo4e-schema
```
git clone git@github.com:conuti-gmbh/bo4e-schema.git && \
cp -r bo4e-schema/schemas components && \
rm -rf bo4e-schema/ && \
python3 remove_unused_key_in_schemas.py && \ 
nodemon
```