# DevOps

## Free up database
The database limit for Hobby-dev is 10k rows.
Clean videos that didn't get downloaded for a while.
```python
DownloadLink.objects.filter(last_download__year__lte=2019).delete()
```
