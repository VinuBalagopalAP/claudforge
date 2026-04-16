// GH Stars Fetch
async function fetchStars() {
    try {
        const response = await fetch('https://api.github.com/repos/VinuBalagopalAP/claudforge');
        const data = await response.json();
        if (data.stargazers_count !== undefined) {
            document.getElementById('star-count').innerText = data.stargazers_count;
        }
    } catch (error) {
        console.error('Error fetching stars:', error);
        document.getElementById('star-count').innerText = '10+'; // Fallback
    }
}
fetchStars();

// Reveal Observer
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
    });
}, { threshold: 0.1 });
document.querySelectorAll('.animate-in, .animate-on-scroll, .suite-card, .toolbox-card').forEach(el => observer.observe(el));

// Terminal Copy Logic
document.addEventListener('click', (e) => {
    const copyBtn = e.target.closest('.t-copy');
    if (copyBtn) {
        const terminal = copyBtn.closest('.terminal-loader');
        const textElement = terminal.querySelector('.t-body');
        
        // Clean text (remove $ prompt and extra spaces)
        let text = textElement.innerText;
        if (text.includes('$')) {
            text = text.split('$')[1];
        }
        text = text.trim();

        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.querySelector('span').innerText;
            copyBtn.querySelector('span').innerText = 'Copied!';
            copyBtn.classList.add('copied');
            
            setTimeout(() => {
                copyBtn.querySelector('span').innerText = originalText;
                copyBtn.classList.remove('copied');
            }, 2000);
        });
    }
});
