import jwt

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyq+dO6rKTwPxCHIZwViV
pbzQEBFnLHpCgU4mH6Z2/reTyPhfBCL6xR2JJNQiC6IXBuZlFWPgRaxMSgbwPjzA
asvjmWyHmbujs6Sn3kYO6dYN3i+DZG5rFbPaZU32Z8sSEvcfsUfzWtwLoJIsZ0sh
NEU3DOfFFJar5rmGQ90lYxGWo4keh+qxFgi8LibOAfuRS3gZF4llNpWOoqJIQyeK
CGDZEG2kIqI+pOkh8i6RBBwxIu+HRijRZ9JuM+plI28FBndtRYSWQ/hCgl9YuXyP
SiDme3g5GBFI7Vps53U5xJbTvKdxHx6wZMEumvZJn55WeOQ/DHxAAYEEPRjAFU/B
jwIDAQAB
-----END PUBLIC KEY-----"""

payload = {
  "sub": "2",
  "aud": [
    "fastapi-users:auth"
  ],
  "exp": 1808801547,
  "pk": PUBLIC_KEY
}



encoded = jwt.encode(payload, PUBLIC_KEY, algorithm='HS256')

print(encoded)