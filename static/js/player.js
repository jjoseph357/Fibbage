document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const playerTabsContainer = document.getElementById('player-tabs-container');
    const playerStage = document.getElementById('player-stage');

    // Local players list: [{ id, name, avatar }]
    let localPlayers = JSON.parse(localStorage.getItem('party_local_players') || '[]');
    let activePlayerId = localStorage.getItem('party_active_player_id') || '';
    let playerStates = {}; // pid -> state object

    const AVATARS = [
        "🦊", "🐼", "🐸", "🦁", "🦄", "🐙", "🐨", "🐯",
        "🐵", "🐧", "🦉", "🐲", "🤖", "👻", "🚀", "🦖",
        "🦩", "🦔", "🐬", "🦥", "🐱", "🐶", "🐮", "🐷",
        "🐻", "🐰", "🦆", "🦚", "🦋", "🍄", "🌮", "🍕"
    ];

    let isJoinFormOpen = false;
    let lastRenderedKey = '';
    let lastRenderedPlayerId = '';

    // Initialize local players
    if (localPlayers.length > 0) {
        if (!activePlayerId || !localPlayers.find(p => p.id === activePlayerId)) {
            activePlayerId = localPlayers[0].id;
        }
    }

    // Save to storage
    function saveLocalPlayers() {
        localStorage.setItem('party_local_players', JSON.stringify(localPlayers));
        localStorage.setItem('party_active_player_id', activePlayerId);
    }

    // Socket listeners
    socket.on('connect', () => {
        // Register all local players with server
        localPlayers.forEach(p => {
            socket.emit('join_player', {
                player_id: p.id,
                name: p.name,
                avatar: p.avatar,
                is_local: true
            });
        });

        if (localPlayers.length === 0) {
            renderJoinForm();
        }
    });

    socket.on('player_update', (state) => {
        if (state && state.player_id) {
            playerStates[state.player_id] = state;
            renderPlayerTabs();
            if (state.player_id === activePlayerId) {
                renderActivePlayerView(state);
            }
        }
    });

    socket.on('sync_request', () => {
        // Request updated state for all local players
        localPlayers.forEach(p => {
            socket.emit('get_player_state', { player_id: p.id });
        });
    });

    function getPlayerViewStateKey(fullState) {
        if (!fullState) return '';
        const mState = fullState.manager_state || 'hub';
        if (mState !== 'in_game') {
            return `${mState}_${fullState.player_id}_${fullState.player_name}_${fullState.player_avatar}_${fullState.room_code || ''}`;
        }
        const gs = fullState.game_state;
        if (!gs) return `${mState}_none`;

        const gameId = gs.game_id || '';
        const stage = gs.stage || '';
        const round = gs.round || 0;
        const hasSubmitted = !!gs.has_submitted;

        if (stage === 'scoreboard' || stage === 'game_over') {
            return `${gameId}_${stage}_${round}_${fullState.player_score || 0}`;
        }

        if (gameId === 'quiplash') {
            if (stage === 'answering') {
                const myPrompts = gs.my_prompts || [];
                const activePrompt = myPrompts.find(p => !p.submitted_answer) || myPrompts[0];
                const activeMid = activePrompt ? activePrompt.matchup_id : 'all_done';
                const allSubmitted = myPrompts.length > 0 && myPrompts.every(p => p.submitted_answer);
                return `${gameId}_${stage}_${round}_${activeMid}_${allSubmitted}`;
            }
            if (stage === 'battle') {
                const promptText = gs.battle_matchup ? gs.battle_matchup.prompt : '';
                const myVote = gs.my_vote || '';
                const canVote = !!gs.can_vote;
                const isMyMatchup = !!gs.is_my_matchup;
                return `${gameId}_${stage}_${round}_${promptText}_${myVote}_${canVote}_${isMyMatchup}`;
            }
        }

        if (gameId === 'doodler') {
            if (stage === 'drawing') {
                return `${gameId}_${stage}_${round}_${gs.is_artist}_${hasSubmitted}`;
            }
            if (stage === 'bluffing') {
                return `${gameId}_${stage}_${round}_${gs.is_artist}_${hasSubmitted}_${gs.my_bluff || ''}`;
            }
            if (stage === 'voting') {
                return `${gameId}_${stage}_${round}_${gs.is_artist}_${hasSubmitted}_${gs.my_vote || ''}`;
            }
        }

        if (gameId === 'fibbage') {
            return `${gameId}_${stage}_${round}_${hasSubmitted}_${gs.my_lie || ''}_${gs.my_vote || ''}`;
        }

        if (gameId === 'trivia' || gameId === 'bible_trivia') {
            const myChoiceStr = Array.isArray(gs.my_choice) ? gs.my_choice.join(',') : (gs.my_choice || '');
            return `${gameId}_${stage}_${round}_${hasSubmitted}_${myChoiceStr}_${gs.is_correct}_${gs.q_type || ''}`;
        }

        return `${gameId}_${stage}_${round}_${hasSubmitted}`;
    }

    // =========================================================================
    // Virtual Multi-Player Switcher Tabs
    // =========================================================================
    function renderPlayerTabs() {
        if (localPlayers.length === 0) {
            playerTabsContainer.innerHTML = '';
            return;
        }

        let tabsHtml = '';
        localPlayers.forEach(p => {
            const isActive = p.id === activePlayerId;
            const pState = playerStates[p.id]?.game_state;
            
            let statusClass = '';
            if (pState) {
                if (pState.has_submitted) {
                    statusClass = 'is-ready';
                } else if (pState.stage === 'answering' || pState.stage === 'voting' || pState.stage === 'drawing' || pState.stage === 'bluffing') {
                    statusClass = 'needs-action';
                }
            }

            tabsHtml += `
                <button class="player-tab-btn ${isActive ? 'active' : ''} ${statusClass}" data-player-id="${p.id}">
                    <span>${p.avatar || '👤'}</span>
                    <span>${escapeHtml(p.name)}</span>
                    <span class="tab-status-dot"></span>
                </button>
            `;
        });

        tabsHtml += `
            <button class="add-player-tab-btn" id="add-player-btn">
                + Add Player
            </button>
        `;

        playerTabsContainer.innerHTML = tabsHtml;

        // Switch active player tab
        playerTabsContainer.querySelectorAll('.player-tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const pid = e.currentTarget.dataset.playerId;
                if (pid !== activePlayerId) {
                    activePlayerId = pid;
                    saveLocalPlayers();
                    window.soundFX.playClick();
                    renderPlayerTabs();
                    if (playerStates[pid]) {
                        renderActivePlayerView(playerStates[pid], true);
                    } else {
                        socket.emit('get_player_state', { player_id: pid });
                    }
                }
            });
        });

        const addBtn = document.getElementById('add-player-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => {
                renderJoinForm(true);
            });
        }
    }

    // =========================================================================
    // View 1: Join / Add Player Form
    // =========================================================================
    function renderJoinForm(isAddingAnother = false) {
        isJoinFormOpen = true;
        let selectedAvatar = AVATARS[Math.floor(Math.random() * AVATARS.length)];

        playerStage.innerHTML = `
            <div style="max-width: 400px; margin: 0 auto; width: 100%;">
                <div style="font-size: 3.5rem; margin-bottom: 8px;">🎮</div>
                <h2>${isAddingAnother ? 'Add Another Player' : 'Join the Game'}</h2>
                <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 20px;">
                    ${isAddingAnother ? 'Add a player profile to switch between on this device.' : 'Choose your nickname & avatar'}
                </p>

                <div style="text-align: left; margin-bottom: 8px;">
                    <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Nickname</label>
                    <input type="text" id="join-name-input" class="form-input" placeholder="Your Name..." maxlength="14" autofocus>
                </div>

                <div style="text-align: left; margin-bottom: 20px;">
                    <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Pick Avatar</label>
                    <div class="avatar-selector" id="avatar-picker">
                        ${AVATARS.map(av => `
                            <button class="avatar-opt-btn ${av === selectedAvatar ? 'selected' : ''}" data-avatar="${av}">
                                ${av}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <div style="display: flex; gap: 10px;">
                    ${isAddingAnother ? `<button class="btn btn-outline" id="cancel-add-btn" style="flex: 1;">Cancel</button>` : ''}
                    <button class="btn btn-primary" id="submit-join-btn" style="flex: 2; font-size: 1.15rem;">
                        ${isAddingAnother ? 'Add Player' : 'Enter Lobby ➔'}
                    </button>
                </div>
            </div>
        `;

        const nameInput = document.getElementById('join-name-input');
        nameInput.focus();

        // Avatar selector clicks
        playerStage.querySelectorAll('.avatar-opt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                playerStage.querySelectorAll('.avatar-opt-btn').forEach(b => b.classList.remove('selected'));
                e.currentTarget.classList.add('selected');
                selectedAvatar = e.currentTarget.dataset.avatar;
                window.soundFX.playClick();
            });
        });

        // Submit Join
        function submitJoin() {
            const name = nameInput.value.trim();
            if (!name) {
                nameInput.style.borderColor = 'var(--danger)';
                return;
            }

            isJoinFormOpen = false;
            lastRenderedKey = '';
            const newPlayerId = 'p_' + Math.random().toString(36).substring(2, 9);
            const newPlayer = { id: newPlayerId, name: name, avatar: selectedAvatar };
            
            localPlayers.push(newPlayer);
            activePlayerId = newPlayerId;
            saveLocalPlayers();

            window.soundFX.playJoin();

            socket.emit('join_player', {
                player_id: newPlayerId,
                name: name,
                avatar: selectedAvatar,
                is_local: true
            });

            renderPlayerTabs();
        }

        document.getElementById('submit-join-btn').addEventListener('click', submitJoin);
        nameInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') submitJoin();
        });

        if (isAddingAnother) {
            document.getElementById('cancel-add-btn').addEventListener('click', () => {
                isJoinFormOpen = false;
                lastRenderedKey = '';
                if (playerStates[activePlayerId]) {
                    renderActivePlayerView(playerStates[activePlayerId], true);
                }
                renderPlayerTabs();
            });
        }
    }

    // =========================================================================
    // View 2: Active Player Controller Stages
    // =========================================================================
    function renderActivePlayerView(fullState, forceRender = false) {
        if (!fullState) return;
        if (isJoinFormOpen && !forceRender) return;

        const newKey = getPlayerViewStateKey(fullState);
        if (!forceRender && lastRenderedPlayerId === fullState.player_id && lastRenderedKey === newKey) {
            return;
        }

        lastRenderedKey = newKey;
        lastRenderedPlayerId = fullState.player_id;
        isJoinFormOpen = false;

        const managerState = fullState.manager_state;
        const gs = fullState.game_state;
        const playerName = fullState.player_name;
        const playerAvatar = fullState.player_avatar;
        const playerScore = fullState.player_score || 0;

        if (managerState === 'hub' || managerState === 'lobby' || !gs) {
            stopQuizCountdown();
            playerStage.innerHTML = `
                <div class="controller-header">
                    <div class="controller-player-badge">
                        <span>${playerAvatar}</span>
                        <span>${escapeHtml(playerName)}</span>
                    </div>
                    <span class="badge" style="background: rgba(255,255,255,0.1);">${fullState.room_code || 'GAME'}</span>
                </div>
                <div style="padding: 40px 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 15px;">🛋️</div>
                    <h2>You're in the Lobby!</h2>
                    <p style="color: var(--text-muted); margin-top: 8px;">Look at the Host Screen. The game will begin shortly!</p>
                </div>
            `;
            return;
        }

        const gameId = gs.game_id;
        const stage = gs.stage;

        if (stage === 'scoreboard' || stage === 'game_over') {
            stopQuizCountdown();
            renderPlayerScoreboard(gs, playerName, playerAvatar);
            return;
        }

        // Game controllers
        if (gameId === 'fibbage') {
            renderFibbageController(gs);
        } else if (gameId === 'quiplash') {
            renderQuiplashController(gs);
        } else if (gameId === 'trivia') {
            renderTriviaController(gs);
        } else if (gameId === 'bible_trivia') {
            renderBibleTriviaController(gs);
        } else if (gameId === 'doodler') {
            renderDoodlerController(gs);
        }
    }

    // --- Fibbage Controller ---
    function renderFibbageController(gs) {
        let contentHtml = '';

        if (gs.stage === 'answering') {
            if (gs.has_submitted) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">✅</div>
                        <h3>Lie Submitted!</h3>
                        <p style="color: var(--accent); margin-top: 8px;">"${escapeHtml(gs.my_lie)}"</p>
                        <p style="color: var(--text-muted); margin-top: 15px;">Waiting for other players to finish...</p>
                    </div>
                `;
            } else {
                contentHtml = `
                    <div style="text-align: left;">
                        <div style="font-size: 0.85rem; font-weight: 700; color: var(--accent); margin-bottom: 6px;">PROMPT:</div>
                        <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 15px;">${escapeHtml(gs.prompt)}</div>
                        
                        <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted);">WRITE A CONVINCING LIE:</label>
                        <input type="text" id="fibbage-lie-input" class="form-input" placeholder="Your lie here..." maxlength="40" autofocus>
                        
                        <button class="btn btn-primary" id="fibbage-submit-btn" style="width: 100%; margin-top: 10px;">
                            Submit Lie ➔
                        </button>
                    </div>
                `;
            }
        } else if (gs.stage === 'voting') {
            if (gs.has_submitted) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🗳️</div>
                        <h3>Vote Cast!</h3>
                        <p style="color: var(--secondary); margin-top: 8px;">You picked: <strong>"${escapeHtml(gs.my_vote)}"</strong></p>
                        <p style="color: var(--text-muted); margin-top: 15px;">Watch the big screen for the reveal!</p>
                    </div>
                `;
            } else {
                let optionsHtml = '';
                (gs.options || []).forEach(opt => {
                    if (opt.is_own) {
                        optionsHtml += `
                            <button class="vote-choice-btn" disabled style="opacity: 0.4;">
                                ${escapeHtml(opt.text)} (Your Lie)
                            </button>
                        `;
                    } else {
                        optionsHtml += `
                            <button class="vote-choice-btn fibbage-vote-btn" data-choice="${escapeHtml(opt.text)}">
                                ${escapeHtml(opt.text)}
                            </button>
                        `;
                    }
                });

                contentHtml = `
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 700; color: var(--accent); margin-bottom: 10px;">
                            PICK THE REAL TRUTH:
                        </div>
                        <div class="controller-voting-grid">
                            ${optionsHtml}
                        </div>
                    </div>
                `;
            }
        } else if (gs.stage === 'reveal') {
            contentHtml = `
                <div style="padding: 30px 10px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">👀</div>
                    <h2>Look at the Big Screen!</h2>
                    <p style="color: var(--text-muted); margin-top: 10px;">Revealing answers and bluff scores...</p>
                </div>
            `;
        }

        renderControllerFrame(gs, contentHtml);

        // Bind events
        const submitLieBtn = document.getElementById('fibbage-submit-btn');
        if (submitLieBtn) {
            const lieInput = document.getElementById('fibbage-lie-input');
            const doSubmit = () => {
                const lie = lieInput.value.trim();
                if (lie) {
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_lie',
                        data: { lie }
                    });
                }
            };
            submitLieBtn.addEventListener('click', doSubmit);
            lieInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSubmit(); });
        }

        playerStage.querySelectorAll('.fibbage-vote-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_vote',
                    data: { choice }
                });
            });
        });

        if (gs.stage === 'answering' || gs.stage === 'voting') {
            startQuizCountdown(gs.timer !== undefined ? parseInt(gs.timer) : 45);
        } else {
            stopQuizCountdown();
        }
    }

    // --- Quiplash Controller ---
    function renderQuiplashController(gs) {
        let contentHtml = '';

        if (gs.stage === 'answering') {
            const myPrompts = gs.my_prompts || [];
            // Find first unsubmitted prompt
            const activePrompt = myPrompts.find(p => !p.submitted_answer) || myPrompts[0];

            if (myPrompts.length === 0 || myPrompts.every(p => p.submitted_answer)) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">💥</div>
                        <h3>All Quips In!</h3>
                        <p style="color: var(--text-muted); margin-top: 10px;">Get ready for the head-to-head battles on screen!</p>
                    </div>
                `;
            } else {
                contentHtml = `
                    <div style="text-align: left;">
                        ${activePrompt.image ? `<img src="${activePrompt.image}" style="max-width: 100%; border-radius: 8px; margin-bottom: 10px;">` : ''}
                        <div style="font-size: 0.85rem; font-weight: 700; color: var(--accent); margin-bottom: 6px;">PROMPT:</div>
                        <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 15px;">${escapeHtml(activePrompt.prompt)}</div>

                        <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted);">YOUR FUNNY PUNCHLINE:</label>
                        <input type="text" id="quip-answer-input" class="form-input" placeholder="Say something funny..." maxlength="50" autofocus>

                        <button class="btn btn-primary" id="quip-submit-btn" style="width: 100%; margin-top: 10px;">
                            Submit Quip ➔
                        </button>
                    </div>
                `;
            }
        } else if (gs.stage === 'battle') {
            if (gs.is_my_matchup && !gs.can_vote) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">⚔️</div>
                        <h2>THIS IS YOUR BATTLE!</h2>
                        <p style="color: var(--accent); margin-top: 10px;">Other players are voting on your punchline now!</p>
                    </div>
                `;
            } else if (gs.my_vote) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🗳️</div>
                        <h3>Vote Submitted!</h3>
                        <p style="color: var(--text-muted); margin-top: 10px;">Watch the big screen for the results!</p>
                    </div>
                `;
            } else if (gs.can_vote && gs.battle_matchup) {
                contentHtml = `
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 700; color: var(--accent); margin-bottom: 12px;">
                            VOTE FOR THE FUNNIEST ANSWER:
                        </div>
                        <div class="controller-voting-grid">
                            <button class="vote-choice-btn quip-vote-btn" data-choice="p1">
                                "${escapeHtml(gs.battle_matchup.p1_answer)}"
                            </button>
                            <button class="vote-choice-btn quip-vote-btn" data-choice="p2">
                                "${escapeHtml(gs.battle_matchup.p2_answer)}"
                            </button>
                        </div>
                    </div>
                `;
            }
        }

        renderControllerFrame(gs, contentHtml);

        const quipSubmitBtn = document.getElementById('quip-submit-btn');
        if (quipSubmitBtn) {
            const input = document.getElementById('quip-answer-input');
            const myPrompts = gs.my_prompts || [];
            const activePrompt = myPrompts.find(p => !p.submitted_answer) || myPrompts[0];

            const doSubmit = () => {
                const answer = input.value.trim();
                if (answer && activePrompt) {
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_quip',
                        data: { matchup_id: activePrompt.matchup_id, answer }
                    });
                }
            };
            quipSubmitBtn.addEventListener('click', doSubmit);
            input.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSubmit(); });
        }

        playerStage.querySelectorAll('.quip-vote-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_vote',
                    data: { choice }
                });
            });
        });

        if (gs.stage === 'answering' || gs.stage === 'battle') {
            startQuizCountdown(gs.timer !== undefined ? parseInt(gs.timer) : 45);
        } else {
            stopQuizCountdown();
        }
    }

    // --- Shared Quiz / Party Controller Countdown Timer ---
    let activeQuizTimer = null;

    function startQuizCountdown(seconds) {
        if (activeQuizTimer) {
            clearInterval(activeQuizTimer);
            activeQuizTimer = null;
        }
        let remaining = parseInt(seconds);
        if (isNaN(remaining) || remaining < 0) return;

        function tick() {
            const valEls = document.querySelectorAll('.quiz-timer-val');
            valEls.forEach(el => {
                el.textContent = Math.max(0, remaining);
            });
            const pills = document.querySelectorAll('.quiz-timer-pill, .player-header-timer');
            pills.forEach(p => {
                if (remaining <= 5 && remaining > 0) {
                    p.classList.add('urgent');
                } else {
                    p.classList.remove('urgent');
                }
            });
        }

        tick();

        activeQuizTimer = setInterval(() => {
            remaining--;
            tick();
            if (remaining <= 0) {
                clearInterval(activeQuizTimer);
                activeQuizTimer = null;
            }
        }, 1000);
    }

    function stopQuizCountdown() {
        if (activeQuizTimer) {
            clearInterval(activeQuizTimer);
            activeQuizTimer = null;
        }
    }

    // --- Trivia Dash Controller ---
    function renderTriviaController(gs) {
        let contentHtml = '';
        const qType = gs.q_type || 'multiple_choice';
        const timerSec = gs.timer !== undefined ? parseInt(gs.timer) : 30;
        const isUrgent = timerSec <= 5 && timerSec > 0;
        const timerPillHtml = `
            <div class="timer-pill quiz-timer-pill ${isUrgent ? 'urgent' : ''}">
                ⏱️ <span class="quiz-timer-val">${timerSec}</span>s
            </div>
        `;

        if (gs.stage === 'answering') {
            if (gs.has_submitted) {
                const displayChoice = Array.isArray(gs.my_choice) ? gs.my_choice.join(', ') : gs.my_choice;
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">⚡</div>
                        <h3>Answer Locked In!</h3>
                        <p style="color: var(--secondary); font-size: 1.25rem; font-weight: 800; margin-top: 8px;">
                            "${escapeHtml(displayChoice)} ${escapeHtml(gs.unit || '')}"
                        </p>
                        <div class="timer-pill quiz-timer-pill ${isUrgent ? 'urgent' : ''}" style="display: inline-flex; margin-top: 15px; font-size: 1rem; padding: 4px 14px;">
                            ⏱️ <span class="quiz-timer-val">${timerSec}</span>s remaining
                        </div>
                        <p style="color: var(--text-muted); margin-top: 15px;">Waiting for other players...</p>
                    </div>
                `;
            } else if (qType === 'slider') {
                const minVal = gs.min || 0;
                const maxVal = gs.max || 100;
                const stepVal = gs.step || 1;
                const initVal = Math.round((minVal + maxVal) / 2);

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="font-size: 0.85rem; font-weight: 800; color: var(--secondary);">
                                🎚️ ${escapeHtml(gs.category)}
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="slider-control-box">
                            <div class="slider-bubble-value">
                                <span id="trivia-slider-val">${initVal}</span> <span style="font-size: 1.2rem; color: var(--text-muted);">${escapeHtml(gs.unit || '')}</span>
                            </div>
                            <input type="range" class="interactive-slider" id="trivia-slider-input" 
                                   min="${minVal}" max="${maxVal}" step="${stepVal}" value="${initVal}">
                            <div class="slider-limits-row">
                                <span>${minVal} ${escapeHtml(gs.unit || '')}</span>
                                <span>${maxVal} ${escapeHtml(gs.unit || '')}</span>
                            </div>
                            <div class="slider-fine-tune-row">
                                <button class="slider-step-btn" id="slider-minus-btn">- ${stepVal}</button>
                                <button class="slider-step-btn" id="slider-plus-btn">+ ${stepVal}</button>
                            </div>
                        </div>
                        <button class="btn btn-primary" id="trivia-slider-submit-btn" style="width: 100%; font-size: 1.15rem; margin-top: 8px;">
                            Lock In Guess ➔
                        </button>
                    </div>
                `;
            } else if (qType === 'multi_select') {
                let tilesHtml = '';
                (gs.options || []).forEach(opt => {
                    tilesHtml += `
                        <div class="multiselect-tile" data-choice="${escapeHtml(opt)}">
                            <span>${escapeHtml(opt)}</span>
                            <span class="multiselect-check-icon">☐</span>
                        </div>
                    `;
                });

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="font-size: 0.85rem; font-weight: 800; color: var(--accent);">
                                ☑️ ${escapeHtml(gs.category)} (Select All That Apply)
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="multiselect-toggle-grid">
                            ${tilesHtml}
                        </div>
                        <button class="btn btn-primary" id="trivia-multiselect-submit-btn" style="width: 100%; font-size: 1.15rem; margin-top: 8px;">
                            Lock In Selections ➔
                        </button>
                    </div>
                `;
            } else if (qType === 'true_false') {
                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="font-size: 0.85rem; font-weight: 800; color: var(--primary);">
                                ⚡ ${escapeHtml(gs.category)}
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.25rem; font-weight: 900; margin-bottom: 20px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="tf-controller-grid">
                            <button class="tf-btn tf-btn-true trivia-opt-btn" data-choice="True">
                                <span style="font-size: 2.2rem;">🟢</span>
                                <span>TRUE</span>
                            </button>
                            <button class="tf-btn tf-btn-false trivia-opt-btn" data-choice="False">
                                <span style="font-size: 2.2rem;">🔴</span>
                                <span>FALSE</span>
                            </button>
                        </div>
                    </div>
                `;
            } else {
                let optionsHtml = '';
                (gs.options || []).forEach(opt => {
                    optionsHtml += `
                        <button class="vote-choice-btn trivia-opt-btn" data-choice="${escapeHtml(opt)}">
                            ${escapeHtml(opt)}
                        </button>
                    `;
                });

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">
                                🎯 ${escapeHtml(gs.category)}
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="controller-voting-grid">
                            ${optionsHtml}
                        </div>
                    </div>
                `;
            }
        } else if (gs.stage === 'reveal') {
            const isCorrect = gs.is_correct;
            const delta = gs.my_score_delta || 0;
            const formattedAnswer = Array.isArray(gs.correct_answer) ? gs.correct_answer.join(', ') : gs.correct_answer;

            contentHtml = `
                <div style="padding: 30px 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">${isCorrect ? '🎉' : (delta > 0 ? '👍' : '❌')}</div>
                    <h2>${isCorrect ? 'CORRECT!' : (delta > 0 ? 'CLOSE GUESS!' : 'WRONG!')}</h2>
                    <p style="color: var(--accent); font-size: 1.1rem; margin-top: 8px;">
                        Answer: <strong>"${escapeHtml(formattedAnswer)} ${escapeHtml(gs.unit || '')}"</strong>
                    </p>
                    ${delta > 0 ? `<p style="color: var(--success); font-weight: 800; font-size: 1.3rem; margin-top: 8px;">+${delta} PTS</p>` : ''}
                </div>
            `;
        }

        renderControllerFrame(gs, contentHtml);

        // Multiple choice & True/False events
        playerStage.querySelectorAll('.trivia-opt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_answer',
                    data: { choice }
                });
            });
        });

        // Slider events
        const sliderInput = document.getElementById('trivia-slider-input');
        if (sliderInput) {
            const sliderVal = document.getElementById('trivia-slider-val');
            const minusBtn = document.getElementById('slider-minus-btn');
            const plusBtn = document.getElementById('slider-plus-btn');
            const step = parseFloat(sliderInput.step) || 1;

            sliderInput.addEventListener('input', (e) => {
                if (sliderVal) sliderVal.textContent = e.target.value;
            });

            if (minusBtn) {
                minusBtn.addEventListener('click', () => {
                    const nextVal = Math.max(parseFloat(sliderInput.min), parseFloat(sliderInput.value) - step);
                    sliderInput.value = nextVal;
                    if (sliderVal) sliderVal.textContent = nextVal;
                });
            }

            if (plusBtn) {
                plusBtn.addEventListener('click', () => {
                    const nextVal = Math.min(parseFloat(sliderInput.max), parseFloat(sliderInput.value) + step);
                    sliderInput.value = nextVal;
                    if (sliderVal) sliderVal.textContent = nextVal;
                });
            }

            const sliderSubmitBtn = document.getElementById('trivia-slider-submit-btn');
            if (sliderSubmitBtn) {
                sliderSubmitBtn.addEventListener('click', () => {
                    const choice = parseFloat(sliderInput.value);
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_answer',
                        data: { choice }
                    });
                });
            }
        }

        // Multi-select events
        const multiTiles = playerStage.querySelectorAll('.multiselect-tile');
        if (multiTiles.length > 0) {
            const selectedChoices = new Set();

            multiTiles.forEach(tile => {
                tile.addEventListener('click', (e) => {
                    const opt = e.currentTarget.dataset.choice;
                    const icon = e.currentTarget.querySelector('.multiselect-check-icon');
                    if (selectedChoices.has(opt)) {
                        selectedChoices.delete(opt);
                        e.currentTarget.classList.remove('is-checked');
                        if (icon) icon.textContent = '☐';
                    } else {
                        selectedChoices.add(opt);
                        e.currentTarget.classList.add('is-checked');
                        if (icon) icon.textContent = '☑';
                    }
                    window.soundFX.playClick();
                });
            });

            const multiSubmitBtn = document.getElementById('trivia-multiselect-submit-btn');
            if (multiSubmitBtn) {
                multiSubmitBtn.addEventListener('click', () => {
                    const choice = Array.from(selectedChoices);
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_answer',
                        data: { choice }
                    });
                });
            }
        }

        if (gs.stage === 'answering') {
            startQuizCountdown(timerSec);
        } else {
            stopQuizCountdown();
        }
    }

    // --- Bible Trivia Controller ---
    function renderBibleTriviaController(gs) {
        let contentHtml = '';
        const qType = gs.q_type || 'multiple_choice';
        const timerSec = gs.timer !== undefined ? parseInt(gs.timer) : 30;
        const isUrgent = timerSec <= 5 && timerSec > 0;
        const timerPillHtml = `
            <div class="timer-pill quiz-timer-pill ${isUrgent ? 'urgent' : ''}">
                ⏱️ <span class="quiz-timer-val">${timerSec}</span>s
            </div>
        `;

        if (gs.stage === 'answering') {
            if (gs.has_submitted) {
                const displayChoice = Array.isArray(gs.my_choice) ? gs.my_choice.join(', ') : gs.my_choice;
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">📜</div>
                        <h3>Answer Locked In!</h3>
                        <p style="color: var(--accent); font-size: 1.25rem; font-weight: 800; margin-top: 8px;">
                            "${escapeHtml(displayChoice)} ${escapeHtml(gs.unit || '')}"
                        </p>
                        <div class="timer-pill quiz-timer-pill ${isUrgent ? 'urgent' : ''}" style="display: inline-flex; margin-top: 15px; font-size: 1rem; padding: 4px 14px;">
                            ⏱️ <span class="quiz-timer-val">${timerSec}</span>s remaining
                        </div>
                        <p style="color: var(--text-muted); margin-top: 15px;">Waiting for other players...</p>
                    </div>
                `;
            } else if (qType === 'slider') {
                const minVal = gs.min || 0;
                const maxVal = gs.max || 100;
                const stepVal = gs.step || 1;
                const initVal = Math.round((minVal + maxVal) / 2);

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span class="testament-tag">${escapeHtml(gs.testament || 'Scripture')}</span>
                                <span style="font-size: 0.85rem; font-weight: 800; color: var(--secondary);">
                                    🎚️ ${escapeHtml(gs.category)}
                                </span>
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="slider-control-box">
                            <div class="slider-bubble-value">
                                <span id="bible-slider-val">${initVal}</span> <span style="font-size: 1.2rem; color: var(--text-muted);">${escapeHtml(gs.unit || '')}</span>
                            </div>
                            <input type="range" class="interactive-slider" id="bible-slider-input" 
                                   min="${minVal}" max="${maxVal}" step="${stepVal}" value="${initVal}">
                            <div class="slider-limits-row">
                                <span>${minVal} ${escapeHtml(gs.unit || '')}</span>
                                <span>${maxVal} ${escapeHtml(gs.unit || '')}</span>
                            </div>
                            <div class="slider-fine-tune-row">
                                <button class="slider-step-btn" id="bible-slider-minus-btn">- ${stepVal}</button>
                                <button class="slider-step-btn" id="bible-slider-plus-btn">+ ${stepVal}</button>
                            </div>
                        </div>
                        <button class="btn btn-primary" id="bible-slider-submit-btn" style="width: 100%; font-size: 1.15rem; margin-top: 8px;">
                            Lock In Biblical Guess ➔
                        </button>
                    </div>
                `;
            } else if (qType === 'multi_select') {
                let tilesHtml = '';
                (gs.options || []).forEach(opt => {
                    tilesHtml += `
                        <div class="multiselect-tile bible-multi-tile" data-choice="${escapeHtml(opt)}">
                            <span>${escapeHtml(opt)}</span>
                            <span class="multiselect-check-icon">☐</span>
                        </div>
                    `;
                });

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span class="testament-tag">${escapeHtml(gs.testament || 'Scripture')}</span>
                                <span style="font-size: 0.85rem; font-weight: 800; color: var(--accent);">
                                    ☑️ ${escapeHtml(gs.category)} (Select All That Apply)
                                </span>
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="multiselect-toggle-grid">
                            ${tilesHtml}
                        </div>
                        <button class="btn btn-primary" id="bible-multiselect-submit-btn" style="width: 100%; font-size: 1.15rem; margin-top: 8px;">
                            Lock In Selections ➔
                        </button>
                    </div>
                `;
            } else if (qType === 'true_false') {
                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span class="testament-tag">${escapeHtml(gs.testament || 'Scripture')}</span>
                                <span style="font-size: 0.85rem; font-weight: 800; color: var(--primary);">
                                    ⚡ ${escapeHtml(gs.category)}
                                </span>
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.25rem; font-weight: 900; margin-bottom: 20px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="tf-controller-grid">
                            <button class="tf-btn tf-btn-true bible-opt-btn" data-choice="True">
                                <span style="font-size: 2.2rem;">🟢</span>
                                <span>TRUE / SCRIPTURE</span>
                            </button>
                            <button class="tf-btn tf-btn-false bible-opt-btn" data-choice="False">
                                <span style="font-size: 2.2rem;">🔴</span>
                                <span>FALSE / MYTH</span>
                            </button>
                        </div>
                    </div>
                `;
            } else {
                let optionsHtml = '';
                (gs.options || []).forEach(opt => {
                    optionsHtml += `
                        <button class="vote-choice-btn bible-opt-btn" data-choice="${escapeHtml(opt)}">
                            ${escapeHtml(opt)}
                        </button>
                    `;
                });

                contentHtml = `
                    <div>
                        <div class="quiz-header-row">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span class="testament-tag">${escapeHtml(gs.testament || 'Scripture')}</span>
                                <span style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">
                                    🎯 ${escapeHtml(gs.category)}
                                </span>
                            </div>
                            ${timerPillHtml}
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 15px;">
                            ${escapeHtml(gs.question)}
                        </div>
                        <div class="controller-voting-grid">
                            ${optionsHtml}
                        </div>
                    </div>
                `;
            }
        } else if (gs.stage === 'reveal') {
            const isCorrect = gs.is_correct;
            const delta = gs.my_score_delta || 0;
            const formattedAnswer = Array.isArray(gs.correct_answer) ? gs.correct_answer.join(', ') : gs.correct_answer;

            contentHtml = `
                <div style="padding: 20px 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">${isCorrect ? '🌟' : (delta > 0 ? '👍' : '❌')}</div>
                    <h2>${isCorrect ? 'SCRIPTURE ACCURATE!' : (delta > 0 ? 'CLOSE ESTIMATE!' : 'INCORRECT!')}</h2>
                    <p style="color: var(--accent); font-size: 1.1rem; margin-top: 8px;">
                        Answer: <strong>"${escapeHtml(formattedAnswer)} ${escapeHtml(gs.unit || '')}"</strong>
                    </p>
                    ${delta > 0 ? `<p style="color: var(--success); font-weight: 800; font-size: 1.3rem; margin-top: 8px;">+${delta} PTS</p>` : ''}
                    
                    ${gs.verse_ref ? `
                        <div style="background: rgba(255, 209, 102, 0.1); border: 1px solid var(--accent); border-radius: 8px; padding: 12px; margin-top: 15px;">
                            <div style="font-weight: 800; color: var(--accent);">📖 ${escapeHtml(gs.verse_ref)}</div>
                            ${gs.verse_text ? `<div style="font-style: italic; font-size: 0.9rem; margin-top: 6px;">"${escapeHtml(gs.verse_text)}"</div>` : ''}
                            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 8px;">${escapeHtml(gs.copyright || '')}</div>
                        </div>
                    ` : ''}
                </div>
            `;
        }

        renderControllerFrame(gs, contentHtml);

        // Multiple choice & True/False events
        playerStage.querySelectorAll('.bible-opt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_answer',
                    data: { choice }
                });
            });
        });

        // Slider events
        const sliderInput = document.getElementById('bible-slider-input');
        if (sliderInput) {
            const sliderVal = document.getElementById('bible-slider-val');
            const minusBtn = document.getElementById('bible-slider-minus-btn');
            const plusBtn = document.getElementById('bible-slider-plus-btn');
            const step = parseFloat(sliderInput.step) || 1;

            sliderInput.addEventListener('input', (e) => {
                if (sliderVal) sliderVal.textContent = e.target.value;
            });

            if (minusBtn) {
                minusBtn.addEventListener('click', () => {
                    const nextVal = Math.max(parseFloat(sliderInput.min), parseFloat(sliderInput.value) - step);
                    sliderInput.value = nextVal;
                    if (sliderVal) sliderVal.textContent = nextVal;
                });
            }

            if (plusBtn) {
                plusBtn.addEventListener('click', () => {
                    const nextVal = Math.min(parseFloat(sliderInput.max), parseFloat(sliderInput.value) + step);
                    sliderInput.value = nextVal;
                    if (sliderVal) sliderVal.textContent = nextVal;
                });
            }

            const sliderSubmitBtn = document.getElementById('bible-slider-submit-btn');
            if (sliderSubmitBtn) {
                sliderSubmitBtn.addEventListener('click', () => {
                    const choice = parseFloat(sliderInput.value);
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_answer',
                        data: { choice }
                    });
                });
            }
        }

        // Multi-select events
        const multiTiles = playerStage.querySelectorAll('.bible-multi-tile');
        if (multiTiles.length > 0) {
            const selectedChoices = new Set();

            multiTiles.forEach(tile => {
                tile.addEventListener('click', (e) => {
                    const opt = e.currentTarget.dataset.choice;
                    const icon = e.currentTarget.querySelector('.multiselect-check-icon');
                    if (selectedChoices.has(opt)) {
                        selectedChoices.delete(opt);
                        e.currentTarget.classList.remove('is-checked');
                        if (icon) icon.textContent = '☐';
                    } else {
                        selectedChoices.add(opt);
                        e.currentTarget.classList.add('is-checked');
                        if (icon) icon.textContent = '☑';
                    }
                    window.soundFX.playClick();
                });
            });

            const multiSubmitBtn = document.getElementById('bible-multiselect-submit-btn');
            if (multiSubmitBtn) {
                multiSubmitBtn.addEventListener('click', () => {
                    const choice = Array.from(selectedChoices);
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_answer',
                        data: { choice }
                    });
                });
            }
        }

        if (gs.stage === 'answering') {
            startQuizCountdown(timerSec);
        } else {
            stopQuizCountdown();
        }
    }

    let activeDoodleTimer = null;

    // --- Doodle Guess Controller ---
    function renderDoodlerController(gs) {
        let contentHtml = '';

        if (gs.stage === 'drawing') {
            if (gs.is_artist) {
                if (gs.has_submitted) {
                    if (activeDoodleTimer) {
                        clearInterval(activeDoodleTimer);
                        activeDoodleTimer = null;
                    }
                    contentHtml = `
                        <div style="padding: 30px 10px;">
                            <div style="font-size: 3rem; margin-bottom: 10px;">🎨</div>
                            <h3>Drawing Submitted!</h3>
                            <p style="color: var(--text-muted); margin-top: 10px;">Watch other players bluff fake titles!</p>
                        </div>
                    `;
                } else {
                    contentHtml = `
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <div style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">YOUR SECRET PROMPT:</div>
                                <div class="timer-pill" id="doodle-timer-pill" style="font-size: 0.95rem; padding: 2px 10px;">⏱️ <span id="doodle-timer-val">${gs.timer || 45}</span>s</div>
                            </div>
                            <div style="font-size: 1.3rem; font-weight: 900; margin-bottom: 10px;">"${escapeHtml(gs.prompt)}"</div>

                            <div class="canvas-toolbar">
                                <div class="color-swatch active" style="background: #000000;" data-color="#000000"></div>
                                <div class="color-swatch" style="background: #e94560;" data-color="#e94560"></div>
                                <div class="color-swatch" style="background: #4a90e2;" data-color="#4a90e2"></div>
                                <div class="color-swatch" style="background: #06d6a0;" data-color="#06d6a0"></div>
                                <button class="btn btn-outline btn-sm" id="clear-canvas-btn">Clear</button>
                            </div>

                            <div class="canvas-wrapper">
                                <canvas id="doodle-canvas" width="300" height="240" style="display: block; cursor: crosshair;"></canvas>
                            </div>

                            <button class="btn btn-primary" id="doodle-submit-btn" style="width: 100%; margin-top: 10px;">
                                Submit Drawing ➔
                            </button>
                        </div>
                    `;
                }
            } else {
                if (activeDoodleTimer) {
                    clearInterval(activeDoodleTimer);
                    activeDoodleTimer = null;
                }
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3.5rem; margin-bottom: 10px;">${gs.artist_avatar}</div>
                        <h3>${escapeHtml(gs.artist_name)} is Drawing!</h3>
                        <p style="color: var(--text-muted); margin-top: 10px;">Look at the big screen to see what they draw...</p>
                    </div>
                `;
            }
        } else if (gs.stage === 'bluffing') {
            if (activeDoodleTimer) {
                clearInterval(activeDoodleTimer);
                activeDoodleTimer = null;
            }
            if (gs.is_artist) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🖼️</div>
                        <h3>Players are guessing your drawing!</h3>
                    </div>
                `;
            } else if (gs.has_submitted) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">✍️</div>
                        <h3>Fake Title Submitted!</h3>
                        <p style="color: var(--accent); margin-top: 8px;">"${escapeHtml(gs.my_bluff)}"</p>
                    </div>
                `;
            } else {
                contentHtml = `
                    <div style="text-align: left;">
                        <div style="font-size: 0.9rem; font-weight: 700; color: var(--accent); margin-bottom: 10px;">
                            WRITE A FAKE TITLE FOR THIS ARTWORK:
                        </div>
                        <input type="text" id="doodle-bluff-input" class="form-input" placeholder="What is this drawing of?..." maxlength="40" autofocus>
                        <button class="btn btn-primary" id="doodle-bluff-btn" style="width: 100%;">
                            Submit Title ➔
                        </button>
                    </div>
                `;
            }
        } else if (gs.stage === 'voting') {
            if (activeDoodleTimer) {
                clearInterval(activeDoodleTimer);
                activeDoodleTimer = null;
            }
            if (gs.is_artist) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🗳️</div>
                        <h3>Players are voting on the real title!</h3>
                    </div>
                `;
            } else if (gs.has_submitted) {
                contentHtml = `
                    <div style="padding: 30px 10px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🗳️</div>
                        <h3>Vote Locked In!</h3>
                    </div>
                `;
            } else {
                let optionsHtml = '';
                (gs.options || []).forEach(opt => {
                    if (opt.is_own) {
                        optionsHtml += `<button class="vote-choice-btn" disabled style="opacity: 0.4;">${escapeHtml(opt.text)} (Your Bluff)</button>`;
                    } else {
                        optionsHtml += `<button class="vote-choice-btn doodle-vote-btn" data-choice="${escapeHtml(opt.text)}">${escapeHtml(opt.text)}</button>`;
                    }
                });

                contentHtml = `
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 700; color: var(--accent); margin-bottom: 10px;">
                            WHICH ONE IS THE REAL TITLE?
                        </div>
                        <div class="controller-voting-grid">
                            ${optionsHtml}
                        </div>
                    </div>
                `;
            }
        } else if (gs.stage === 'reveal') {
            if (activeDoodleTimer) {
                clearInterval(activeDoodleTimer);
                activeDoodleTimer = null;
            }
            contentHtml = `
                <div style="padding: 30px 10px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">👀</div>
                    <h2>Check the Big Screen!</h2>
                </div>
            `;
        }

        renderControllerFrame(gs, contentHtml);

        // Drawing Canvas wiring
        const canvas = document.getElementById('doodle-canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.lineWidth = 4;
            let drawing = false;
            let currentColor = '#000000';

            // Start artist live countdown timer
            if (activeDoodleTimer) {
                clearInterval(activeDoodleTimer);
                activeDoodleTimer = null;
            }
            let remaining = parseInt(gs.timer) || 45;
            const timerValEl = document.getElementById('doodle-timer-val');
            const timerPillEl = document.getElementById('doodle-timer-pill');

            activeDoodleTimer = setInterval(() => {
                remaining -= 1;
                if (timerValEl) {
                    timerValEl.textContent = Math.max(0, remaining);
                }
                if (timerPillEl && remaining <= 5) {
                    timerPillEl.classList.add('urgent');
                }
                if (remaining <= 0) {
                    clearInterval(activeDoodleTimer);
                    activeDoodleTimer = null;
                    const dataUrl = canvas.toDataURL('image/png');
                    lastRenderedKey = '';
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_drawing',
                        data: { drawing: dataUrl }
                    });
                }
            }, 1000);

            playerStage.querySelectorAll('.color-swatch').forEach(swatch => {
                swatch.addEventListener('click', (e) => {
                    playerStage.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    currentColor = e.currentTarget.dataset.color;
                    ctx.strokeStyle = currentColor;
                });
            });

            document.getElementById('clear-canvas-btn').addEventListener('click', () => {
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                const dataUrl = canvas.toDataURL('image/png');
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'draft_drawing',
                    data: { drawing: dataUrl }
                });
            });

            function getCanvasPos(e) {
                const rect = canvas.getBoundingClientRect();
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;
                return {
                    x: (clientX - rect.left) * (canvas.width / rect.width),
                    y: (clientY - rect.top) * (canvas.height / rect.height)
                };
            }

            function startDraw(e) {
                drawing = true;
                ctx.beginPath();
                const pos = getCanvasPos(e);
                ctx.moveTo(pos.x, pos.y);
                ctx.strokeStyle = currentColor;
                e.preventDefault();
            }

            function moveDraw(e) {
                if (!drawing) return;
                const pos = getCanvasPos(e);
                ctx.lineTo(pos.x, pos.y);
                ctx.stroke();
                e.preventDefault();
            }

            function stopDraw() {
                if (!drawing) return;
                drawing = false;
                const dataUrl = canvas.toDataURL('image/png');
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'draft_drawing',
                    data: { drawing: dataUrl }
                });
            }

            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', moveDraw);
            window.addEventListener('mouseup', stopDraw);

            canvas.addEventListener('touchstart', startDraw, { passive: false });
            canvas.addEventListener('touchmove', moveDraw, { passive: false });
            canvas.addEventListener('touchend', stopDraw);

            document.getElementById('doodle-submit-btn').addEventListener('click', () => {
                if (activeDoodleTimer) {
                    clearInterval(activeDoodleTimer);
                    activeDoodleTimer = null;
                }
                const dataUrl = canvas.toDataURL('image/png');
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_drawing',
                    data: { drawing: dataUrl }
                });
            });
        }

        // Bluff submit
        const bluffBtn = document.getElementById('doodle-bluff-btn');
        if (bluffBtn) {
            const input = document.getElementById('doodle-bluff-input');
            const doSubmit = () => {
                const bluff = input.value.trim();
                if (bluff) {
                    lastRenderedKey = '';
                    window.soundFX.playClick();
                    socket.emit('player_action', {
                        player_id: activePlayerId,
                        action: 'submit_bluff',
                        data: { bluff }
                    });
                }
            };
            bluffBtn.addEventListener('click', doSubmit);
            input.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSubmit(); });
        }

        playerStage.querySelectorAll('.doodle-vote-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                lastRenderedKey = '';
                window.soundFX.playClick();
                socket.emit('player_action', {
                    player_id: activePlayerId,
                    action: 'submit_vote',
                    data: { choice }
                });
            });
        });
    }

    // --- Scoreboard / Game Over ---
    function renderPlayerScoreboard(gs, playerName, playerAvatar) {
        const topPlayers = gs.leaderboard || [];
        const myRank = topPlayers.findIndex(p => p.pid === activePlayerId) + 1;
        const myScore = gs.my_score || 0;
        const myDelta = gs.my_score_delta || 0;

        playerStage.innerHTML = `
            <div class="controller-header">
                <div class="controller-player-badge">
                    <span>${playerAvatar}</span>
                    <span>${escapeHtml(playerName)}</span>
                </div>
                <div class="badge" style="background: var(--accent); color: #000;">
                    ${myScore} PTS
                </div>
            </div>
            <div style="padding: 30px 10px;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">
                    ${myRank === 1 ? '🥇' : myRank === 2 ? '🥈' : myRank === 3 ? '🥉' : '🏆'}
                </div>
                <h2>${gs.stage === 'game_over' ? 'Final Standings' : `Round ${gs.round} Complete!`}</h2>
                <p style="font-size: 1.3rem; font-weight: 800; margin-top: 10px; color: var(--accent);">
                    Rank #${myRank || 1} • ${myScore} Points
                </p>
                ${myDelta > 0 ? `<p style="color: var(--success); font-weight: 700; margin-top: 5px;">+${myDelta} pts this round!</p>` : ''}
                <p style="color: var(--text-muted); margin-top: 15px;">Look at the Host Screen for full leaderboard</p>
            </div>
        `;
    }

    function renderControllerFrame(gs, contentHtml) {
        const isTimedStage = (gs.stage === 'answering' || gs.stage === 'voting' || gs.stage === 'bluffing' || gs.stage === 'battle');
        const hasTimer = isTimedStage && (gs.timer !== undefined && gs.timer !== null);
        const timerSec = hasTimer ? parseInt(gs.timer) : 0;
        const isUrgent = hasTimer && (timerSec <= 5 && timerSec > 0);

        playerStage.innerHTML = `
            <div class="controller-header">
                <div class="controller-player-badge">
                    <span>${gs.my_avatar || '👤'}</span>
                    <span>${escapeHtml(gs.my_name || 'Player')}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    ${hasTimer ? `
                        <div class="timer-pill player-header-timer ${isUrgent ? 'urgent' : ''}">
                            ⏱️ <span class="quiz-timer-val">${timerSec}</span>s
                        </div>
                    ` : ''}
                    <span class="badge" style="background: rgba(255,255,255,0.1);">R${gs.round || 1}</span>
                    <span class="badge" style="background: var(--accent); color: #000; font-weight: 900;">${gs.my_score || 0} PTS</span>
                </div>
            </div>
            ${contentHtml}
        `;
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
});
