run-local-dynamodb:
	mkdir -p dynamodb_local_latest/tests && \
	rm -Rf dynamodb_local_latest/tests/* && \
	cd dynamodb_local_latest && \
	java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -dbPath tests

run-local-chalice:
	cd employees_api && pipenv run chalice local --port 8001

test:
	pipenv run pytest -vvs
