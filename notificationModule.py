from plyer import notification

# Function calling system notification
def show_notification(title:str, message:str):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=1,
    )