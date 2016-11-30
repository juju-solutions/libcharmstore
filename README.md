# CharmStore Python Library

The environment variables CS\_API\_URL and CS\_API\_TIMEOUT can be set to
repectively set the Charm Store endpoint URL and how long to wait before a
Charm Store query times out.

```bash
export CS_API_URL=https://api.jujucharms.com/v4
export CS_API_TIMEOUT=200
```

```python
from charmstore import CharmStore, Charm, Bundle
```
