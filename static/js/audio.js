/**
 * Web Audio API Procedural Sound FX Synthesizer
 * Zero external audio files required. Works 100% offline.
 */
class SoundSynthesizer {
    constructor() {
        this.ctx = null;
        this.isMuted = localStorage.getItem('party_game_muted') === 'true';
    }

    init() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) {
                this.ctx = new AudioCtx();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggleMute() {
        this.isMuted = !this.isMuted;
        localStorage.setItem('party_game_muted', this.isMuted);
        return this.isMuted;
    }

    _playTone(freq, type, duration, gainStart = 0.15, gainEnd = 0.001) {
        if (this.isMuted) return;
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

        gain.gain.setValueAtTime(gainStart, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(gainEnd, this.ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    }

    playClick() {
        this._playTone(600, 'sine', 0.08, 0.1);
    }

    playJoin() {
        if (this.isMuted) return;
        this.init();
        [440, 554.37, 659.25, 880].forEach((freq, i) => {
            setTimeout(() => this._playTone(freq, 'triangle', 0.25, 0.15), i * 70);
        });
    }

    playStart() {
        if (this.isMuted) return;
        this.init();
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
            setTimeout(() => this._playTone(freq, 'sine', 0.35, 0.2), i * 90);
        });
    }

    playTick() {
        this._playTone(900, 'triangle', 0.05, 0.08);
    }

    playBuzzer() {
        if (this.isMuted) return;
        this.init();
        this._playTone(150, 'sawtooth', 0.4, 0.25);
    }

    playReal() {
        if (this.isMuted) return;
        this.init();
        // Major chord shimmer
        [523.25, 659.25, 783.99, 1046.50, 1318.51].forEach((freq, i) => {
            setTimeout(() => this._playTone(freq, 'sine', 0.5, 0.2), i * 60);
        });
    }

    playFake() {
        if (this.isMuted) return;
        this.init();
        // Cartoon slide down
        this._playTone(350, 'sawtooth', 0.25, 0.2);
        setTimeout(() => this._playTone(220, 'sawtooth', 0.35, 0.2), 180);
    }

    playQuiplash() {
        if (this.isMuted) return;
        this.init();
        [440, 659.25, 880, 1108.73, 1318.51].forEach((freq, i) => {
            setTimeout(() => this._playTone(freq, 'square', 0.3, 0.15), i * 75);
        });
    }

    playWin() {
        if (this.isMuted) return;
        this.init();
        const melody = [523.25, 523.25, 523.25, 659.25, 783.99, 659.25, 783.99, 1046.50];
        const times = [0, 120, 240, 360, 480, 600, 720, 900];
        melody.forEach((freq, i) => {
            setTimeout(() => this._playTone(freq, 'triangle', 0.4, 0.25), times[i]);
        });
    }
}

window.soundFX = new SoundSynthesizer();
