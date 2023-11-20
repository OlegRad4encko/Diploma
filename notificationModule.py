from plyer import notification

# Function calling system notification
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=1,
    )