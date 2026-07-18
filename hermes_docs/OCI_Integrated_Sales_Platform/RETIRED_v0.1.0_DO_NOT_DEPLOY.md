# v0.1.0 retired — do not deploy

Independent QA classified v0.1.0 as **PRODUCTION NO-GO**. Do not install or expose it.

Reasons include missing OIDC/RBAC and Oracle runtime integration, unsafe privileged-script assumptions, unverified DB migration/recovery, and incomplete UAT/security evidence.

Use v0.1.1 only for localhost preview. Its production preflight fails closed and its Nginx template denies remote access. Production remains prohibited until G0–G8 gates pass.
