"""
Security Headers Middleware
Adds CSP and Permissions-Policy headers to all responses
"""


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy
        # Strict policy that only allows resources from same origin and specific trusted domains
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://checkout.razorpay.com https://www.googletagmanager.com https://www.google-analytics.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.infosecdairies.io https://www.google-analytics.com; "
            "frame-src https://checkout.razorpay.com; "
            "frame-ancestors 'none'; "  # Prevents clickjacking via CSP
            "base-uri 'self'; "
            "form-action 'self'; "
            "upgrade-insecure-requests;"
        )
        response['Content-Security-Policy'] = csp_policy
        
        # Permissions Policy (formerly Feature-Policy)
        # Restricts access to browser features
        permissions_policy = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(self), "  # Only allow payment on same origin
            "usb=()"
        )
        response['Permissions-Policy'] = permissions_policy
        
        return response
