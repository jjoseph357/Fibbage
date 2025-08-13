document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const adminControls = document.getElementById('admin-controls');
    let gameState = {};
    let currentPromptData = {};

    socket.on('game_update', (state) => {
        gameState = state;
        updateAdminView();
    });

    socket.on('random_prompt_data', (data) => {
        // ... (this function remains unchanged)
        currentPromptData = data;
        const promptInput = document.getElementById('prompt-input');
        const answerInput = document.getElementById('answer-input');
        const imagePreview = document.getElementById('image-preview');
        if (promptInput && answerInput) {
            promptInput.value = data.prompt;
            answerInput.value = data.answer || '';
        }
        if(imagePreview) {
            if (data.image) {
                imagePreview.src = data.image;
                imagePreview.style.display = 'block';
            } else {
                imagePreview.style.display = 'none';
            }
        }
    });

    function updateAdminView() {
        adminControls.innerHTML = '';

        if (gameState.stage === 'waiting') {
            renderStartPhase();
        } else if (gameState.stage === 'answering') {
            renderAnsweringPhase();
        } else if (gameState.stage === 'voting') {
            renderVotingPhase();
        } else if (gameState.stage === 'revealing') { // Check for the new stage
            renderRevealingPhase();
        }
    }

    // --- NEW: RENDER FUNCTION FOR THE ADMIN'S REVEAL SCREEN ---
    function renderRevealingPhase() {
        const section = document.createElement('div');
        section.className = 'admin-section';
        const revealed = gameState.last_revealed;
        const resultText = revealed.is_real ? 'REAL' : 'FAKE';
        const resultClass = revealed.is_real ? 'reveal-final-real' : 'reveal-final-fake';

        section.innerHTML = `
            <h2>Answer Revealed</h2>
            <p>The answer chosen was:</p>
            <h3 class="prompt">${revealed.answer}</h3>
            <p>This answer was <strong class="${resultClass}">${resultText}</strong>.</p>
            <button id="back-to-voting-btn">Back to Answers</button>
        `;
        adminControls.appendChild(section);

        document.getElementById('back-to-voting-btn').addEventListener('click', () => {
            socket.emit('back_to_voting');
        });
    }

    function renderStartPhase() {
        // ... (this function remains unchanged)
        const section = document.createElement('div');
        section.className = 'admin-section';
        const isQuiplash = gameState.game_mode === 'quiplash';
        section.innerHTML = `
            <h2>New Round</h2>
            <div>
                <label for="game-mode">Game Mode:</label>
                <select id="game-mode-select">
                    <option value="fibbage" ${!isQuiplash ? 'selected' : ''}>Fibbage</option>
                    <option value="quiplash" ${isQuiplash ? 'selected' : ''}>Quiplash</option>
                </select>
            </div>
            <div>
                <label for="prompt">Prompt:</label><br>
                <textarea id="prompt-input" rows="3"></textarea>
            </div>
            <img id="image-preview" style="max-width: 400px; max-height: 400px; display: none; margin-top: 10px;">
            <div id="answer-input-container" style="display: ${isQuiplash ? 'none' : 'block'};">
                <label for="answer">Answer:</label><br>
                <input type="text" id="answer-input">
            </div>
            <button id="shuffle-btn">Shuffle Random Prompt</button>
            <button id="start-btn">Start Game</button>
        `;
        adminControls.appendChild(section);
        const gameModeSelect = document.getElementById('game-mode-select');
        gameModeSelect.addEventListener('change', (e) => {
            const answerInputContainer = document.getElementById('answer-input-container');
            if (e.target.value === 'quiplash') {
                answerInputContainer.style.display = 'none';
            } else {
                answerInputContainer.style.display = 'block';
            }
        });
        document.getElementById('shuffle-btn').addEventListener('click', () => {
             const game_mode = document.getElementById('game-mode-select').value;
             socket.emit('get_random_prompt', { game_mode });
        });
        document.getElementById('start-btn').addEventListener('click', () => {
            const prompt = document.getElementById('prompt-input').value;
            const answer = document.getElementById('answer-input').value;
            const game_mode = document.getElementById('game-mode-select').value;
            if (prompt && (answer || game_mode === 'quiplash')) {
                socket.emit('start_game', { prompt, answer, game_mode, image: currentPromptData.image });
            } else {
                alert('Please provide a prompt and an answer, or use the shuffle button.');
            }
        });
    }

    function renderAnsweringPhase() {
        // ... (this function remains unchanged)
        const section = document.createElement('div');
        section.className = 'admin-section';
        const isQuiplash = gameState.game_mode === 'quiplash';
        section.innerHTML = `
            <h2>Collecting Answers</h2>
            ${gameState.image ? `<img src="${gameState.image}" style="max-width: 400px; max-height: 400px; margin-bottom: 10px;">` : ''}
            <p class="prompt">${gameState.prompt}</p>
            ${!isQuiplash ? `<p><strong>Answer:</strong> ${gameState.answer}</p>` : ''}
            <h3>Player Answers:</h3>
            <div id="player-answers-container">
                <div class="player-answers-input"><input type="text" class="player-answer-input"></div>
            </div>
            <button id="add-answer-btn">+</button>
            <button id="start-voting-btn">Go to Voting</button>
        `;
        adminControls.appendChild(section);
        document.getElementById('add-answer-btn').addEventListener('click', addPlayerAnswerInput);
        document.getElementById('start-voting-btn').addEventListener('click', submitPlayerAnswers);
    }

    function renderVotingPhase() {
        // ... (this function remains unchanged)
        const section = document.createElement('div');
        section.className = 'admin-section';
        const isFibbage = gameState.game_mode === 'fibbage';
        let answersHtml = `<h2>Click an answer to reveal it</h2><div class="answer-list">`;
        gameState.answers.forEach((answer, index) => {
            const isReal = isFibbage && answer === gameState.answer;
            const clickableClass = isFibbage ? 'reveal-trigger' : '';
            const dataAttribute = isFibbage ? `data-answer="${answer.replace(/"/g, '&quot;')}"` : '';
            answersHtml += `
                <div class="card ${isReal ? 'real-answer' : ''} ${clickableClass}" ${dataAttribute}>
                    <span>${index + 1}. ${answer}</span>
                    ${isReal ? '<strong>(REAL ANSWER)</strong>' : ''}
                </div>`;
        });
        answersHtml += `</div><button id="new-round-btn">Start New Round</button>`;
        section.innerHTML = answersHtml;
        adminControls.appendChild(section);
        if (isFibbage) {
            document.querySelectorAll('.reveal-trigger').forEach(card => {
                card.addEventListener('click', (e) => {
                    const answerText = e.currentTarget.dataset.answer;
                    socket.emit('reveal_answer', { answer_text: answerText });
                });
            });
        }
        document.getElementById('new-round-btn').addEventListener('click', () => {
            socket.emit('new_round');
        });
    }

    function addPlayerAnswerInput() {
        // ... (this function remains unchanged)
        const container = document.getElementById('player-answers-container');
        const newInput = document.createElement('div');
        newInput.className = 'player-answers-input';
        newInput.innerHTML = `<input type="text" class="player-answer-input">`;
        container.appendChild(newInput);
    }

    function submitPlayerAnswers() {
        // ... (this function remains unchanged)
        const inputs = document.querySelectorAll('.player-answer-input');
        const playerAnswers = Array.from(inputs).map(input => input.value.trim()).filter(value => value !== '');
        socket.emit('submit_answers', { player_answers: playerAnswers });
    }
});