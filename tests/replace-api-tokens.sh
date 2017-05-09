DIR="fixtures/ac.cnstrc.com"

perl -pi -e 's/"api_token": "[^"]+"/"api_token": "my-api-token"/; s/"autocomplete_key": "[^"]+"/"autocomplete_key": "my-ac-key"/' test_constructor.py

perl -pi -e 's/autocomplete_key=[\w\-]+/autocomplete_key=my-ac-key/g; s/\[Basic [^\]]+\]/[Basic bXktYXBpLXRva2VuOg==]/g' $DIR/*
