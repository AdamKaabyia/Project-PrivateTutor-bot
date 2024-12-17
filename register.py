from config import *

# Handlers for the register conversation
async def register_start(update: Update, context: CallbackContext) -> int:
    """Start the registration process."""
    await update.message.reply_text("Welcome to the registration process! Please enter your name:")
    return REGISTER_NAME


async def register_name(update: Update, context: CallbackContext) -> int:
    """Collect the name and ask for the email."""
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Great! Now, please enter your email:")
    return REGISTER_EMAIL


async def register_email(update: Update, context: CallbackContext) -> int:
    """Collect the email and ask for the username."""
    context.user_data["email"] = update.message.text
    await update.message.reply_text("Thanks! Please enter your username:")
    return REGISTER_USERNAME


async def register_username(update: Update, context: CallbackContext) -> int:
    """Collect the username and ask for the password."""
    context.user_data["username"] = update.message.text
    await update.message.reply_text("Almost done! Please enter your password:")
    return REGISTER_PASSWORD


async def register_password(update: Update, context: CallbackContext) -> int:
    """Collect the password and complete the registration."""
    context.user_data["password"] = update.message.text

    # Prepare payload for the API
    payload = {
        "name": context.user_data["name"],
        "email": context.user_data["email"],
        "username": context.user_data["username"],
        "password": context.user_data["password"],
        "roles": ["None"],  # Default role is "None"
    }

    # Send request to the API
    response = requests.post(f"{API_BASE_URL}/users/", json=payload)
    if response.status_code == 201:
        await update.message.reply_text("Registration successful! You can now log in with /login.")
    else:
        error_message = response.json().get("detail", "An error occurred.")
        await update.message.reply_text(f"Registration failed: {error_message}")

    return ConversationHandler.END


async def register_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the registration process."""
    await update.message.reply_text("Registration process canceled.")
    return ConversationHandler.END
