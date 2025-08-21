import time

from src.services.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test rate limiter token bucket functionality"""

    def test_allows_first_request(self):
        """First request should always be allowed"""
        rate_limiter = RateLimiter()

        result = rate_limiter.is_allowed("192.168.1.1", 5)

        assert result is True

    def test_blocks_when_tokens_exhausted(self):
        """Should block requests when all tokens are consumed"""
        rate_limiter = RateLimiter()
        client_ip = "192.168.1.2"
        rate_limit = 3

        # Use up all tokens
        for _ in range(rate_limit):
            assert rate_limiter.is_allowed(client_ip, rate_limit) is True

        # Next request should be blocked
        result = rate_limiter.is_allowed(client_ip, rate_limit)
        assert result is False

    def test_different_ips_have_separate_buckets(self):
        """Different IPs should have independent rate limits"""
        rate_limiter = RateLimiter()
        rate_limit = 2

        # Exhaust tokens for first IP
        for _ in range(rate_limit):
            assert rate_limiter.is_allowed("192.168.1.1", rate_limit) is True

        # First IP should be blocked
        assert rate_limiter.is_allowed("192.168.1.1", rate_limit) is False

        # Second IP should still work
        assert rate_limiter.is_allowed("192.168.1.2", rate_limit) is True

    def test_tokens_refill_over_time(self):
        """Tokens should refill after time passes"""
        rate_limiter = RateLimiter()
        client_ip = "192.168.1.3"
        rate_limit = 5

        # Exhaust all tokens
        for _ in range(rate_limit):
            assert rate_limiter.is_allowed(client_ip, rate_limit) is True

        # Should be blocked immediately
        assert rate_limiter.is_allowed(client_ip, rate_limit) is False

        # Wait for tokens to refill (1 second = 5 tokens at 5/second rate)
        time.sleep(1.1)

        # Should be allowed again
        assert rate_limiter.is_allowed(client_ip, rate_limit) is True

    def test_partial_refill(self):
        """Should allow partial token refill"""
        rate_limiter = RateLimiter()
        client_ip = "192.168.1.4"
        rate_limit = 10

        # Exhaust all tokens
        for _ in range(rate_limit):
            assert rate_limiter.is_allowed(client_ip, rate_limit) is True

        # Wait for partial refill (0.5 seconds = 5 tokens at 10/second)
        time.sleep(0.5)

        # Should allow 5 more requests
        for _ in range(5):
            assert rate_limiter.is_allowed(client_ip, rate_limit) is True

        # 6th request should be blocked
        assert rate_limiter.is_allowed(client_ip, rate_limit) is False

    def test_bucket_cleanup_removes_old_entries(self):
        """Cleanup should remove old bucket entries"""
        rate_limiter = RateLimiter()

        # Create some buckets
        rate_limiter.is_allowed("192.168.1.10", 5)
        rate_limiter.is_allowed("192.168.1.11", 5)

        assert len(rate_limiter.buckets) == 2

        # Run cleanup with very short max_age
        rate_limiter.cleanup_old_buckets(max_age=0)

        # All buckets should be removed
        assert len(rate_limiter.buckets) == 0
