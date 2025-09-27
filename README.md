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

To use this tool within the Alt1 Toolkit, you need to run a simple local web server on your computer. Here’s how to do it using Python:

1.  **Ensure you have Python:** Most systems have Python pre-installed. You can check by opening a command prompt (or Terminal on Mac) and typing `python --version`. If it's not installed, download it from [python.org](https://python.org).

2.  **Navigate to the App Directory:**
    *   Open a command prompt or terminal.
    *   Use the `cd` command to navigate to the folder where you have saved the app files (`index.html`, `script.js`, `style.css`, `tasks.json`). For example:
        ```bash
        cd C:\path\to\your\app\folder
        ```

3.  **Start the Local Server:**
    *   In the command prompt, run the following command:
        ```bash
        python -m http.server
        ```
    *   You should see a message like `Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...`. This means your local server is running. Keep this command prompt window open.

4.  **Add the App to Alt1:**
    *   Open the Alt1 Toolkit.
    *   In the Alt1 menu, click on "Add App".
    *   In the "App URL" field, enter the following address:
        ```
        http://localhost:8000
        ```
    *   Give the app a name, like "Catalyst Task Checker".
    *   Click "OK" to save the app.

The app should now appear in your list of Alt1 applications and is ready to use! Just click on it to open it within Alt1.