from app.core.security import pwd_context

get_password_hash = pwd_context.hash
verify_password = pwd_context.verify

