document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const hostStage = document.getElementById('host-stage');
    const navRoomCode = document.getElementById('nav-room-code');
    const navJoinUrl = document.getElementById('nav-join-url');
    const muteToggleBtn = document.getElementById('mute-toggle-btn');
    const returnHubBtn = document.getElementById('return-hub-btn');
    const hostForceNextBtn = document.getElementById('host-force-next-btn');

    let currentHostState = null;
    let primaryJoinUrl = window.location.origin + '/play';
    let previousPlayersCount = 0;
    let previousStage = '';

    // 1. Fetch Network Info (IPs for Hotspot and LAN)
    fetch('/api/network')
        .then(r => r.json())
        .then(data => {
            if (data.urls && data.urls.length > 0) {
                primaryJoinUrl = data.primary_url || data.urls[0];
                navJoinUrl.textContent = primaryJoinUrl.replace('http://', '');
            }
            if (currentHostState && currentHostState.manager_state === 'lobby') {
                renderLobbyView(currentHostState);
            }
        })
        .catch(() => {
            navJoinUrl.textContent = window.location.host + '/play';
        });

    // 2. Sound Mute Toggle
    function updateMuteButton() {
        muteToggleBtn.textContent = window.soundFX.isMuted ? '🔇 SFX: OFF' : '🔊 SFX: ON';
    }
    updateMuteButton();

    muteToggleBtn.addEventListener('click', () => {
        const isMuted = window.soundFX.toggleMute();
        updateMuteButton();
    });

    // 3. Socket Connection & Host Registration
    socket.on('connect', () => {
        socket.emit('join_host');
    });

    socket.on('host_update', (state) => {
        currentHostState = state;
        handleStateUpdate(state);
    });

    socket.on('error_message', (data) => {
        alert(data.message || 'Error occurred');
    });

    // 4. Navigation & Host Control Buttons
    const restartSessionBtn = document.getElementById('restart-session-btn');
    if (restartSessionBtn) {
        restartSessionBtn.addEventListener('click', () => {
            if (confirm('Reset question and prompt history for all games in this session?')) {
                socket.emit('restart_session', { reset_scores: false });
                window.soundFX.playClick();
            }
        });
    }

    returnHubBtn.addEventListener('click', () => {
        if (confirm('Return to the Games Hub?')) {
            socket.emit('return_to_hub');
        }
    });

    hostForceNextBtn.addEventListener('click', () => {
        socket.emit('host_advance');
        window.soundFX.playClick();
    });

    document.getElementById('host-brand-btn').addEventListener('click', () => {
        if (currentHostState && currentHostState.manager_state !== 'hub') {
            if (confirm('Return to Games Hub?')) {
                socket.emit('return_to_hub');
            }
        }
    });

    // 5. State Dispatcher
    function handleStateUpdate(state) {
        navRoomCode.textContent = state.room_code || 'GAME';

        // Sound triggers on state changes
        if (state.players_count > previousPlayersCount) {
            window.soundFX.playJoin();
        }
        previousPlayersCount = state.players_count;

        // Button visibility
        if (state.manager_state === 'hub') {
            returnHubBtn.style.display = 'none';
            hostForceNextBtn.style.display = 'none';
            renderHubView(state);
        } else if (state.manager_state === 'lobby') {
            returnHubBtn.style.display = 'inline-flex';
            hostForceNextBtn.style.display = 'none';
            renderLobbyView(state);
        } else if (state.manager_state === 'in_game') {
            returnHubBtn.style.display = 'inline-flex';
            hostForceNextBtn.style.display = 'inline-flex';
            renderInGameView(state);
        }
    }

    // =========================================================================
    // View 1: Games Hub
    // =========================================================================
    function renderHubView(state) {
        const games = state.available_games || [];
        let html = `
            <div class="hub-header">
                <h1>SELECT A PARTY GAME</h1>
                <p style="color: var(--text-muted); font-size: 1.2rem;">Choose an experience to start your local room lobby</p>
            </div>
            <div class="hub-games-grid">
        `;

        games.forEach(g => {
            html += `
                <div class="game-hub-card" data-game-id="${g.id}">
                    <div class="game-card-icon">${g.icon}</div>
                    <div class="game-card-category">${g.category}</div>
                    <div class="game-card-title">${g.name}</div>
                    <div class="game-card-desc">${g.description}</div>
                    <div class="game-card-meta">
                        <span>👥 ${g.min_players}-${g.max_players} Players</span>
                        <span>⏱️ ${g.estimated_time}</span>
                    </div>
                    <button class="btn btn-primary select-game-btn" data-game-id="${g.id}">
                        Play This Game ➔
                    </button>
                </div>
            `;
        });

        html += `</div>`;
        hostStage.innerHTML = html;

        hostStage.querySelectorAll('.select-game-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const gameId = e.currentTarget.dataset.gameId;
                window.soundFX.playClick();
                socket.emit('select_game', { game_id: gameId });
            });
        });
    }

    // =========================================================================
    // View 2: Lobby Screen with QR Code
    // =========================================================================
    function renderLobbyView(state) {
        const game = state.selected_game || {};
        const players = state.players || [];
        const minPlayers = game.min_players || 2;
        const canStart = players.length >= 1; // Allow 1+ for testing & virtual multiplayers

        let playersHtml = '';
        if (players.length === 0) {
            playersHtml = `
                <div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">📱</div>
                    <h3>Waiting for players to join...</h3>
                    <p>Scan the QR code or enter the URL on your phone or second window!</p>
                </div>
            `;
        } else {
            players.forEach(p => {
                playersHtml += `
                    <div class="player-bubble">
                        <div class="player-bubble-avatar">${p.avatar || '👤'}</div>
                        <div class="player-bubble-name">${escapeHtml(p.name)}</div>
                    </div>
                `;
            });
        }

        hostStage.innerHTML = `
            <div class="lobby-layout">
                <!-- QR & Connection Card -->
                <div class="qr-join-card">
                    <span class="badge" style="background: var(--accent); color: var(--text-dark); margin-bottom: 10px;">
                        ${game.name || 'Party Game'}
                    </span>
                    <h3 style="margin: 10px 0;">Scan to Join</h3>
                    
                    <div class="qr-canvas-wrapper" id="lobby-qr-code"></div>

                    <div style="margin-top: 10px;">
                        <div class="join-code-label">Or go to URL</div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: var(--secondary); word-break: break-all;">
                            ${primaryJoinUrl}
                        </div>
                    </div>
                    <p class="qr-scan-instruction" style="margin-top: 15px;">
                        Point your phone camera at the screen to join instantly!
                    </p>
                </div>

                <!-- Players Area & Launch Options -->
                <div class="lobby-players-area">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h2>Lobby (${players.length} Joined)</h2>
                            <p style="color: var(--text-muted);">${game.description || ''}</p>
                        </div>
                        <div style="display: flex; gap: 15px; align-items: center;">
                            <label style="font-size: 0.9rem; color: var(--text-muted);">
                                Rounds:
                                <select id="rounds-select" style="background: #1e293b; color: #fff; border: 1px solid var(--card-border); padding: 4px 8px; border-radius: 4px; margin-left: 5px;">
                                    <option value="3" ${state.game_options.rounds == 3 ? 'selected' : ''}>3 Rounds</option>
                                    <option value="5" ${state.game_options.rounds == 5 ? 'selected' : ''}>5 Rounds</option>
                                </select>
                            </label>
                        </div>
                    </div>

                    <div class="players-grid">
                        ${playersHtml}
                    </div>

                    <div class="lobby-actions">
                        <button class="btn btn-outline" id="lobby-back-hub-btn">
                            ← Choose Different Game
                        </button>
                        <button class="btn btn-primary" id="lobby-start-btn" ${!canStart ? 'disabled' : ''} style="font-size: 1.3rem; padding: 14px 35px;">
                            🚀 Start Game (${players.length} Ready)
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Render QR Code using standalone offline generator
        new window.QRCode('lobby-qr-code', {
            text: primaryJoinUrl,
            width: 180,
            height: 180
        });

        // Event listeners
        document.getElementById('lobby-back-hub-btn').addEventListener('click', () => {
            socket.emit('return_to_hub');
        });

        document.getElementById('lobby-start-btn').addEventListener('click', () => {
            window.soundFX.playStart();
            socket.emit('start_game');
        });

        document.getElementById('rounds-select').addEventListener('change', (e) => {
            socket.emit('select_game', {
                game_id: state.selected_game.id,
                options: { rounds: parseInt(e.target.value) }
            });
        });
    }

    // =========================================================================
    // View 3: In-Game TV Stages
    // =========================================================================
    function renderInGameView(state) {
        const gameState = state.game_state;
        if (!gameState) return;

        const gameId = gameState.game_id;
        const stage = gameState.stage;

        if (stage !== previousStage) {
            if (stage === 'game_over') {
                window.soundFX.playWin();
                window.launchConfetti();
            } else if (stage === 'answering') {
                window.soundFX.playStart();
            }
            previousStage = stage;
        }

        if (stage === 'game_over') {
            renderPodiumView(gameState);
            return;
        }

        if (stage === 'scoreboard') {
            renderScoreboardView(gameState);
            return;
        }

        // Render game-specific stages
        if (gameId === 'fibbage') {
            renderFibbageTV(gameState);
        } else if (gameId === 'quiplash') {
            renderQuiplashTV(gameState);
        } else if (gameId === 'trivia') {
            renderTriviaTV(gameState);
        } else if (gameId === 'bible_trivia') {
            renderBibleTriviaTV(gameState);
        } else if (gameId === 'doodler') {
            renderDoodlerTV(gameState);
        }
    }

    // --- Fibbage TV ---
    function renderFibbageTV(gs) {
        const isUrgent = gs.timer <= 5 && gs.timer > 0;
        let contentHtml = '';

        if (gs.stage === 'answering') {
            contentHtml = `
                <div class="prompt-hero-box">
                    ${gs.prompt_image ? `<img src="${gs.prompt_image}" class="prompt-hero-image">` : ''}
                    <div class="prompt-hero-text">${gs.prompt}</div>
                    <p style="color: var(--accent); margin-top: 15px; font-size: 1.2rem; font-weight: 700;">
                        ✍️ Players are writing their lies...
                    </p>
                </div>
                <div class="players-progress-bar">
                    ${renderPlayersStatusTags(gs.players_status)}
                </div>
            `;
        } else if (gs.stage === 'voting') {
            let optionsHtml = '';
            (gs.options || []).forEach(opt => {
                optionsHtml += `
                    <div class="choice-tv-card">
                        <span>${escapeHtml(opt.text)}</span>
                    </div>
                `;
            });

            contentHtml = `
                <div class="prompt-hero-box" style="padding: 25px;">
                    <div style="font-size: 1.8rem; font-weight: 800;">${gs.prompt}</div>
                    <p style="color: var(--secondary); font-size: 1.1rem; margin-top: 8px;">
                        🗳️ Vote for the REAL truth on your controller!
                    </p>
                </div>
                <div class="voting-choices-grid">
                    ${optionsHtml}
                </div>
                <div class="players-progress-bar" style="margin-top: 20px;">
                    ${renderPlayersStatusTags(gs.players_status)}
                </div>
            `;
        } else if (gs.stage === 'reveal') {
            const currentRevealIdx = gs.reveal_index;
            let optionsHtml = '';

            (gs.options || []).forEach((opt, idx) => {
                const isRevealed = idx <= currentRevealIdx;
                const isCurrent = idx === currentRevealIdx;
                let cardClasses = 'choice-tv-card';

                let detailsHtml = '';
                if (isRevealed) {
                    if (opt.is_truth) {
                        cardClasses += ' is-real-truth';
                        detailsHtml = `<div class="badge" style="background: var(--success); color: #fff; margin-top: 8px;">🌟 THE TRUTH! (+1000 PTS)</div>`;
                    } else {
                        cardClasses += ' is-fake-lie';
                        detailsHtml = `<div class="author-tag">Written by: <strong>${escapeHtml(opt.author_name || 'Nobody')}</strong></div>`;
                    }

                    if (opt.voters && opt.voters.length > 0) {
                        detailsHtml += `<div class="voters-pill-list">`;
                        opt.voters.forEach(v => {
                            detailsHtml += `<span class="voter-mini-badge">${v.avatar} ${escapeHtml(v.name)}</span>`;
                        });
                        detailsHtml += `</div>`;
                    }
                } else {
                    detailsHtml = `<div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 8px;">Waiting...</div>`;
                }

                if (isCurrent) cardClasses += ' active-reveal';

                optionsHtml += `
                    <div class="${cardClasses}">
                        <span>${escapeHtml(opt.text)}</span>
                        ${detailsHtml}
                    </div>
                `;
            });

            contentHtml = `
                <div class="prompt-hero-box" style="padding: 20px;">
                    <div style="font-size: 1.6rem; font-weight: 800;">${gs.prompt}</div>
                </div>
                <div class="voting-choices-grid">
                    ${optionsHtml}
                </div>
            `;
        }

        hostStage.innerHTML = `
            <div class="game-stage-wrapper">
                <div class="stage-top-bar">
                    <div class="stage-round-badge">Round ${gs.round} / ${gs.total_rounds}</div>
                    <div class="timer-pill ${isUrgent ? 'urgent' : ''}">⏱️ ${gs.timer}s</div>
                </div>
                ${contentHtml}
            </div>
        `;
    }

    // --- Quiplash TV ---
    function renderQuiplashTV(gs) {
        const isUrgent = gs.timer <= 5 && gs.timer > 0;
        let contentHtml = '';

        if (gs.stage === 'answering') {
            contentHtml = `
                <div class="prompt-hero-box">
                    <div class="prompt-hero-text">💥 QUIPLASH: WRITE YOUR PUNCHLINES!</div>
                    <p style="color: var(--accent); margin-top: 15px; font-size: 1.2rem; font-weight: 700;">
                        Enter your wittiest responses on your phone...
                    </p>
                </div>
                <div class="players-progress-bar">
                    ${renderPlayersStatusTags(gs.players_status)}
                </div>
            `;
        } else if (gs.stage === 'battle') {
            const m = gs.matchup;
            if (!m) return;

            let votersHtml = '';
            if (m.revealed && m.voter_avatars) {
                votersHtml = `
                    <div style="text-align: center; margin-top: 20px;">
                        <span style="color: var(--text-muted); font-size: 0.9rem;">Votes Cast:</span>
                        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; max-width: 600px; margin: 8px auto 0;">
                            ${m.voter_avatars.map(v => `<span style="font-size: 1.6rem;" title="${escapeHtml(v.id)}">${v.avatar}</span>`).join('')}
                        </div>
                    </div>
                `;
            }

            contentHtml = `
                <div class="prompt-hero-box" style="padding: 30px;">
                    ${m.image ? `<img src="${m.image}" class="prompt-hero-image">` : ''}
                    <div class="prompt-hero-text" style="font-size: 2.2rem;">${m.prompt}</div>
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-top: 10px;">
                        Matchup ${m.matchup_index} of ${m.total_matchups}
                    </div>
                </div>

                ${m.is_quiplash ? `<div class="quiplash-bonus-badge">⚡ QUIPLASH! 100% SWEEP! ⚡</div>` : ''}

                <div class="quiplash-battle-grid">
                    <div class="quip-battle-card">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <span style="font-weight: 800; font-size: 1.1rem; color: var(--secondary);">
                                ${m.revealed ? `${m.p1_avatar} ${escapeHtml(m.p1_name)}` : 'PLAYER 1'}
                            </span>
                            ${m.revealed ? `<span style="font-size: 1.4rem; font-weight: 900; color: var(--accent);">${m.p1_pct}%</span>` : ''}
                        </div>
                        <div class="quip-text">"${escapeHtml(m.p1_answer)}"</div>
                        ${m.revealed ? `
                            <div class="quip-pct-bar">
                                <div class="quip-pct-fill" style="width: ${m.p1_pct}%;"></div>
                            </div>
                        ` : ''}
                    </div>

                    <div class="quip-battle-card">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <span style="font-weight: 800; font-size: 1.1rem; color: var(--primary);">
                                ${m.revealed ? `${m.p2_avatar} ${escapeHtml(m.p2_name)}` : 'PLAYER 2'}
                            </span>
                            ${m.revealed ? `<span style="font-size: 1.4rem; font-weight: 900; color: var(--accent);">${m.p2_pct}%</span>` : ''}
                        </div>
                        <div class="quip-text">"${escapeHtml(m.p2_answer)}"</div>
                        ${m.revealed ? `
                            <div class="quip-pct-bar">
                                <div class="quip-pct-fill" style="width: ${m.p2_pct}%; background: var(--primary);"></div>
                            </div>
                        ` : ''}
                    </div>
                </div>
                ${votersHtml}
            `;
        }

        hostStage.innerHTML = `
            <div class="game-stage-wrapper">
                <div class="stage-top-bar">
                    <div class="stage-round-badge">Round ${gs.round} / ${gs.total_rounds}</div>
                    <div class="timer-pill ${isUrgent ? 'urgent' : ''}">⏱️ ${gs.timer}s</div>
                </div>
                ${contentHtml}
            </div>
        `;
    }

    // --- Trivia Dash TV ---
    function renderTriviaTV(gs) {
        const isUrgent = gs.timer <= 5 && gs.timer > 0;
        const qType = gs.q_type || 'multiple_choice';
        let bodyHtml = '';

        let typeBadge = '';
        if (qType === 'slider') {
            typeBadge = `<span class="qtype-pill qtype-slider">🎚️ Guess the Number</span>`;
        } else if (qType === 'multi_select') {
            typeBadge = `<span class="qtype-pill qtype-multiselect">☑️ Select All That Apply</span>`;
        } else if (qType === 'true_false') {
            typeBadge = `<span class="qtype-pill qtype-tf">⚡ Fact or Fiction</span>`;
        } else {
            typeBadge = `<span class="qtype-pill qtype-mc">🎯 Multiple Choice</span>`;
        }

        if (qType === 'slider') {
            if (gs.stage === 'answering') {
                bodyHtml = `
                    <div class="tv-slider-reveal-box">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--secondary); margin-bottom: 8px;">
                            Range: ${gs.min} to ${gs.max} ${gs.unit || ''}
                        </div>
                        <p style="color: var(--text-muted); font-size: 1.1rem;">Use the slider on your device to lock in your closest estimate!</p>
                    </div>
                `;
            } else if (gs.stage === 'reveal') {
                const targetVal = gs.correct_answer;
                const minVal = gs.min || 0;
                const maxVal = gs.max || 100;
                const pct = Math.max(0, Math.min(100, ((targetVal - minVal) / Math.max(1, (maxVal - minVal))) * 100));

                let guessesHtml = '';
                (gs.slider_guesses || []).forEach((g, idx) => {
                    const isBullseye = g.diff === 0;
                    guessesHtml += `
                        <div class="tv-slider-guess-card ${isBullseye ? 'is-real-truth' : ''}">
                            <span>${g.avatar} ${escapeHtml(g.name)}</span>
                            <span style="color: var(--accent); font-weight: 900;">${g.guess} ${gs.unit || ''}</span>
                            <span class="badge" style="background: ${g.score_delta > 0 ? 'var(--success)' : 'rgba(255,255,255,0.1)'}; color: #fff;">
                                +${g.score_delta} PTS
                            </span>
                        </div>
                    `;
                });

                bodyHtml = `
                    <div class="tv-slider-reveal-box">
                        <div class="tv-target-answer-pill">
                            🎯 TRUE VALUE: ${targetVal} ${gs.unit || ''}
                        </div>

                        <div class="tv-slider-track-wrap">
                            <div class="tv-slider-target-pin" style="left: ${pct}%;">
                                <span class="pin-badge">TARGET</span>
                                <div class="pin-line"></div>
                            </div>
                        </div>
                        <div class="slider-limits-row" style="margin: 0 20px 20px;">
                            <span>${minVal} ${gs.unit || ''}</span>
                            <span>${maxVal} ${gs.unit || ''}</span>
                        </div>

                        <div class="tv-slider-player-list">
                            ${guessesHtml}
                        </div>
                    </div>
                `;
            }
        } else if (qType === 'multi_select' || qType === 'multiple_choice' || qType === 'true_false') {
            let optionsHtml = '';
            if (gs.stage === 'answering') {
                const colors = ['#e94560', '#4a90e2', '#ffd166', '#06d6a0', '#9b5de5', '#f15bb5'];
                (gs.options || []).forEach((opt, idx) => {
                    optionsHtml += `
                        <div class="choice-tv-card" style="border-left: 8px solid ${colors[idx % colors.length]};">
                            <span>${escapeHtml(opt)}</span>
                        </div>
                    `;
                });
            } else if (gs.stage === 'reveal') {
                (gs.options_breakdown || []).forEach(opt => {
                    let cardClass = 'choice-tv-card';
                    if (opt.is_correct) {
                        cardClass += ' is-real-truth';
                    }
                    optionsHtml += `
                        <div class="${cardClass}">
                            <span>${escapeHtml(opt.text)}</span>
                            ${opt.is_correct ? `<div class="badge" style="background: var(--success); color: #fff; margin-top: 8px;">✓ CORRECT</div>` : `<div class="badge" style="background: rgba(233,69,96,0.3); color: var(--danger); margin-top: 8px;">✗ INCORRECT</div>`}
                            <div class="voters-pill-list">
                                ${(opt.voters || []).map(v => `<span class="voter-mini-badge">${v.avatar} ${escapeHtml(v.name)}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });
            }
            bodyHtml = `<div class="voting-choices-grid">${optionsHtml}</div>`;
        }

        hostStage.innerHTML = `
            <div class="game-stage-wrapper">
                <div class="stage-top-bar">
                    <div class="stage-round-badge">${typeBadge} ⚡ ${escapeHtml(gs.category)} (Q ${gs.round}/${gs.total_rounds})</div>
                    <div class="timer-pill ${isUrgent ? 'urgent' : ''}">⏱️ ${gs.timer}s</div>
                </div>
                <div class="prompt-hero-box">
                    <div class="prompt-hero-text">${gs.question}</div>
                    ${gs.explanation && gs.stage === 'reveal' ? `<p style="color: var(--accent); margin-top: 15px; font-size: 1.15rem; font-weight: 700;">💡 ${escapeHtml(gs.explanation)}</p>` : ''}
                </div>
                ${bodyHtml}
                <div class="players-progress-bar" style="margin-top: 20px;">
                    ${renderPlayersStatusTags(gs.players_status)}
                </div>
            </div>
        `;
    }

    // --- Bible Trivia TV ---
    function renderBibleTriviaTV(gs) {
        const isUrgent = gs.timer <= 5 && gs.timer > 0;
        const qType = gs.q_type || 'multiple_choice';
        let bodyHtml = '';

        let typeBadge = '';
        if (qType === 'slider') {
            typeBadge = `<span class="qtype-pill qtype-slider">🎚️ Guess the Number</span>`;
        } else if (qType === 'multi_select') {
            typeBadge = `<span class="qtype-pill qtype-multiselect">☑️ Select All That Apply</span>`;
        } else if (qType === 'true_false') {
            typeBadge = `<span class="qtype-pill qtype-tf">⚡ Fact or Fiction</span>`;
        } else {
            typeBadge = `<span class="qtype-pill qtype-mc">🎯 Multiple Choice</span>`;
        }

        if (qType === 'slider') {
            if (gs.stage === 'answering') {
                bodyHtml = `
                    <div class="tv-slider-reveal-box">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--secondary); margin-bottom: 8px;">
                            Range: ${gs.min} to ${gs.max} ${gs.unit || ''}
                        </div>
                        <p style="color: var(--text-muted); font-size: 1.1rem;">Use your device slider to lock in your biblical estimate!</p>
                    </div>
                `;
            } else if (gs.stage === 'reveal') {
                const targetVal = gs.correct_answer;
                const minVal = gs.min || 0;
                const maxVal = gs.max || 100;
                const pct = Math.max(0, Math.min(100, ((targetVal - minVal) / Math.max(1, (maxVal - minVal))) * 100));

                let guessesHtml = '';
                (gs.slider_guesses || []).forEach((g) => {
                    const isBullseye = g.diff === 0;
                    guessesHtml += `
                        <div class="tv-slider-guess-card ${isBullseye ? 'is-real-truth' : ''}">
                            <span>${g.avatar} ${escapeHtml(g.name)}</span>
                            <span style="color: var(--accent); font-weight: 900;">${g.guess} ${gs.unit || ''}</span>
                            <span class="badge" style="background: ${g.score_delta > 0 ? 'var(--success)' : 'rgba(255,255,255,0.1)'}; color: #fff;">
                                +${g.score_delta} PTS
                            </span>
                        </div>
                    `;
                });

                bodyHtml = `
                    <div class="tv-slider-reveal-box">
                        <div class="tv-target-answer-pill">
                            🎯 SCRIPTURE RECORD: ${targetVal} ${gs.unit || ''}
                        </div>

                        <div class="tv-slider-track-wrap">
                            <div class="tv-slider-target-pin" style="left: ${pct}%;">
                                <span class="pin-badge">TARGET</span>
                                <div class="pin-line"></div>
                            </div>
                        </div>
                        <div class="slider-limits-row" style="margin: 0 20px 20px;">
                            <span>${minVal} ${gs.unit || ''}</span>
                            <span>${maxVal} ${gs.unit || ''}</span>
                        </div>

                        <div class="tv-slider-player-list">
                            ${guessesHtml}
                        </div>
                    </div>
                `;
            }
        } else if (qType === 'multi_select' || qType === 'multiple_choice' || qType === 'true_false') {
            let optionsHtml = '';
            if (gs.stage === 'answering') {
                const colors = ['#e94560', '#4a90e2', '#ffd166', '#06d6a0', '#9b5de5', '#f15bb5'];
                (gs.options || []).forEach((opt, idx) => {
                    optionsHtml += `
                        <div class="choice-tv-card" style="border-left: 8px solid ${colors[idx % colors.length]};">
                            <span>${escapeHtml(opt)}</span>
                        </div>
                    `;
                });
            } else if (gs.stage === 'reveal') {
                (gs.options_breakdown || []).forEach(opt => {
                    let cardClass = 'choice-tv-card';
                    if (opt.is_correct) {
                        cardClass += ' is-real-truth';
                    }
                    optionsHtml += `
                        <div class="${cardClass}">
                            <span>${escapeHtml(opt.text)}</span>
                            ${opt.is_correct ? `<div class="badge" style="background: var(--success); color: #fff; margin-top: 8px;">✓ CORRECT</div>` : `<div class="badge" style="background: rgba(233,69,96,0.3); color: var(--danger); margin-top: 8px;">✗ INCORRECT</div>`}
                            <div class="voters-pill-list">
                                ${(opt.voters || []).map(v => `<span class="voter-mini-badge">${v.avatar} ${escapeHtml(v.name)}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });
            }
            bodyHtml = `<div class="voting-choices-grid">${optionsHtml}</div>`;
        }

        let verseCardHtml = '';
        if (gs.stage === 'reveal') {
            verseCardHtml = `
                <div class="bible-verse-tv-card">
                    <div class="bible-verse-ref">📖 ${escapeHtml(gs.verse_ref || '')}</div>
                    ${gs.verse_text ? `<div class="bible-verse-text">"${escapeHtml(gs.verse_text)}"</div>` : ''}
                    ${gs.explanation ? `<p style="color: var(--accent); margin-top: 10px; font-weight: 700; font-size: 1.15rem;">💡 ${escapeHtml(gs.explanation)}</p>` : ''}
                    <div class="bible-verse-attribution">${escapeHtml(gs.copyright || '')}</div>
                </div>
            `;
        }

        hostStage.innerHTML = `
            <div class="game-stage-wrapper">
                <div class="stage-top-bar">
                    <div class="stage-round-badge">
                        <span class="testament-tag">${escapeHtml(gs.testament || 'Scripture')}</span>
                        ${typeBadge} ⚡ ${escapeHtml(gs.category)} (Q ${gs.round}/${gs.total_rounds})
                    </div>
                    <div class="timer-pill ${isUrgent ? 'urgent' : ''}">⏱️ ${gs.timer}s</div>
                </div>
                <div class="prompt-hero-box">
                    <div class="prompt-hero-text">${escapeHtml(gs.question)}</div>
                </div>
                ${bodyHtml}
                ${verseCardHtml}
                <div class="players-progress-bar" style="margin-top: 20px;">
                    ${renderPlayersStatusTags(gs.players_status)}
                </div>
            </div>
        `;
    }

    // --- Doodle Guess TV ---
    function renderDoodlerTV(gs) {
        const isUrgent = gs.timer <= 5 && gs.timer > 0;
        let contentHtml = '';

        if (gs.stage === 'drawing') {
            contentHtml = `
                <div class="prompt-hero-box">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">${gs.artist_avatar}</div>
                    <div class="prompt-hero-text">${escapeHtml(gs.artist_name)} is Drawing!</div>
                    <p style="color: var(--text-muted); margin-top: 10px;">Watch the big screen as the artwork comes to life...</p>
                </div>
            `;
        } else if (gs.stage === 'bluffing' || gs.stage === 'voting' || gs.stage === 'reveal') {
            let optionsHtml = '';
            if (gs.stage === 'voting' || gs.stage === 'reveal') {
                (gs.options || []).forEach(opt => {
                    let cardClass = 'choice-tv-card';
                    let meta = '';
                    if (gs.stage === 'reveal') {
                        if (opt.is_truth) {
                            cardClass += ' is-real-truth';
                            meta = `<div class="badge" style="background: var(--success); color: #fff; margin-top: 8px;">🌟 REAL TITLE!</div>`;
                        } else {
                            cardClass += ' is-fake-lie';
                            meta = `<div class="author-tag">Bluff by: ${escapeHtml(opt.author_name || 'Nobody')}</div>`;
                        }
                        if (opt.voters && opt.voters.length > 0) {
                            meta += `<div class="voters-pill-list">${opt.voters.map(v => `<span class="voter-mini-badge">${v.avatar} ${escapeHtml(v.name)}</span>`).join('')}</div>`;
                        }
                    }
                    optionsHtml += `
                        <div class="${cardClass}">
                            <span>${escapeHtml(opt.text)}</span>
                            ${meta}
                        </div>
                    `;
                });
            }

            contentHtml = `
                <div style="display: flex; gap: 30px; align-items: center; justify-content: center; flex-wrap: wrap;">
                    <div style="background: #fff; padding: 12px; border-radius: var(--radius-md); box-shadow: var(--shadow-card);">
                        ${gs.drawing ? `<img src="${gs.drawing}" style="max-height: 340px; max-width: 400px; display: block; border-radius: 8px;">` : ''}
                    </div>
                    <div style="flex: 1; min-width: 300px;">
                        <h3 style="margin-bottom: 12px; color: var(--accent);">Artist: ${gs.artist_avatar} ${escapeHtml(gs.artist_name)}</h3>
                        ${gs.stage === 'bluffing' ? `<p style="font-size: 1.3rem;">✍️ Players are writing fake titles for this artwork!</p>` : ''}
                        <div class="voting-choices-grid">
                            ${optionsHtml}
                        </div>
                    </div>
                </div>
            `;
        }

        hostStage.innerHTML = `
            <div class="game-stage-wrapper">
                <div class="stage-top-bar">
                    <div class="stage-round-badge">🎨 Doodle Guess (Round ${gs.round}/${gs.total_rounds})</div>
                    <div class="timer-pill ${isUrgent ? 'urgent' : ''}">⏱️ ${gs.timer}s</div>
                </div>
                ${contentHtml}
            </div>
        `;
    }

    // --- Scoreboard View ---
    function renderScoreboardView(gs) {
        let itemsHtml = '';
        (gs.leaderboard || []).forEach((p, idx) => {
            const delta = (gs.round_score_deltas || {})[p.pid] || 0;
            itemsHtml += `
                <div class="leaderboard-item ${idx === 0 ? 'rank-1' : ''}">
                    <div class="player-info-group">
                        <span class="rank-number">#${idx + 1}</span>
                        <span style="font-size: 2rem;">${p.avatar}</span>
                        <div>
                            <div style="font-size: 1.2rem; font-weight: 800;">${escapeHtml(p.name)}</div>
                            ${delta > 0 ? `<span style="color: var(--success); font-size: 0.85rem; font-weight: 700;">+${delta} pts this round</span>` : ''}
                        </div>
                    </div>
                    <div class="leaderboard-score">${p.score} PTS</div>
                </div>
            `;
        });

        hostStage.innerHTML = `
            <div class="scoreboard-box">
                <h1 style="text-align: center; margin-bottom: 10px;">🏆 STANDINGS (ROUND ${gs.round})</h1>
                <div class="leaderboard-list">
                    ${itemsHtml}
                </div>
                <div style="text-align: center; margin-top: 25px;">
                    <button class="btn btn-primary" id="next-round-btn" style="font-size: 1.2rem; padding: 12px 35px;">
                        Next Round ➔
                    </button>
                </div>
            </div>
        `;

        document.getElementById('next-round-btn').addEventListener('click', () => {
            socket.emit('host_advance');
        });
    }

    // --- Victory Podium View ---
    function renderPodiumView(gs) {
        const topPlayers = gs.leaderboard || [];
        const winner = topPlayers[0] || { name: 'Winner', avatar: '👑', score: 0 };

        let listHtml = '';
        topPlayers.forEach((p, idx) => {
            listHtml += `
                <div class="leaderboard-item ${idx === 0 ? 'rank-1' : ''}">
                    <div class="player-info-group">
                        <span class="rank-number">${idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `#${idx + 1}`}</span>
                        <span style="font-size: 1.8rem;">${p.avatar}</span>
                        <span style="font-size: 1.1rem; font-weight: 800;">${escapeHtml(p.name)}</span>
                    </div>
                    <div class="leaderboard-score">${p.score} PTS</div>
                </div>
            `;
        });

        hostStage.innerHTML = `
            <div class="scoreboard-box" style="text-align: center;">
                <div style="font-size: 4.5rem; margin-bottom: 10px;">👑</div>
                <h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 5px;">${escapeHtml(winner.name)} WINS!</h1>
                <p style="color: var(--text-muted); margin-bottom: 25px;">Final Score: ${winner.score} Points</p>
                
                <div class="leaderboard-list">
                    ${listHtml}
                </div>

                <div style="display: flex; justify-content: center; gap: 15px; margin-top: 30px;">
                    <button class="btn btn-outline" id="podium-hub-btn">Return to Games Hub</button>
                    <button class="btn btn-primary" id="podium-replay-btn">Play Again 🚀</button>
                </div>
            </div>
        `;

        document.getElementById('podium-hub-btn').addEventListener('click', () => {
            socket.emit('return_to_hub');
        });

        document.getElementById('podium-replay-btn').addEventListener('click', () => {
            socket.emit('start_game');
        });
    }

    function renderPlayersStatusTags(playersStatus) {
        if (!playersStatus) return '';
        return Object.entries(playersStatus).map(([pid, p]) => `
            <div class="player-status-tag ${p.has_submitted ? 'submitted' : ''}">
                <span>${p.avatar}</span>
                <span>${escapeHtml(p.name)}</span>
                <span>${p.has_submitted ? '✓' : '...'}</span>
            </div>
        `).join('');
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
});
