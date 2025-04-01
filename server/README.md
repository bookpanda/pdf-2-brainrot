```bash
curl -X PUT "presigned_url" \
     -H "Content-Type: application/pdf" \
     --data-binary @./test.pdf
```