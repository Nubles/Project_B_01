# Catalyst League Task Checker

This is a web-based tool designed to help players track their progress in the Catalyst League. It allows users to look up their RuneScape username and see a comprehensive list of their completed and incomplete tasks, sorted by difficulty tier. The application is designed to be used as a local app within the Alt1 Toolkit.

## Features

*   **Dynamic Task Tracking:** Enter your RuneScape username to fetch your latest task completion data directly from the official RuneScape Wiki API.
*   **Tabbed Interface:**
    *   **All Tasks:** View all league tasks.
    *   **Pinned Tasks:** Keep a separate list of tasks you want to focus on.
    *   **Random Task:** Get a randomly selected task to work on next.
*   **Search and Filtering:**
    *   **Search Bar:** Quickly find tasks by searching for keywords in their titles.
    *   **Filter Dropdowns:** Filter the task list by `Tier`, `Location`, and `Skill` requirements.
    *   **Hide Completed Toggle:** Clean up your view by hiding tasks you've already completed.
*   **Pinned Tasks:**
    *   Pin any uncompleted task by clicking the pin icon next to it.
    *   Pinned tasks appear in the "Pinned Tasks" tab for easy access.
    *   Your pinned tasks are saved in your browser's local storage, so they persist between sessions.
    *   Tasks are automatically removed from the pinned list upon completion.
*   **Random Task Generator:**
    *   Click the "Get Random Task" button to be assigned a random, uncompleted task.
    *   The task appears in a persistent card within the tab, allowing you to browse other tabs without losing it.
    *   The card includes a "Pin it" button and a "Complete it" button to temporarily mark the task as done for your session.
    *   If all tasks are completed, a celebratory message with a fireworks animation is displayed.
*   **Wiki Integration:**
    *   Tasks with specific quest, skill, or achievement diary requirements will have automatically generated links to the relevant RuneScape Wiki page, making it easy to find guides and information.

## How to Install in Alt1

1.  **Copy the Installation URL:**
    *   Copy the following URL. This is the direct link to install the app in Alt1:
        ```
        alt1://addapp/https://nubles.github.io/Project_B_01/appconfig.json
        ```

2.  **Add the App to Alt1:**
    *   Make sure the Alt1 Toolkit is running.
    *   Press `Alt` + `1` on your keyboard to open the Alt1 browser.
    *   Paste the URL you copied into the address bar at the top of the Alt1 browser and press Enter.

3.  **Confirm Installation:**
    *   Alt1 will display the app's information.
    *   Click the "Add App" button to install it.

The app will now be added to your Alt1 application list and is ready to use.