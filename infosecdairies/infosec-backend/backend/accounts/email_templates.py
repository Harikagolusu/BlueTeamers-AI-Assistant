import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def _send_html_email(subject: str, text_body: str, html_body: str, to_email: str, *, from_email: str, context: str) -> None:
    """Send HTML email with plain text fallback."""
    try:
        logger.info(
            "Sending HTML email (%s): EMAIL_BACKEND=%s DEFAULT_FROM_EMAIL=%s to=%s",
            context,
            getattr(settings, "EMAIL_BACKEND", None),
            getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to_email,
        )
        
        # Format from_email with sender name if not already formatted
        if "<" not in from_email:
            from_email = f"Infosec Dairies <{from_email}>"
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[to_email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        
    except Exception:
        logger.exception("Failed to send email (%s)", context)


def get_otp_email_template(code: str, brand_color: str = "#0891b2") -> tuple[str, str]:
    """Return (text_body, html_body) for OTP email."""
    logo_url = "https://www.infosecdairies.io/assets/infosecdairies-logo-3K6bivW-.png"
    
    text_body = f"""Welcome to Infosec Dairies!

Your email verification code is: {code}

Enter this code to complete your registration.

This code expires in 10 minutes.

If you didn't request this code, please ignore this email.

—
Infosec Dairies Team"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email - Infosec Dairies</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%; background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, {brand_color} 0%, #06b6d4 100%); padding: 40px 30px; text-align: center;">
                            <img src="{logo_url}" alt="Infosec Dairies" width="100" height="100" style="margin-bottom: 15px; border-radius: 16px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">Infosec Dairies</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Secure Your Digital Future</p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #f8fafc; margin: 0 0 20px 0; font-size: 24px; font-weight: 600;">Verify Your Email</h2>
                            <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                                Welcome! Use the verification code below to complete your registration:
                            </p>
                            
                            <!-- Code Box -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0;">
                                <tr>
                                    <td style="background: linear-gradient(135deg, {brand_color}20 0%, #06b6d420 100%); border: 2px solid {brand_color}; border-radius: 12px; padding: 30px; text-align: center;">
                                        <p style="color: #64748b; font-size: 14px; margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 2px;">Your Verification Code</p>
                                        <div style="font-size: 42px; font-weight: 800; color: #ffffff; letter-spacing: 8px; font-family: 'Courier New', monospace; text-shadow: 0 0 20px {brand_color}80;">{code}</div>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 25px 0;">
                                ⏰ This code expires in <strong style="color: {brand_color};">10 minutes</strong>
                            </p>
                            
                            <p style="color: #64748b; font-size: 13px; line-height: 1.5; margin: 20px 0 0 0; border-top: 1px solid #334155; padding-top: 20px;">
                                If you didn't request this code, please ignore this email. Your account security is important to us.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #0f172a; padding: 30px; text-align: center; border-top: 1px solid #1e293b;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">
                                © 2026 Infosec Dairies. All rights reserved.<br>
                                <span style="color: {brand_color};">Securing the digital world, one learner at a time.</span>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return text_body, html_body


def get_payment_receipt_template(course_title: str, amount: str, order_id: str, payment_id: str, user_name: str) -> tuple[str, str]:
    """Return (text_body, html_body) for payment receipt email."""
    logo_url = "https://www.infosecdairies.io/assets/infosecdairies-logo-3K6bivW-.png"
    
    text_body = f"""Payment Confirmation

Hi {user_name},

We received your payment for: {course_title}

Amount: ₹{amount}
Razorpay Order ID: {order_id}
Razorpay Payment ID: {payment_id}

You now have lifetime access to the course.

Thank you for learning with us!

—
Infosec Dairies Team"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Receipt - Infosec Dairies</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%; background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 30px; text-align: center;">
                            <img src="{logo_url}" alt="Infosec Dairies" width="100" height="100" style="margin-bottom: 15px; border-radius: 16px; background: white; padding: 8px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700;">Payment Successful!</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Your enrollment is confirmed</p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                                Hi <strong style="color: #f8fafc;">{user_name}</strong>,
                            </p>
                            <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                Thank you for your purchase! Here's your payment receipt:
                            </p>
                            
                            <!-- Receipt Box -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #0f172a; border-radius: 12px; margin: 30px 0;">
                                <tr>
                                    <td style="padding: 25px;">
                                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="padding: 10px 0; border-bottom: 1px solid #1e293b;">
                                                    <span style="color: #64748b; font-size: 14px;">Course</span>
                                                    <div style="color: #f8fafc; font-size: 18px; font-weight: 600; margin-top: 5px;">{course_title}</div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 15px 0; border-bottom: 1px solid #1e293b;">
                                                    <span style="color: #64748b; font-size: 14px;">Amount Paid</span>
                                                    <div style="color: #10b981; font-size: 24px; font-weight: 700; margin-top: 5px;">₹{amount}</div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 15px 0; border-bottom: 1px solid #1e293b;">
                                                    <span style="color: #64748b; font-size: 14px;">Order ID</span>
                                                    <div style="color: #94a3b8; font-size: 14px; font-family: monospace; margin-top: 5px;">{order_id}</div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 15px 0 10px 0;">
                                                    <span style="color: #64748b; font-size: 14px;">Payment ID</span>
                                                    <div style="color: #94a3b8; font-size: 14px; font-family: monospace; margin-top: 5px;">{payment_id}</div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <div style="background: linear-gradient(135deg, #0891b220 0%, #06b6d420 100%); border-left: 4px solid #0891b2; padding: 20px; border-radius: 8px; margin: 30px 0;">
                                <p style="color: #f8fafc; font-size: 15px; margin: 0; line-height: 1.5;">
                                    🎓 <strong>You now have lifetime access to this course!</strong><br>
                                    <span style="color: #94a3b8; font-size: 14px;">Start learning anytime from your dashboard.</span>
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #0f172a; padding: 30px; text-align: center; border-top: 1px solid #1e293b;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">
                                © 2026 Infosec Dairies. All rights reserved.<br>
                                <span style="color: #0891b2;">Questions? Reply to this email.</span>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return text_body, html_body


def get_certificate_template(download_url: str, course_name: str = "your course") -> tuple[str, str]:
    """Return (text_body, html_body) for certificate email."""
    logo_url = "https://www.infosecdairies.io/assets/infosecdairies-logo-3K6bivW-.png"
    
    text_body = f"""🎉 Congratulations!

You have successfully completed {course_name}!

Your certificate is ready for download:
{download_url}

This is a significant achievement. Keep up the great work!

—
Infosec Dairies Team

P.S. Share your achievement on LinkedIn and tag us!"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certificate Ready - Infosec Dairies</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%; background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 50px 30px; text-align: center;">
                            <img src="{logo_url}" alt="Infosec Dairies" width="100" height="100" style="margin-bottom: 20px; border-radius: 16px; background: white; padding: 8px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 700;">Congratulations!</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 18px;">You've earned your certificate</p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px; text-align: center;">
                            <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                                You have successfully completed
                            </p>
                            <h2 style="color: #f8fafc; margin: 0 0 30px 0; font-size: 24px; font-weight: 700;">{course_name}</h2>
                            
                            <div style="background: linear-gradient(135deg, #f59e0b20 0%, #d9770620 100%); border: 2px solid #f59e0b; border-radius: 12px; padding: 30px; margin: 30px 0;">
                                <p style="color: #f59e0b; font-size: 14px; margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 2px;">✨ Achievement Unlocked</p>
                                <p style="color: #f8fafc; font-size: 18px; margin: 0; font-weight: 600;">Course Completion Certificate</p>
                            </div>
                            
                            <!-- Download Button -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 35px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{download_url}" style="display: inline-block; background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%); color: #ffffff; text-decoration: none; padding: 18px 40px; border-radius: 10px; font-size: 16px; font-weight: 600; box-shadow: 0 10px 25px -5px rgba(8, 145, 178, 0.4);">
                                            📥 Download Your Certificate
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #64748b; font-size: 13px; margin: 20px 0 0 0; line-height: 1.5;">
                                Or copy this link:<br>
                                <span style="color: #94a3b8; font-family: monospace; word-break: break-all;">{download_url}</span>
                            </p>
                            
                            <div style="background: #0f172a; border-radius: 8px; padding: 20px; margin: 30px 0 0 0;">
                                <p style="color: #f8fafc; font-size: 15px; margin: 0 0 10px 0;">🚀 What's next?</p>
                                <p style="color: #94a3b8; font-size: 14px; margin: 0; line-height: 1.5;">
                                    Share your achievement on LinkedIn and tag us!<br>
                                    <span style="color: #f59e0b;">#InfosecDairies #CyberSecurity</span>
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #0f172a; padding: 30px; text-align: center; border-top: 1px solid #1e293b;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">
                                © 2026 Infosec Dairies. All rights reserved.<br>
                                <span style="color: #f59e0b;">Keep learning, keep growing! 🌟</span>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return text_body, html_body
