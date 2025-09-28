console.log("script.js loaded");

let allTasks = {};
let playerData = null;
let pinnedTasks = new Set(JSON.parse(localStorage.getItem('pinnedTasks') || '[]'));
let tempCompletedTasks = new Set();
const allSkills = new Set(["Agility", "Archaeology", "Attack", "Construction", "Cooking", "Crafting", "Defence", "Divination", "Dungeoneering", "Farming", "Firemaking", "Fishing", "Fletching", "Herblore", "Constitution", "Hunter", "Invention", "Magic", "Mining", "Necromancy", "Prayer", "Ranged", "Runecrafting", "Slayer", "Smithing", "Strength", "Summoning", "Thieving", "Woodcutting"]);

document.addEventListener('DOMContentLoaded', () => {
    fetch('tasks.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            allTasks = data;
            populateFilters();
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<p style="color: red;">Failed to load tasks. Please try refreshing the page.</p>';
        });
});

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

document.getElementById('lookup-btn').addEventListener('click', () => {
    const username = document.getElementById('username').value.trim();
    if (!username) {
        alert('Please enter a username.');
        return;
    }

    const apiUrl = `https://sync.runescape.wiki/runescape/player/${username}/LEAGUE_1`;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading player data...';
    tempCompletedTasks.clear();

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.error) throw new Error(data.error);
            playerData = data;
            document.getElementById('random-task-btn').disabled = false;
            displayResults();
            displayPinnedTasks();
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}. Please check the username and try again.</p>`;
        });
});

function populateFilters() {
    const tiers = new Set(Object.keys(allTasks));
    const locations = new Set();
    const skills = new Set();

    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            locations.add(task.locality.split(':')[0]);
            if (task.requirements) {
                const reqs = task.requirements.split(',');
                reqs.forEach(req => {
                    const match = req.trim().match(/^\d+\s+([a-zA-Z\s]+)/);
                    if (match && !/completion of/i.test(match[0]) && allSkills.has(match[1].trim())) {
                        skills.add(match[1].trim());
                    }
                });
            }
        });
    }

    const tierFilter = document.getElementById('tier-filter');
    Array.from(tiers).sort().forEach(tier => tierFilter.appendChild(new Option(tier, tier)));

    const locationFilter = document.getElementById('location-filter');
    Array.from(locations).sort().forEach(loc => locationFilter.appendChild(new Option(loc, loc)));

    const skillFilter = document.getElementById('skill-filter');
    Array.from(skills).sort().forEach(skill => skillFilter.appendChild(new Option(skill, skill)));
}

function processTasks(completedTaskIds) {
    const processed = {};
    for (const tier in allTasks) {
        processed[tier] = { completed: [], incomplete: [], points: 0, totalPoints: 0 };
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
    let totalCompletedPoints = 0, totalPossiblePoints = 0;
    const tierOrder = ['Easy', 'Medium', 'Hard', 'Elite', 'Master'];
    const hideCompleted = document.getElementById('hide-completed-toggle').checked;
    const searchTerm = document.getElementById('search-bar').value.toLowerCase();
    const selectedTier = document.getElementById('tier-filter').value;
    const selectedLocation = document.getElementById('location-filter').value;
    const selectedSkill = document.getElementById('skill-filter').value;

    tierOrder.forEach(tier => {
        if (results[tier] && (!selectedTier || tier === selectedTier)) {
            totalCompletedPoints += results[tier].points;
            totalPossiblePoints += results[tier].totalPoints;
            const allTierTasks = [...results[tier].completed, ...results[tier].incomplete].sort((a, b) => a.id - b.id);
            const filteredTasks = allTierTasks.filter(task => {
                const isCompleted = completedTaskIds.has(task.id) || tempCompletedTasks.has(task.id);
                if (hideCompleted && isCompleted) return false;
                if (searchTerm && !task.task.toLowerCase().includes(searchTerm)) return false;
                if (selectedLocation && task.locality.split(':')[0] !== selectedLocation) return false;
                if (selectedSkill && !(new RegExp(`\\b${selectedSkill}\\b`, 'i')).test(task.requirements)) return false;
                return true;
            });

            if (filteredTasks.length > 0) {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'task-category';
                const categoryTitle = document.createElement('h2');
                categoryTitle.textContent = `${tier} Tasks (${results[tier].points} / ${results[tier].totalPoints} Points)`;
                categoryDiv.appendChild(categoryTitle);
                filteredTasks.forEach(task => categoryDiv.appendChild(createTaskElement(task, completedTaskIds)));
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
    taskDiv.innerHTML = `
        <div class="task-header">
            <div class="task-main-info">
                <div class="task-name">${task.task}</div>
                <div class="task-description">${task.information}</div>
                <div class="task-requirements"><em>Requirements: ${task.requirements || 'N/A'}</em></div>
            </div>
            <div class="task-actions">
                <div class="task-points">${task.points} pts</div>
            </div>
        </div>
    `;
    if (!isCompleted) {
        const pinIcon = document.createElement('span');
        pinIcon.className = 'pin-icon';
        pinIcon.innerHTML = '&#128204;';
        if (pinnedTasks.has(task.id)) pinIcon.classList.add('pinned');
        pinIcon.onclick = e => { e.stopPropagation(); togglePinTask(task.id); };
        taskDiv.querySelector('.task-actions').appendChild(pinIcon);
    }
    const linksContainer = document.createElement('div');
    linksContainer.className = 'task-links-container';
    generateWikiLinks(task).forEach(link => {
        const linkEl = document.createElement('div');
        linkEl.className = 'task-link';
        linkEl.innerHTML = `<a href="${link.url}" target="_blank" onclick="event.stopPropagation()">${link.name}</a>`;
        linksContainer.appendChild(linkEl);
    });
    if (linksContainer.hasChildNodes()) taskDiv.appendChild(linksContainer);
    return taskDiv;
}

['hide-completed-toggle', 'search-bar', 'tier-filter', 'location-filter', 'skill-filter'].forEach(id => {
    document.getElementById(id).addEventListener(id === 'search-bar' ? 'input' : 'change', displayResults);
});

function togglePinTask(taskId) {
    pinnedTasks.has(taskId) ? pinnedTasks.delete(taskId) : pinnedTasks.add(taskId);
    localStorage.setItem('pinnedTasks', JSON.stringify(Array.from(pinnedTasks)));
    displayResults();
    displayPinnedTasks();
}

function displayPinnedTasks() {
    const pinnedResultsDiv = document.getElementById('pinned-results');
    pinnedResultsDiv.innerHTML = '';
    const completedTaskIds = playerData ? new Set(playerData.league_tasks) : new Set();
    const tasksToRemove = Array.from(pinnedTasks).filter(id => completedTaskIds.has(id) || tempCompletedTasks.has(id));
    if (tasksToRemove.length > 0) {
        tasksToRemove.forEach(id => pinnedTasks.delete(id));
        localStorage.setItem('pinnedTasks', JSON.stringify(Array.from(pinnedTasks)));
    }
    if (pinnedTasks.size === 0) {
        pinnedResultsDiv.innerHTML = '<p>No tasks have been pinned.</p>';
        return;
    }
    const tasksToDisplay = [];
    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            if (pinnedTasks.has(task.id)) tasksToDisplay.push(task);
        });
    }
    tasksToDisplay.sort((a, b) => a.id - b.id).forEach(task => {
        pinnedResultsDiv.appendChild(createTaskElement(task, completedTaskIds));
    });
}

document.getElementById('random-task-btn').addEventListener('click', () => {
    if (!playerData) {
        alert('Please check tasks for a user first.');
        return;
    }
    const completedTaskIds = new Set(playerData.league_tasks);
    const incompleteTasks = [];
    for (const tier in allTasks) {
        allTasks[tier].forEach(task => {
            if (!completedTaskIds.has(task.id) && !tempCompletedTasks.has(task.id)) {
                incompleteTasks.push(task);
            }
        });
    }
    const cardContainer = document.getElementById('random-task-card-container');
    const fireworksContainer = document.getElementById('fireworks-container');
    cardContainer.innerHTML = '';
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
            cardContainer.innerHTML = '';
        };
        actions.appendChild(pinBtn);
        actions.appendChild(completeBtn);
        taskCard.appendChild(actions);
        cardContainer.appendChild(taskCard);
    }
});

function createFireworks() {
    const container = document.getElementById('fireworks-container');
    if (!container) return;
    container.innerHTML = '<p>There\'s nothing left to do other than go outside and touch grass.</p>';
    for (let i = 0; i < 50; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        firework.style.left = Math.random() * 100 + 'vw';
        firework.style.top = Math.random() * 100 + 'vh';
        firework.style.animationDuration = (Math.random() * 1 + 0.5) + 's';
        firework.style.animationDelay = (Math.random() * 1) + 's';
        container.appendChild(firework);
        setTimeout(() => firework.remove(), 2000);
    }
}

function generateWikiLinks(task) {
    const baseUrl = 'https://runescape.wiki/w/';
    const links = [];
    const reqString = task.requirements || '';
    const taskString = task.task || '';

    const taskSetMatch = taskString.match(/Complete the task set: (Easy|Medium|Hard|Elite) (.*?)\./i);
    if (taskSetMatch) {
        const tier = taskSetMatch[1].trim();
        let area = taskSetMatch[2].trim();
        if (area.includes("Fremennik")) area = "Fremennik"; // Normalize area name
        const linkName = `${tier} ${area} achievements`;
        links.push({ name: linkName, url: `${baseUrl}${tier}_${area}_achievements` });
    }

    const questRegex = /(?:Completion of|Complete the quest:)\s+([a-zA-Z\s'-]+?)(?:\(miniquest\))?/gi;
    const combinedText = taskString + ' ' + reqString;
    let match;
    while ((match = questRegex.exec(combinedText)) !== null) {
        const questName = match[1].trim().replace(/[.,]$/, '');
        if (questName.length < 50 && !questName.toLowerCase().includes('achievements')) {
            links.push({ name: questName, url: `${baseUrl}${questName.replace(/\s+/g, '_')}` });
        }
    }

    const skillRegex = /(\d+)\s+([a-zA-Z]+)/g;
    while ((match = skillRegex.exec(reqString)) !== null) {
        const skillName = match[2].trim();
        if (allSkills.has(skillName)) {
            links.push({ name: `${match[1]} ${skillName}`, url: `${baseUrl}${skillName}` });
        }
    }

    return links.filter((link, index, self) => index === self.findIndex(l => l.url === link.url));
}