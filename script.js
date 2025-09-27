console.log("script.js loaded");
let allTasks = {};

// Tab switching
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

let playerData = null;
let pinnedTasks = new Set(JSON.parse(localStorage.getItem('pinnedTasks') || '[]'));

// Fetch all tasks from the JSON file when the script loads
fetch('tasks.json')
    .then(response => response.json())
    .then(data => {
        allTasks = data;
        populateFilters();
    })
    .catch(error => console.error('Error loading tasks:', error));

document.getElementById('lookup-btn').addEventListener('click', () => {
    console.log("Get Tasks button clicked");
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
        .then(data => {
            if (data.error) {
                 throw new Error(data.error);
            }
            playerData = data;
            displayResults();
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}. Please check the username and try again. The user may not have any league data.</p>`;
        });
});

function populateFilters() {
    const tiers = new Set();
    const locations = new Set();
    const skills = new Set();

    for (const tier in allTasks) {
        tiers.add(tier);
        allTasks[tier].forEach(task => {
            locations.add(task.locality.split(':')[0]);
            if (task.requirements) {
                const reqs = task.requirements.split(',');
                reqs.forEach(req => {
                    const match = req.trim().match(/^\d+\s+([a-zA-Z]+)/);
                    if (match) {
                        skills.add(match[1]);
                    }
                });
            }
        });
    }

    const tierFilter = document.getElementById('tier-filter');
    Array.from(tiers).sort().forEach(tier => {
        const option = document.createElement('option');
        option.value = tier;
        option.textContent = tier;
        tierFilter.appendChild(option);
    });

    const locationFilter = document.getElementById('location-filter');
    Array.from(locations).sort().forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.textContent = location;
        locationFilter.appendChild(option);
    });

    const skillFilter = document.getElementById('skill-filter');
    Array.from(skills).sort().forEach(skill => {
        const option = document.createElement('option');
        option.value = skill;
        option.textContent = skill;
        skillFilter.appendChild(option);
    });
}


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

function displayResults() {
    if (!playerData) return;

    const completedTaskIds = new Set(playerData.league_tasks);
    const results = processTasks(completedTaskIds);

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    let totalCompletedPoints = 0;
    let totalPossiblePoints = 0;

    const tierOrder = ['Easy', 'Medium', 'Hard', 'Elite', 'Master'];
    const hideCompleted = document.getElementById('hide-completed-toggle').checked;
    const searchTerm = document.getElementById('search-bar').value.toLowerCase();
    const selectedTier = document.getElementById('tier-filter').value;
    const selectedLocation = document.getElementById('location-filter').value;
    const selectedSkill = document.getElementById('skill-filter').value;

    tierOrder.forEach(tier => {
        if (results[tier] && (!selectedTier || tier === selectedTier)) {
            const category = results[tier];
            totalCompletedPoints += category.points;
            totalPossiblePoints += category.totalPoints;

            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'task-category';

            const categoryTitle = document.createElement('h2');
            categoryTitle.textContent = `${tier} Tasks (${category.points} / ${category.totalPoints} Points)`;
            categoryDiv.appendChild(categoryTitle);

            const allTierTasks = [...category.completed, ...category.incomplete].sort((a, b) => a.id - b.id);

            const filteredTasks = allTierTasks.filter(task => {
                const isCompleted = completedTaskIds.has(task.id);
                if (hideCompleted && isCompleted) return false;

                if (searchTerm && !task.task.toLowerCase().includes(searchTerm)) {
                    return false;
                }
                if (selectedLocation && task.locality.split(':')[0] !== selectedLocation) {
                    return false;
                }
                if (selectedSkill) {
                    const skillReq = task.requirements && task.requirements.toLowerCase().includes(selectedSkill.toLowerCase());
                    if (!skillReq) return false;
                }
                return true;
            });


            filteredTasks.forEach(task => {
                const isCompleted = completedTaskIds.has(task.id);
                const taskDiv = document.createElement('div');
                taskDiv.className = isCompleted ? 'task completed' : 'task';

                const taskHeader = document.createElement('div');
                taskHeader.className = 'task-header';

                const taskMainInfo = document.createElement('div');
                taskMainInfo.className = 'task-main-info';
                taskMainInfo.innerHTML = `
                    <div class="task-name">${task.task}</div>
                    <div class="task-description">${task.information}</div>
                    <div class="task-requirements"><em>Requirements: ${task.requirements || 'N/A'}</em></div>
                `;

                const taskActions = document.createElement('div');
                taskActions.className = 'task-actions';

                const taskPoints = document.createElement('div');
                taskPoints.className = 'task-points';
                taskPoints.textContent = `${task.points} pts`;

                const pinIcon = document.createElement('span');
                pinIcon.className = 'pin-icon';
                pinIcon.innerHTML = '&#128204;'; // Pin emoji
                if (pinnedTasks.has(task.id)) {
                    pinIcon.classList.add('pinned');
                }
                pinIcon.onclick = () => togglePinTask(task.id);

                taskActions.appendChild(taskPoints);
                if (!isCompleted) {
                    taskActions.appendChild(pinIcon);
                }

                const wikiLink = generateWikiLink(task);
                if(wikiLink) {
                    const linkDiv = document.createElement('div');
                    linkDiv.className = 'task-link';
                    linkDiv.innerHTML = `<a href="${wikiLink}" target="_blank">Wiki</a>`;
                    taskActions.appendChild(linkDiv);
                }

                taskHeader.appendChild(taskMainInfo);
                taskHeader.appendChild(taskActions);
                taskDiv.appendChild(taskHeader);
                categoryDiv.appendChild(taskDiv);
            });
             if (filteredTasks.length > 0) {
                resultsDiv.appendChild(categoryDiv);
            }
        }
    });

    // Add a total summary at the top
    const summaryDiv = document.createElement('div');
    summaryDiv.innerHTML = `<h3>Total Points: ${totalCompletedPoints} / ${totalPossiblePoints}</h3><hr>`;
    resultsDiv.prepend(summaryDiv);

    displayPinnedTasks();
}

document.getElementById('hide-completed-toggle').addEventListener('change', displayResults);
document.getElementById('search-bar').addEventListener('input', displayResults);
document.getElementById('tier-filter').addEventListener('change', displayResults);
document.getElementById('location-filter').addEventListener('change', displayResults);
document.getElementById('skill-filter').addEventListener('change', displayResults);

function togglePinTask(taskId) {
    if (pinnedTasks.has(taskId)) {
        pinnedTasks.delete(taskId);
    } else {
        pinnedTasks.add(taskId);
    }
    localStorage.setItem('pinnedTasks', JSON.stringify(Array.from(pinnedTasks)));
    displayResults();
    displayPinnedTasks();
}

function displayPinnedTasks() {
    const pinnedResultsDiv = document.getElementById('pinned-results');
    pinnedResultsDiv.innerHTML = '';
    const completedTaskIds = playerData ? new Set(playerData.league_tasks) : new Set();

    // Remove completed tasks from pinned list
    pinnedTasks.forEach(taskId => {
        if (completedTaskIds.has(taskId)) {
            pinnedTasks.delete(taskId);
        }
    });
    localStorage.setItem('pinnedTasks', JSON.stringify(Array.from(pinnedTasks)));


    if (pinnedTasks.size === 0) {
        pinnedResultsDiv.innerHTML = '<p>No tasks have been pinned.</p>';
        return;
    }

    const tasksToDisplay = [];
    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            if (pinnedTasks.has(task.id)) {
                tasksToDisplay.push(task);
            }
        });
    }

    tasksToDisplay.forEach(task => {
        const isCompleted = completedTaskIds.has(task.id);
        const taskDiv = document.createElement('div');
        taskDiv.className = isCompleted ? 'task completed' : 'task';

        const taskHeader = document.createElement('div');
        taskHeader.className = 'task-header';

        const taskMainInfo = document.createElement('div');
        taskMainInfo.className = 'task-main-info';
        taskMainInfo.innerHTML = `
            <div class="task-name">${task.task}</div>
            <div class="task-description">${task.information}</div>
            <div class="task-requirements"><em>Requirements: ${task.requirements || 'N/A'}</em></div>
        `;

        const taskActions = document.createElement('div');
        taskActions.className = 'task-actions';

        const taskPoints = document.createElement('div');
        taskPoints.className = 'task-points';
        taskPoints.textContent = `${task.points} pts`;

        const wikiLink = generateWikiLink(task);
        if(wikiLink) {
            const linkDiv = document.createElement('div');
            linkDiv.className = 'task-link';
            linkDiv.innerHTML = `<a href="${wikiLink}" target="_blank">Wiki</a>`;
            taskActions.appendChild(linkDiv);
        }

        taskActions.appendChild(taskPoints);

        taskHeader.appendChild(taskMainInfo);
        taskHeader.appendChild(taskActions);
        taskDiv.appendChild(taskHeader);
        pinnedResultsDiv.appendChild(taskDiv);
    });
}

// Random Task Feature
const randomTaskBtn = document.getElementById('random-task-btn');
const modal = document.getElementById('random-task-modal');
const closeBtn = document.querySelector('.close-btn');
const randomTaskContent = document.getElementById('random-task-content');
const fireworksContainer = document.getElementById('fireworks-container');

randomTaskBtn.addEventListener('click', () => {
    const completedTaskIds = playerData ? new Set(playerData.league_tasks) : new Set();
    const incompleteTasks = [];

    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            if (!completedTaskIds.has(task.id)) {
                incompleteTasks.push(task);
            }
        });
    }

    if (incompleteTasks.length === 0) {
        randomTaskContent.style.display = 'none';
        fireworksContainer.style.display = 'block';
        // Simple fireworks effect
        createFireworks();
    } else {
        fireworksContainer.style.display = 'none';
        randomTaskContent.style.display = 'block';
        const randomTask = incompleteTasks[Math.floor(Math.random() * incompleteTasks.length)];
        randomTaskContent.innerHTML = `
            <h3>${randomTask.task}</h3>
            <p>${randomTask.information}</p>
            <p><em>Requirements: ${randomTask.requirements || 'N/A'}</em></p>
            <p><strong>Points: ${randomTask.points}</strong></p>
        `;
    }

    modal.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

function createFireworks() {
    const container = document.getElementById('fireworks-container');
    for (let i = 0; i < 30; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        firework.style.left = Math.random() * 100 + 'vw';
        firework.style.top = Math.random() * 100 + 'vh';
        firework.style.animationDuration = (Math.random() * 2 + 1) + 's';
        container.appendChild(firework);
        setTimeout(() => firework.remove(), 3000);
    }
}

function generateWikiLink(task) {
    const baseUrl = 'https://runescape.wiki/w/';
    let searchTerm = '';

    // Check for quest requirements first
    const questMatch = task.task.match(/Complete the quest: (.*?)\./) || task.requirements.match(/Completion of (.*?)(?:\(quest\))?$/);
    if (questMatch && questMatch[1]) {
        searchTerm = questMatch[1].trim().replace(/\s+/g, '_');
        return `${baseUrl}${searchTerm}`;
    }

    // Check for skill requirements
    const skillMatch = task.requirements.match(/\d+\s+([a-zA-Z]+)/);
    if (skillMatch && skillMatch[1]) {
        searchTerm = skillMatch[1].trim();
        return `${baseUrl}${searchTerm}`;
    }

    // Fallback to task name if it seems like a quest
    if (task.task.toLowerCase().includes("quest")) {
        searchTerm = task.task.replace(/Complete the quest: /i, '').replace(/\./, '').trim().replace(/\s+/g, '_');
        return `${baseUrl}${searchTerm}`;
    }

    return null;
}