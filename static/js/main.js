document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const gameContainer = document.getElementById('game-container');

    socket.on('game_update', (state) => {
        updateView(state);
    });

    function updateView(state) {
        gameContainer.innerHTML = ''; // Clear previous content

        if (state.stage === 'waiting') {
            const waitingText = document.createElement('h2');
            waitingText.className = 'waiting-text';
            waitingText.textContent = 'Waiting for the next round...';
            gameContainer.appendChild(waitingText);
        } else if (state.stage === 'answering') {
            const promptText = document.createElement('h2');
            promptText.className = 'prompt';
            promptText.textContent = state.prompt;
            gameContainer.appendChild(promptText);
        } else if (state.stage === 'voting') {
            const promptText = document.createElement('h2');
            promptText.className = 'prompt';
            promptText.textContent = state.prompt;
            gameContainer.appendChild(promptText);

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
});