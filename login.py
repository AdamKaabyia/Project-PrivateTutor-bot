
from config import *

# Handlers for the login conversation
async def login_start(update: Update, context: CallbackContext) -> int:
    """Start the login process."""
    await update.message.reply_text("Please enter your email:")
    return LOGIN_EMAIL


async def login_email(update: Update, context: CallbackContext) -> int:
    """Collect the email and ask for the password."""
    context.user_data["email"] = update.message.text
    await update.message.reply_text("Now, please enter your password:")
    return LOGIN_PASSWORD


async def login_password(update: Update, context: CallbackContext) -> int:
    """Collect the password and complete the login."""
    context.user_data["password"] = update.message.text

    # Prepare payload for the API
    payload = {"email": context.user_data["email"], "password": context.user_data["password"]}

    # Send request to the API
    response = requests.post(f"{API_BASE_URL}/users/login", json=payload)
    if response.status_code == 200:
        user = response.json()
        user_id = user["id"]
        user_sessions[update.effective_user.id] = user_id
        await update.message.reply_text("Login successful! Use /role to choose a role (Teacher or Student).")
    else:
        error_message = response.json().get("detail", "An error occurred.")
        await update.message.reply_text(f"Login failed: {error_message}")

    return ConversationHandler.END


async def login_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the login process."""
    await update.message.reply_text("Login process canceled.")
    return ConversationHandler.END
