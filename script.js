console.log("script.js loaded");
let allTasks = {};
let playerData = null;
let pinnedTasks = new Set(JSON.parse(localStorage.getItem('pinnedTasks') || '[]'));
let tempCompletedTasks = new Set();


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

// Fetch all tasks from the JSON file when the script loads
fetch('tasks.json')
    .then(response => response.json())
    .then(data => {
        allTasks = data;
        populateFilters();
        document.getElementById('random-task-btn').disabled = false;
    })
    .catch(error => console.error('Error loading tasks:', error));

document.getElementById('lookup-btn').addEventListener('click', () => {
    console.log("Get Tasks button clicked");
    const username = document.getElementById('username').value.trim();
    if (!username) {
        alert('Please enter a username.');
        return;
    }

    if (Object.keys(allTasks).length === 0) {
        alert('Task list is not loaded yet. Please try again in a moment.');
        return;
    }

    const apiUrl = `https://sync.runescape.wiki/runescape/player/${username}/LEAGUE_1`;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading player data...';
    tempCompletedTasks.clear(); // Clear temp completed on new lookup

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
            displayPinnedTasks();
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
                    const match = req.trim().match(/^\d+\s+([a-zA-Z\s]+)/);
                    if (match && !/completion of/i.test(match[0])) {
                        let skillName = match[1].trim();
                        skills.add(skillName);
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
            if (completedTaskIds.has(task.id) || tempCompletedTasks.has(task.id)) {
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
    resultsDiv.innerHTML = '';

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


            const allTierTasks = [...category.completed, ...category.incomplete].sort((a, b) => a.id - b.id);

            const filteredTasks = allTierTasks.filter(task => {
                const isCompleted = completedTaskIds.has(task.id) || tempCompletedTasks.has(task.id);
                if (hideCompleted && isCompleted) return false;

                if (searchTerm && !task.task.toLowerCase().includes(searchTerm)) {
                    return false;
                }
                if (selectedLocation && task.locality.split(':')[0] !== selectedLocation) {
                    return false;
                }
                 if (selectedSkill) {
                    const skillRegex = new RegExp(`\\b${selectedSkill}\\b`, 'i');
                    if (!skillRegex.test(task.requirements)) return false;
                }
                return true;
            });

            if (filteredTasks.length > 0) {
                categoryDiv.appendChild(categoryTitle);
                filteredTasks.forEach(task => {
                    const taskDiv = createTaskElement(task, completedTaskIds);
                    categoryDiv.appendChild(taskDiv);
                });
                resultsDiv.appendChild(categoryDiv);
            }
        }
    });

    const summaryDiv = document.createElement('div');
    summaryDiv.innerHTML = `<h3>Total Points: ${totalCompletedPoints} / ${totalPossiblePoints}</h3><hr>`;
    resultsDiv.prepend(summaryDiv);
}

function createTaskElement(task, completedTaskIds) {
    const isCompleted = completedTaskIds.has(task.id) || tempCompletedTasks.has(task.id);
    const taskDiv = document.createElement('div');
    taskDiv.className = isCompleted ? 'task completed' : 'task';
    taskDiv.setAttribute('data-task-id', task.id);

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
    taskActions.appendChild(taskPoints);

    if (!isCompleted) {
        const pinIcon = document.createElement('span');
        pinIcon.className = 'pin-icon';
        pinIcon.innerHTML = '&#128204;';
        if (pinnedTasks.has(task.id)) {
            pinIcon.classList.add('pinned');
        }
        pinIcon.onclick = (e) => {
            e.stopPropagation();
            togglePinTask(task.id);
        };
        taskActions.appendChild(pinIcon);
    }

    const wikiLink = generateWikiLink(task);
    if(wikiLink) {
        const linkDiv = document.createElement('div');
        linkDiv.className = 'task-link';
        linkDiv.innerHTML = `<a href="${wikiLink}" target="_blank" onclick="event.stopPropagation()">Wiki</a>`;
        taskActions.appendChild(linkDiv);
    }

    taskHeader.appendChild(taskMainInfo);
    taskHeader.appendChild(taskActions);
    taskDiv.appendChild(taskHeader);
    return taskDiv;
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

    const tasksToRemove = [];
    pinnedTasks.forEach(taskId => {
        if (completedTaskIds.has(taskId) || tempCompletedTasks.has(taskId)) {
            tasksToRemove.push(taskId);
        }
    });

    tasksToRemove.forEach(taskId => pinnedTasks.delete(taskId));
    if (tasksToRemove.length > 0) {
        localStorage.setItem('pinnedTasks', JSON.stringify(Array.from(pinnedTasks)));
    }


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

    tasksToDisplay.sort((a,b) => a.id - b.id).forEach(task => {
        const taskDiv = createTaskElement(task, completedTaskIds);
        pinnedResultsDiv.appendChild(taskDiv);
    });
}

