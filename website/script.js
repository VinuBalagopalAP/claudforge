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
