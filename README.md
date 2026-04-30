# 🚀 Snowflake SPCS + Streamlit (General Guide)

This guide walks through:

* Creating an image repository
* Building & pushing a container
* Deploying a service (SPCS)
* Accessing it (internal + public)
* Connecting from Streamlit

---

# 📦 1. Create Image Repository

```sql
SHOW IMAGE REPOSITORIES;

CREATE IMAGE REPOSITORY <repo_name>;
```

---

# 🔎 How to Get Your Registry URL

Run:

```sql
SHOW IMAGE REPOSITORIES;
```

You’ll see something like:

```
<account>.registry.snowflakecomputing.com/<database>/<schema>/<repo_name>
```

### ✅ Registry URL Format

```text
<account_identifier>.registry.snowflakecomputing.com
```

---

### 🔍 How to find `<account_identifier>`

Run:

```sql
SELECT CURRENT_ACCOUNT();
```

Example output:

```
NSZZCNF-RH51888
```

👉 Convert to lowercase:

```
nszzcnf-rh51888
```

---

### ✅ Final Image Path Format

```text
<account>.registry.snowflakecomputing.com/<db>/<schema>/<repo>/<image>:<tag>
```

Example:

```text
nszzcnf-rh51888.registry.snowflakecomputing.com/my_db/public/my_repo/my_app:latest
```

---

# 🐳 2. Build & Push Docker Image

```bash
docker build -t my-app:latest .

docker tag my-app:latest \
<account>.registry.snowflakecomputing.com/<db>/<schema>/<repo>/my-app:latest

docker push \
<account>.registry.snowflakecomputing.com/<db>/<schema>/<repo>/my-app:latest
```

---

# ⚙️ 3. Create Compute Pool

```sql
CREATE COMPUTE POOL <pool_name>
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;

SHOW COMPUTE POOLS;
```

---

# 🗄️ 4. Create Database (if needed)

```sql
CREATE DATABASE <db_name>;
```

---

# 🚀 5. Create Service (SPCS)

```sql
CREATE SERVICE <service_name>
IN COMPUTE POOL <pool_name>
FROM SPECIFICATION $$
spec:
  containers:
    - name: app
      image: <full_image_path>
      resources:
        requests:
          cpu: "1"
          memory: "2Gi"
  endpoints:
    - name: api
      port: 8000
      public: true
$$;
```

---

# 🔍 6. Verify Deployment

```sql
SHOW SERVICES;

SHOW ENDPOINTS IN SERVICE <service_name>;
```

---

# 🌐 7. Endpoints

## ✅ Public Endpoint

```
https://<random>.snowflakecomputing.app
```

* Accessible externally
* Requires **External Access Integration** for Streamlit

---

## ✅ Internal Endpoint (Recommended)

```
http://<service-name>.<namespace>.svc.spcs.internal:<port>
```

### Example:

```
http://my-service.bq24.svc.spcs.internal:8000
```

---

# 🔐 8. Enable Public Access (Optional)

Only needed if Streamlit calls **public URL**

---

## Step 1: Network Rule

```sql
CREATE OR REPLACE NETWORK RULE <rule_name>
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('<public-domain>:443');
```

---

## Step 2: External Access Integration

```sql
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION <integration_name>
  ALLOWED_NETWORK_RULES = (<rule_name>)
  ENABLED = TRUE;
```

---

## Step 3: Attach to Streamlit

```sql
ALTER STREAMLIT <streamlit_app_name>
SET EXTERNAL_ACCESS_INTEGRATIONS = (<integration_name>);
```

---

# 🖥️ 9. Streamlit Example (Internal Call)

```python
import streamlit as st
import requests

BASE_URL = "http://<service>.<namespace>.svc.spcs.internal:<port>"

name = st.text_input("Enter your name")

if st.button("Send") and name:
    try:
        res = requests.get(f"{BASE_URL}/process", params={"name": name})
        st.success(res.json().get("message") if res.ok else res.text)
    except:
        st.error("Service unreachable")
```

---

# 🧠 Key Concepts

### Internal DNS Pattern

```
<service-name>.<namespace>.svc.spcs.internal:<port>
```

---

### Public vs Internal

| Type     | Use Case                | Recommended       |
| -------- | ----------------------- | ----------------- |
| Internal | Snowflake → SPCS        | ✅ Yes             |
| Public   | External apps / browser | ⚠️ Only if needed |

---

# ⚠️ Common Pitfalls

### ❌ Service unreachable

* Wrong namespace
* Missing port
* Service not running

---

### ❌ Connection error (Streamlit)

* Using public URL without integration

---

### ❌ API not responding

* App not bound to `0.0.0.0`
* Wrong route path

---

# ✅ Best Practices

* Prefer **internal endpoint** for Snowflake-native apps
* Keep services **private unless required**
* Use **external access only when necessary**



Just tell me 👍
