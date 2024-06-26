import flet as ft
import requests
import uuid


ENDPOINT = "REPLACE_WITH_ENDPOINT"
API_KEY = "REPLACE_WITH_API_KEY"


USER_ID = uuid.uuid4()


def post_user_points(user_id, points):
    # Prepare the headers
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Prepare the data
    data = {
        'userId': str(user_id),  # Convert UUID to string if it's not already
        'points': points
    }

    try:
        # Make the POST request
        response = requests.post(f"{ENDPOINT}/report", json=data, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the response JSON if successful
        return response.json()
    
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        return None

# Example usage
def post_report(points):
    # Generate a random UUID for this example
    result = post_user_points(USER_ID, points)
    if result:
        print("Successfully posted data:", result)
    else:
        print("Failed to post data")

def main(page: ft.Page):
    page.title = "JumPyMorgancker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # Set window dimensions to mimic a phone
    page.window.width = 720  # typical phone width
    page.window.height = 1280  # typical phone height
    page.window.resizable = False  # optional: prevent window resizing

    def show_notification(message):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # Header
    header = ft.AppBar(
        title=ft.Text("JumPyMorgan"),
        center_title=True,
        bgcolor=ft.colors.BLUE_600,
    )

    # Dashboard
    steps_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Steps", size=20),
                ft.Text("10,000", size=40, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
        ),
    )

    calories_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Calories", size=20),
                ft.Text("500", size=40, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
        ),
    )

    dashboard = ft.Row([steps_card, calories_card], alignment=ft.MainAxisAlignment.CENTER)

    # Activity List
    activity_list = ft.ListView(
        controls=[
            ft.ListTile(title=ft.Text("Morning Run"), subtitle=ft.Text("30 minutes")),
            ft.ListTile(title=ft.Text("Weightlifting"), subtitle=ft.Text("45 minutes")),
            ft.ListTile(title=ft.Text("Evening Walk"), subtitle=ft.Text("20 minutes")),
        ],
        expand=1,
    )

    def on_add_activity(e):
        points = 100  # You might want to make this dynamic based on user input

        result = post_user_points(USER_ID, points)
        if result:
            show_notification(f"Activity added successfully! Points: {points}")
        else:
            show_notification("Failed to add activity. Please try again.")

    # Add Activity Button
    add_activity_button = ft.FloatingActionButton(
        icon=ft.icons.SEND, text="Report Data", on_click=on_add_activity
    )

    # Main layout
    page.add(
        header,
        ft.Column([
            dashboard,
            ft.Text("Recent Activities", size=20, weight=ft.FontWeight.BOLD),
            activity_list,
        ], expand=True, spacing=20),
        add_activity_button,
    )

ft.app(target=main)