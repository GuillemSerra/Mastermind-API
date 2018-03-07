# Mastermind-API

## API Description

### Create new game
Request:
```shell
curl --request GET \
  --url http://localhost:8080/game/new 
```
Answer:
```json
{
	"body": {
		"game_id": "5c9f0611fa5ff0ad9ea97e9c69692bd20ee8d1fc"
	},
	"code": 0,
	"msg": "ok"
}
```

### Play game
Request:
```shell
curl --request POST \
  --url http://localhost:8080/game/play \
  --header 'content-type: application/json' \
  --data '{
	"game_id": "5c9f0611fa5ff0ad9ea97e9c69692bd20ee8d1fc",
	"guess": ["BLUE", "PURPLE", "RED", "YELLOW"]
}
'
```

Answer:
```json
{
	"body": {
		"black_pegs": 1,
		"white_pegs": 1
	},
	"code": 0,
	"msg": "ok"
}
```

### Get game history
Request:
```shell
curl --request GET \
  --url http://localhost:8080/game/history \
  --header 'content-type: application/json' \
  --data '{
	"game_id": "5c9f0611fa5ff0ad9ea97e9c69692bd20ee8d1fc"
}
'
```

Answer:
```json
{
	"body": [
		{
			"guess": [
				"BLUE",
				"PURPLE",
				"RED",
				"YELLOW"
			],
			"result": {
				"black_pegs": 1,
				"white_pegs": 1
			}
		}
	],
	"code": 0,
	"msg": "ok"
}
```

## Deploy instructions
Before booting up the application you must run the MySQL container so it can create the database:
* `docker-compose up --build mysql`

Otherwise you can just boot up the full stack twice and let the other containers fail:
* `docker-compose up --build`
