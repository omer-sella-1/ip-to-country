import time
from threading import Lock


class RateLimiter:
    def __init__(self):
        self.buckets = {}
        self.lock = Lock()

    def _get_or_create_bucket(self, client_ip, rate_limit):
        with self.lock:
            if client_ip in self.buckets:
                return self.buckets[client_ip]
            else:
                new_bucket = {
                    "tokens": rate_limit,
                    "last_refill": time.time(),
                    "max_tokens": rate_limit,
                    "refill_rate": rate_limit,
                    "lock": Lock(),
                }
                self.buckets[client_ip] = new_bucket
                return new_bucket

    def _refill_bucket(self, bucket):
        current_time = time.time()
        time_elapsed = current_time - bucket["last_refill"]

        new_tokens = time_elapsed * bucket["refill_rate"]

        bucket["tokens"] += new_tokens

        if bucket["tokens"] > bucket["max_tokens"]:
            bucket["tokens"] = bucket["max_tokens"]

        bucket["last_refill"] = current_time

    def is_allowed(self, client_ip, rate_limit):
        bucket = self._get_or_create_bucket(client_ip, rate_limit)
        with bucket["lock"]:
            self._refill_bucket(bucket)

            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                return True
            else:
                return False

    def cleanup_old_buckets(self, max_age=3600):
        current_time = time.time()
        with self.lock:
            expired_keys = [
                key
                for key, bucket in self.buckets.items()
                if current_time - bucket["last_refill"] > max_age
            ]
            for key in expired_keys:
                del self.buckets[key]
