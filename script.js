console.log("script.js loaded");

const allTasks = {
  "Easy": [
    { "id": 462, "locality": "Anachronia", "task": "Complete the base camp tutorial on Anachronia.", "information": "Complete the Anachronia base camp tutorial.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 463, "locality": "Anachronia", "task": "Observe all the large dragonkin statues around Anachronia.", "information": "Observe all the large dragonkin statues around Anachronia.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 464, "locality": "Anachronia", "task": "Surge under the spine on Anachronia.", "information": "Complete Spinal Surgery. (5 Agility)", "requirements": "5 Agility", "tier": "Easy", "points": 10 },
    { "id": 461, "locality": "Anachronia", "task": "Set sail for Anachronia.", "information": "Set sail for Anachronia on The Stormbreaker docked at Varrock Dig Site.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 465, "locality": "Anachronia", "task": "Complete the quest: Helping Laniakea (miniquest).", "information": "Complete the Helping Laniakea miniquest.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 466, "locality": "Anachronia", "task": "Complete the quest: Raksha, the Shadow Colossus.", "information": "Complete Raksha, the Shadow Colossus quest.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 467, "locality": "Anachronia", "task": "Obtain 100 potent herbs from Herby Werby.", "information": "Obtain 100 potent herbs from Herby Werby. (1 Herblore)", "requirements": "1 Herblore", "tier": "Easy", "points": 10 },
    { "id": 217, "locality": "Asgarnia: Burthorpe", "task": "Complete a lap of the Burthorpe Agility course.", "information": "Complete a lap of the Burthorpe Agility Course. (1 Agility)", "requirements": "1 Agility", "tier": "Easy", "points": 10 },
    { "id": 221, "locality": "Asgarnia: Falador", "task": "Kill a goblin raider boss in the Goblin Village.", "information": "Kill 15 goblins in the Goblin Village to spawn a goblin raider boss.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 222, "locality": "Asgarnia: Falador", "task": "Complete the quest: Witch's House.", "information": "Complete Witch's House.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 223, "locality": "Asgarnia: Falador", "task": "Sit down with Tiffy in Falador park.", "information": "Sit on the bench with Sir Tiffy Cashien in Falador Park.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 224, "locality": "Asgarnia: Falador", "task": "Pray to Bandos's remains.", "information": "Pray to Bandos's remains (just south-east of Goblin Village).", "requirements": "just south-east of Goblin Village", "tier": "Easy", "points": 10 },
    { "id": 225, "locality": "Asgarnia: Falador", "task": "Dance in the Falador party room.", "information": "Dance in the Falador party room.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 263, "locality": "Asgarnia: Port Sarim", "task": "Give Thurgo a redberry pie.", "information": "Give Thurgo a redberry pie. (10 Cooking, Partial completion of The Knight's Sword)", "requirements": "10 Cooking, Partial completion of The Knight's Sword", "tier": "Easy", "points": 10 },
    { "id": 268, "locality": "Asgarnia: Taverley", "task": "Build a God statue in Taverley.", "information": "Build a God statue in Taverley.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 271, "locality": "Desert: Menaphos", "task": "Enter Menaphos.", "information": "Enter Menaphos.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 272, "locality": "Desert: General", "task": "Catch a whirligig at Het's Oasis.", "information": "Catch a whirligig at Het's Oasis. (1 Hunter)", "requirements": "1 Hunter", "tier": "Easy", "points": 10 },
    { "id": 274, "locality": "Desert: General", "task": "Search the Grand Gold Chest in room 1 of Pyramid Plunder.", "information": "Search the grand gold chest in room 1 of Pyramid Plunder in Sophanem. (21 Thieving, Partial completion of Icthlarin's Little Helper)", "requirements": "21 Thieving, Partial completion of Icthlarin's Little Helper", "tier": "Easy", "points": 10 },
    { "id": 275, "locality": "Desert: General", "task": "Search the Grand Gold Chest in room 2 of Pyramid Plunder.", "information": "Search the grand gold chest in room 2 of Pyramid Plunder in Sophanem. (31 Thieving, Partial completion of Icthlarin's Little Helper)", "requirements": "31 Thieving, Partial completion of Icthlarin's Little Helper", "tier": "Easy", "points": 10 },
    { "id": 276, "locality": "Desert: General", "task": "Search the Grand Gold Chest in room 3 of Pyramid Plunder.", "information": "Search the grand gold chest in room 3 of Pyramid Plunder in Sophanem. (41 Thieving, Partial completion of Icthlarin's Little Helper)", "requirements": "41 Thieving, Partial completion of Icthlarin's Little Helper", "tier": "Easy", "points": 10 },
    { "id": 277, "locality": "Desert: General", "task": "Mine a gem rock at the Al Kharid mine.", "information": "Mine a gem rock at the Al Kharid mine. A common gem rock can be mined with level 1 Mining.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 279, "locality": "Desert: General", "task": "Kill a crocodile.", "information": "Kill a crocodile.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 280, "locality": "Desert: General", "task": "Create a spirit kalphite pouch.", "information": "Create a spirit kalphite pouch at the obelisk south west of Pollnivneach. (25 Summoning, A pouch, 51 spirit shards, a blue charm, and a potato cactus)", "requirements": "25 Summoning, A pouch, 51 spirit shards, a blue charm, and a potato cactus", "tier": "Easy", "points": 10 },
    { "id": 281, "locality": "Desert: Menaphos", "task": "Squish 10 corrupted scarabs.", "information": "Squish 10 corrupted scarabs.", "requirements": "N/A", "tier": "Easy", "points": 10 },
    { "id": 282, "locality": "Desert: General", "task": "Sell a pyramid top to Simon.", "information": "Hand Simon Templeton a pyramid top. (30 Agility)", "requirements": "30 Agility", "tier": "Easy", "points": 10 },
    { "id": 283, "locality": "Desert: General", "task": "Use any of the magic carpets in the desert.", "information": "Use any of the magic carpets in the desert. (1,000 coins)", "requirements": "1,000 coins", "tier": "Easy", "points": 10 },
    { "id": 284, "locality": "Desert: General", "task": "Harvest a rose at Het's Oasis.", "information": "Harvest a rose at Het's Oasis. (30 Farming)", "requirements": "30 Farming", "tier": "Easy", "points": 10 },
    { "id": 339, "locality": "Fremennik: Lunar Isles", "task": "Switch to the Lunar Spellbook at the astral altar.", "information": "Switch to the Lunar Spellbook at the astral altar. (Completion of Lunar Diplomacy)", "requirements": "Completion of Lunar Diplomacy", "tier": "Easy", "points": 10 },
    { "id": 340, "locality": "Fremennik: Mainland", "task": "Defeat a Rock Crab in the Fremennik Province.", "information": "Defeat a Rock Crab in the Fremennik Province.", "requirements": "N/A", "tier": "Easy", "points": 10 }
  ]
};

let playerData = null;
let pinnedTasks = new Set(JSON.parse(localStorage.getItem('pinnedTasks') || '[]'));
let tempCompletedTasks = new Set();
const allSkills = new Set(["Agility", "Archaeology", "Attack", "Construction", "Cooking", "Crafting", "Defence", "Divination", "Dungeoneering", "Farming", "Firemaking", "Fishing", "Fletching", "Herblore", "Constitution", "Hunter", "Invention", "Magic", "Mining", "Necromancy", "Prayer", "Ranged", "Runecrafting", "Slayer", "Smithing", "Strength", "Summoning", "Thieving", "Woodcutting"]);

document.addEventListener('DOMContentLoaded', () => {
    populateFilters();
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