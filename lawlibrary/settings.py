import os

from liiweb.settings import *  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent  # noqa

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.environ.get("NODE_PATH") or os.path.join(BASE_DIR, "node_modules"),  # noqa
]

# move peachjam_subs so template inheritance works correctly
INSTALLED_APPS = [x for x in INSTALLED_APPS if x != "peachjam_subs"]  # noqa

INSTALLED_APPS = [
    "lawlibrary.apps.LawlibraryConfig",
    "peachjam_pay",
    "peachjam_subs",
    "peachjam_ml",
    "allauth.socialaccount.providers.openid_connect",
] + INSTALLED_APPS  # noqa

ROOT_URLCONF = "lawlibrary.urls"

JAZZMIN_SETTINGS["site_title"] = "Lawlibrary"  # noqa
JAZZMIN_SETTINGS["site_header"] = "Lawlibrary"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "Lawlibrary.org.za"  # noqa

PEACHJAM["MULTIPLE_LOCALITIES"] = True  # noqa
PEACHJAM["CHAT_ENABLED"] = True  # noqa
PEACHJAM["CHAT_PUBLIC"] = True  # noqa
PEACHJAM["PDFJS_TO_TEXT"] = (  # noqa
    "../peachjam/bin/pdfjs-to-text" if DEBUG else "pdfjs-to-text"  # noqa
)

PEACHJAM_PAY = {
    "PAYFAST_MERCHANT_ID": os.environ.get("PAYFAST_MERCHANT_ID", ""),
    "PAYFAST_MERCHANT_KEY": os.environ.get("PAYFAST_MERCHANT_KEY", ""),
    "PAYFAST_SALT": os.environ.get("PAYFAST_SALT", ""),
    "PAYFAST_SANDBOX": (os.environ.get("PAYFAST_SANDBOX") or "true").lower() == "true",
}

TEMPLATES[0]["OPTIONS"]["context_processors"].append(  # noqa
    "lawlibrary.context_processors.lawlibrary"
)

TEMPLATED_EMAIL_BACKEND = "peachjam.emails.CustomerIOTemplateBackend"

SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_PROVIDERS["openid_connect"] = {  # noqa
    "APPS": [
        {
            "provider_id": "xero",
            "name": "Xero",
            "client_id": os.environ.get("XERO_CLIENT_ID"),
            "secret": os.environ.get("XERO_SECRET"),
            "settings": {
                "hidden": True,
                "server_url": "https://identity.xero.com",
                "token_auth_method": "client_secret_basic",
            },
        }
    ],
    "SCOPE": [
        "openid",
        "profile",
        "email",
        "offline_access",
        "accounting.transactions",
        "accounting.contacts",
        "accounting.attachments",
    ],
}

LANGUAGES = [("en", "English")]

LOGGING["loggers"]["peachjam_pay"] = {"level": "DEBUG" if DEBUG else "INFO"}  # noqa


if not DEBUG:  # noqa
    # Law Library media files are stored on S3 and served via a Cloudflare CDN (via copying to R2).
    # We can therefore set long-lived cache headers and serve them from a custom domain.
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": f"max-age={86400*5}"}
    AWS_S3_CUSTOM_DOMAIN = "media.lawlibrary.org.za"

PEACHJAM["AUTH_OTP"] = True
ACCOUNT_LOGIN_BY_CODE_ENABLED = True