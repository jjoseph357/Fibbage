document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const gameContainer = document.getElementById('game-container');
    let gameState = {};

    socket.on('game_update', (state) => {
        gameState = state;
        if (!gameContainer.querySelector('.reveal-container') || state.stage === 'voting') {
            updateView(state);
        }
    });

    function updateView(state) {
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

            // --- CORE LOGIC CHANGE FOR VIEWERS ---
            if (state.stage === 'voting') {
                const votingGrid = document.createElement('div');
                votingGrid.className = 'voting-grid';

                // ONLY render the REVEALED answers
                if (state.revealed_answers && state.revealed_answers.length > 0) {
                    state.revealed_answers.forEach((answer) => {
                        const card = document.createElement('div');
                        // Use a fade-in animation for newly revealed cards
                        card.className = 'card revealed-card';
                        card.innerHTML = `<span>${answer}</span>`;
                        votingGrid.appendChild(card);
                    });
                } else {
                    // If no answers are revealed yet, show a waiting message
                    const waitingRevealText = document.createElement('h2');
                    waitingRevealText.className = 'waiting-text';
                    waitingRevealText.textContent = 'Waiting for the answers...';
                    gameContainer.appendChild(waitingRevealText);
                }
                gameContainer.appendChild(votingGrid);
            }
        }
    }

    // --- (The reveal animation handler remains the same) ---
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
        }, 3500);
    });
});