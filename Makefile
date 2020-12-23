run-local-dynamodb:
	cd dynamodb_local_latest && java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

run-local-chalice:
	cd employees-api && chalice local --port 8001
