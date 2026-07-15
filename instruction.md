1. Read and parse every request from /app/access.log

2. Compute the following values:
   - total_requests — the total number of requests.
   - unique_ips — the number of unique client IP addresses.
   - top_path — the most frequently requested path.

3. Creating a jSON object which contains exactly these feilds:
   - total_requests
   - unique_ips
   - top_path

4. Saving JSON report as in /app/report.json


# The task is considered complete only if all of the following are true:

1. /app/report.json is created.
2. /app/report.json is not empty.
3. /app/report.json contains valid JSON.
4. The JSON contains the required fields:
   - total_requests
   - unique_ips
   - top_path
5. total_requests matches the value computed from 
  /app/access.log.
7. unique_ips matches the value computed from /app/access.log.
8. top_path matches the most requested path computed from /app/access.log