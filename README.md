# Cafe EPOS API

## Get started with Docker

### Clone Repo
```bash
git clone git@github.com:bbell2411/cafe-epos.git
cd cafe-epos
```

### Build and Run
```bash
# Build containers
make build

# Start the server
make up
```
### In a new terminal, run setup
```bash
# Run migrations and seed data
make setup
```

### Run Tests 
```bash
make test
```

## API Examples

All requests require header: `X-Api-Key: demo`

### Create a tab
```bash
curl -X POST http://localhost:8000/api/tabs/ \
  -H "X-Api-Key: demo" \
  -H "Content-Type: application/json" \
  -d '{"table_number": 12, "covers": 3}'
```
### Get tab details
```bash
curl http://localhost:8000/api/tabs/1/ \
  -H "X-Api-Key: demo"
  ```
### Add item to tab
```bash
curl -X POST http://localhost:8000/api/tabs/1/items/ \
  -H "X-Api-Key: demo" \
  -H "Content-Type: application/json" \
  -d '{"menu_item_id": 1, "qty": 2}'
  ```
### Create Payment Intent
```bash
curl -X POST http://localhost:8000/api/tabs/1/payment_intent/ \
-H "X-Api-Key: demo"
```
### Confirm Payment
```bash 
curl -X POST http://localhost:8000/api/tabs/1/take_payment/ \
  -H "X-Api-Key: demo" \
  -H "Content-Type: application/json" \
  -d '{"intent_id": "pi_abc123"}'
  ```
## Notes
- VAT calculated per line item then rounded to nearest pence
- Service charge is 10% of subtotal, recalculated when items added
- Menu items are pre-seeded via management command
- Tab status is either OPEN or PAID 
- Made sure money is stored as integer pence to avoid decimal issues
- Mock payment gateway returns success unless intent_id ends with "13" to test error handling.
- Once a tab is paid, it can't be modified

