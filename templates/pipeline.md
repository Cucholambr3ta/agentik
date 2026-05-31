# Templates para AGENTIK

## Pipeline Template
```
/xdd-start
<comando>
/gate assert <condición>
/cierre-fase
```

## Receipt Template
```json
{
  "id": "uuid",
  "timestamp": "ISO-8601",
  "action": "string",
  "actor": "agentik",
  "result": "success|failure",
  "pipeline": "string",
  "signature": "hmac-sha256"
}
```