// Random Task Feature
const randomTaskBtn = document.getElementById('random-task-btn');
const randomTaskCardContainer = document.getElementById('random-task-card-container');
const fireworksContainer = document.getElementById('fireworks-container');

randomTaskBtn.addEventListener('click', () => {
    if (!playerData) {
        alert('Please check tasks for a user first.');
        return;
    }
    const completedTaskIds = playerData ? new Set(playerData.league_tasks) : new Set();
    const incompleteTasks = [];

    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            if (!completedTaskIds.has(task.id) && !tempCompletedTasks.has(task.id)) {
                incompleteTasks.push(task);
            }
        });
    }

    randomTaskCardContainer.innerHTML = '';
    fireworksContainer.style.display = 'none';

    if (incompleteTasks.length === 0) {
        fireworksContainer.style.display = 'block';
        createFireworks();
    } else {
        const randomTask = incompleteTasks[Math.floor(Math.random() * incompleteTasks.length)];
        const taskCard = createTaskElement(randomTask, completedTaskIds);

        const actions = document.createElement('div');
        actions.className = 'random-task-actions';

        const pinBtn = document.createElement('button');
        pinBtn.textContent = 'Pin it';
        pinBtn.onclick = () => togglePinTask(randomTask.id);

        const completeBtn = document.createElement('button');
        completeBtn.textContent = 'Complete it';
        completeBtn.onclick = () => {
            tempCompletedTasks.add(randomTask.id);
            displayResults();
            displayPinnedTasks();
            randomTaskCardContainer.innerHTML = ''; // Clear the card
        };

        actions.appendChild(pinBtn);
        actions.appendChild(completeBtn);
        taskCard.appendChild(actions);

        randomTaskCardContainer.appendChild(taskCard);
    }
});


function createFireworks() {
    const container = document.getElementById('fireworks-container');
    if(!container) return;
    container.innerHTML = '<p>There\'s nothing left to do other than go outside and touch grass.</p>'; // Reset
    for (let i = 0; i < 50; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';

        const x = Math.random() * 100;
        const y = Math.random() * 100;
        firework.style.left = x + 'vw';
        firework.style.top = y + 'vh';

        const size = Math.random() * 5 + 2;
        firework.style.width = size + 'px';
        firework.style.height = size + 'px';

        firework.style.animationDuration = (Math.random() * 1 + 0.5) + 's';
        firework.style.animationDelay = (Math.random() * 1) + 's';

        container.appendChild(firework);
        setTimeout(() => firework.remove(), 2000);
    }
}

function generateWikiLink(task) {
    const baseUrl = 'https://runescape.wiki/w/';
    let searchTerm = '';

    const questMatch = task.task.match(/Complete the quest: (.*?)(?:\(miniquest\))?\./) || task.requirements.match(/Completion of (.*?)(?:\(quest\))?$/i);
    if (questMatch && questMatch[1]) {
        searchTerm = questMatch[1].trim().replace(/ \(miniquest\)/i, '').replace(/\s+/g, '_');
        return `${baseUrl}${searchTerm}`;
    }

    const skillMatch = task.requirements.match(/(\d+)\s+([a-zA-Z]+)/);
    if (skillMatch && skillMatch[2]) {
        searchTerm = skillMatch[2].trim();
        return `${baseUrl}${searchTerm}`;
    }

    if (task.task.toLowerCase().includes("quest")) {
        searchTerm = task.task.replace(/Complete the quest: /i, '').replace(/\./, '').trim().replace(/\s+/g, '_');
        return `${baseUrl}${searchTerm}`;
    }

    return null;
}