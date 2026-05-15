(function() {
    const canvas = document.getElementById('binaryCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const FONT_SIZE = 15;
    let cols, drops, speeds;

    function init() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        cols = Math.floor(canvas.width / FONT_SIZE);
        drops = Array.from({length: cols}, () => Math.random() * -(canvas.height / FONT_SIZE));
        speeds = Array.from({length: cols}, () => 0.3 + Math.random() * 1.2);
    }

    init();
    window.addEventListener('resize', init);

    const COLORS = [
        [255, 255, 255],
        [180, 200, 255],
        [140, 170, 255],
        [100, 140, 240],
    ];

    function draw() {
        ctx.fillStyle = 'rgba(10, 18, 40, 0.13)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = `bold ${FONT_SIZE}px 'Courier New', monospace`;

        for (let i = 0; i < cols; i++) {
            const y = drops[i] * FONT_SIZE;
            const x = i * FONT_SIZE;
            const char = Math.random() > 0.5 ? '1' : '0';
            const isHead = (drops[i] % 1) < speeds[i];

            if (isHead) {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
                ctx.shadowColor = '#7c9fff';
                ctx.shadowBlur = 10;
            } else {
                const c = COLORS[Math.floor(Math.random() * COLORS.length)];
                const alpha = 0.12 + Math.random() * 0.45;
                ctx.fillStyle = `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${alpha})`;
                ctx.shadowBlur = 0;
            }

            ctx.fillText(char, x, y);
            ctx.shadowBlur = 0;

            if (y > canvas.height && Math.random() > 0.97) {
                drops[i] = 0;
                speeds[i] = 0.3 + Math.random() * 1.2;
            }
            drops[i] += speeds[i];
        }
    }

    setInterval(draw, 40);
})();
