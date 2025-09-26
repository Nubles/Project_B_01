let allTasks = {};

// Fetch all tasks from the JSON file when the script loads
fetch('tasks.json')
    .then(response => response.json())
    .then(data => {
        allTasks = data;
    })
    .catch(error => console.error('Error loading tasks:', error));

document.getElementById('lookup-btn').addEventListener('click', () => {
    const username = document.getElementById('username').value.trim();
    if (!username) {
        alert('Please enter a username.');
        return;
    }

    // Ensure tasks are loaded before proceeding
    if (Object.keys(allTasks).length === 0) {
        alert('Task list is not loaded yet. Please try again in a moment.');
        return;
    }

    const apiUrl = `https://sync.runescape.wiki/runescape/player/${username}/LEAGUE_1`;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading player data...';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(playerData => {
            if (playerData.error) {
                 throw new Error(playerData.error);
            }
            // Correctly access the 'league_tasks' array from the API response.
            const completedTaskIds = new Set(playerData.league_tasks);
            const results = processTasks(completedTaskIds);
            displayResults(results);
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}. Please check the username and try again. The user may not have any league data.</p>`;
        });
});

function processTasks(completedTaskIds) {
    const processed = {};
    for (const tier in allTasks) {
        processed[tier] = {
            completed: [],
            incomplete: [],
            points: 0,
            totalPoints: 0
        };

        allTasks[tier].forEach(task => {
            processed[tier].totalPoints += task.points;
            if (completedTaskIds.has(task.id)) {
                processed[tier].completed.push(task);
                processed[tier].points += task.points;
            } else {
                processed[tier].incomplete.push(task);
            }
        });
    }
    return processed;
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    let totalCompletedPoints = 0;
    let totalPossiblePoints = 0;

    // Order of tiers to display
    const tierOrder = ['Easy', 'Medium', 'Hard', 'Elite', 'Master'];

    tierOrder.forEach(tier => {
        if (results[tier]) {
            const category = results[tier];
            totalCompletedPoints += category.points;
            totalPossiblePoints += category.totalPoints;

            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'task-category';

            const categoryTitle = document.createElement('h2');
            categoryTitle.textContent = `${tier} Tasks (${category.points} / ${category.totalPoints} Points)`;
            categoryDiv.appendChild(categoryTitle);

            const tasks = [...category.completed, ...category.incomplete];

            tasks.forEach(task => {
                const isCompleted = category.completed.includes(task);
                const taskDiv = document.createElement('div');
                taskDiv.className = isCompleted ? 'task completed' : 'task';
                taskDiv.innerHTML = `
                    <div class="task-info">
                        <div class="task-name">${task.task}</div>
                        <div class="task-description">${task.information}</div>
                        <div class="task-requirements"><em>Requirements: ${task.requirements || 'N/A'}</em></div>
                    </div>
                    <div class="task-points">${task.points} pts</div>
                `;
                categoryDiv.appendChild(taskDiv);
            });
            resultsDiv.appendChild(categoryDiv);
        }
    });

    // Add a total summary at the top
    const summaryDiv = document.createElement('div');
    summaryDiv.innerHTML = `<h3>Total Points: ${totalCompletedPoints} / ${totalPossiblePoints}</h3><hr>`;
    resultsDiv.prepend(summaryDiv);
}