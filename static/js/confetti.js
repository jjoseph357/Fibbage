/**
 * Lightweight Canvas Confetti Generator
 */
(function() {
    window.launchConfetti = function() {
        const canvas = document.createElement('canvas');
        canvas.id = 'confetti-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '99999';
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const pieces = [];
        const colors = ['#e94560', '#50c878', '#4a90e2', '#ffd166', '#06d6a0', '#118ab2', '#ff9f1c'];

        for (let i = 0; i < 150; i++) {
            pieces.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height - canvas.height,
                size: Math.random() * 10 + 6,
                color: colors[Math.floor(Math.random() * colors.length)],
                vx: (Math.random() - 0.5) * 4,
                vy: Math.random() * 4 + 3,
                rotation: Math.random() * 360,
                vrot: (Math.random() - 0.5) * 10
            });
        }

        let animationFrame;
        let frameCount = 0;

        function update() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            pieces.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                p.rotation += p.vrot;

                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                ctx.restore();
            });

            frameCount++;
            if (frameCount < 250) {
                animationFrame = requestAnimationFrame(update);
            } else {
                cancelAnimationFrame(animationFrame);
                if (canvas.parentNode) {
                    canvas.parentNode.removeChild(canvas);
                }
            }
        }

        update();
    };
})();
