## server init
Receive:
```json
{
    "state": "SERVER_INIT"
}
```
## PREGAME
Receive:
```json
{
    "state": "PREGAME",
    "self": {
        "name": "Player1",
        "major": "Major1",
        "allies": "Ally1",
        "ready": True,
    },
    "opponent": {
        "name": "Player2",
        "major": "Major2",
        "allies": "Ally2",
        "ready": False
    },
}
```

Send:
```python
"READY" |
"NOT_READY" |
```

## RESCHEDULE
Receive:
```json
{
    "state": "RESCHEDULE",
    "TODO"
}
```