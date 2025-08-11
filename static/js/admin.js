document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const adminControls = document.getElementById('admin-controls');
    let gameState = {};

    socket.on('game_update', (state) => {
        gameState = state;
        updateAdminView();
    });

    socket.on('random_prompt_data', (data) => {
        const promptInput = document.getElementById('prompt-input');
        const answerInput = document.getElementById('answer-input');
        if (promptInput && answerInput) {
            promptInput.value = data.prompt;
            answerInput.value = data.answer;
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
        }
    }

    function renderStartPhase() {
        const section = document.createElement('div');
        section.className = 'admin-section';

        // The backticks (`) here are essential for multi-line HTML
        section.innerHTML = `
            <h2>New Round</h2>
            <div>
                <label for="prompt">Prompt:</label><br>
                <textarea id="prompt-input" rows="3"></textarea>
            </div>
            <div>
                <label for="answer">Answer:</label><br>
                <input type="text" id="answer-input">
            </div>
            <button id="shuffle-btn">Shuffle Random Prompt</button>
            <button id="start-btn">Start Game</button>
        `;
        adminControls.appendChild(section);

        document.getElementById('shuffle-btn').addEventListener('click', () => {
             socket.emit('get_random_prompt');
        });

        document.getElementById('start-btn').addEventListener('click', () => {
            const prompt = document.getElementById('prompt-input').value;
            const answer = document.getElementById('answer-input').value;
            if (prompt && answer) {
                socket.emit('start_game', { prompt, answer });
            } else {
                alert('Please provide a prompt and an answer, or use the shuffle button.');
            }
        });
    }

    function renderAnsweringPhase() {
        const section = document.createElement('div');
        section.className = 'admin-section';
        section.innerHTML = `
            <h2>Collecting Answers</h2>
            <p class="prompt"><strong>Prompt:</strong> ${gameState.prompt}</p>
            <p><strong>Answer:</strong> ${gameState.answer}</p>
            <h3>Player Answers:</h3>
            <div id="player-answers-container">
                <div class="player-answers-input">
                    <input type="text" class="player-answer-input">
                </div>
            </div>
            <button id="add-answer-btn">+</button>
            <button id="start-voting-btn">Go to Voting</button>
        `;
        adminControls.appendChild(section);

        document.getElementById('add-answer-btn').addEventListener('click', addPlayerAnswerInput);
        document.getElementById('start-voting-btn').addEventListener('click', submitPlayerAnswers);
    }

    function renderVotingPhase() {
        const section = document.createElement('div');
        section.className = 'admin-section';
        let answersHtml = `<h2>Voting Stage</h2><div class="answer-list">`;
        gameState.answers.forEach((answer, index) => {
            const isReal = answer === gameState.answer;
            answersHtml += `
                <div class="card ${isReal ? 'real-answer' : ''}">
                    <span>${index + 1}. ${answer}</span>
                    ${isReal ? '<strong>(REAL ANSWER)</strong>' : ''}
                </div>`;
        });
        answersHtml += `</div><button id="new-round-btn">Start New Round</button>`;
        section.innerHTML = answersHtml;
        adminControls.appendChild(section);

        document.getElementById('new-round-btn').addEventListener('click', () => {
            socket.emit('new_round');
        });
    }

    function addPlayerAnswerInput() {
        const container = document.getElementById('player-answers-container');
        const newInput = document.createElement('div');
        newInput.className = 'player-answers-input';
        newInput.innerHTML = `<input type="text" class="player-answer-input">`;
        container.appendChild(newInput);
    }

    function submitPlayerAnswers() {
        const inputs = document.querySelectorAll('.player-answer-input');
        const playerAnswers = Array.from(inputs)
            .map(input => input.value.trim())
            .filter(value => value !== '');
        socket.emit('submit_answers', { player_answers: playerAnswers });
    }
});