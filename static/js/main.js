document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const gameContainer = document.getElementById('game-container');
    let gameState = {}; // This will hold the last known state of the game

    socket.on('game_update', (state) => {
        gameState = state;
        if (!gameContainer.querySelector('.reveal-container') || state.stage === 'voting') {
            updateView(state);
        }
    });

    function updateView(state) {
        // ... (this function remains unchanged)
        gameContainer.innerHTML = '';
        if (state.stage === 'waiting') {
            const waitingText = document.createElement('h2');
            waitingText.className = 'waiting-text';
            waitingText.textContent = 'Waiting for the next round...';
            gameContainer.appendChild(waitingText);
        } else if (state.stage === 'answering' || state.stage === 'voting') {
            if (state.image) {
                const imageEl = document.createElement('img');
                imageEl.src = state.image;
                imageEl.className = 'prompt-image';
                gameContainer.appendChild(imageEl);
            }
            const promptText = document.createElement('h2');
            promptText.className = 'prompt';
            promptText.textContent = state.prompt;
            gameContainer.appendChild(promptText);
            if (state.stage === 'voting') {
                const votingGrid = document.createElement('div');
                votingGrid.className = 'voting-grid';
                state.answers.forEach((answer, index) => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `<span class="card-number">${index + 1}.</span> ${answer}`;
                    votingGrid.appendChild(card);
                });
                gameContainer.appendChild(votingGrid);
            }
        }
    }

    // --- UPDATED: REVEAL ANIMATION LISTENER ---
    socket.on('show_reveal_animation', (data) => {
        gameContainer.innerHTML = '';

        const revealContainer = document.createElement('div');
        revealContainer.className = 'reveal-container';

        revealContainer.innerHTML = `
            <h3 class="reveal-main-prompt">${data.prompt}</h3>
            <p class="reveal-question">The answer was...</p>
            <h2 class="reveal-prompt">${data.clicked_answer}</h2>
            <div class="reveal-result-text"></div>
        `;
        gameContainer.appendChild(revealContainer);

        const promptElement = revealContainer.querySelector('.reveal-prompt');
        const resultElement = revealContainer.querySelector('.reveal-result-text');

        promptElement.classList.add('is-flickering');

        setTimeout(() => {
            promptElement.classList.remove('is-flickering');

            if (data.is_real) {
                promptElement.classList.add('reveal-final-real');
                resultElement.textContent = 'REAL!';
                resultElement.classList.add('reveal-final-real');
            } else {
                promptElement.classList.add('reveal-final-fake');
                resultElement.textContent = 'FAKE!';
                resultElement.classList.add('reveal-final-fake');
            }

            // The automatic timer that caused bugs has been REMOVED.
            // The screen will now wait here until the admin presses the button.

        }, 3500);
    });
});