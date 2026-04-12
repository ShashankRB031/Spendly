// main.js — students will add JavaScript here as features are built

// Video Modal functionality
(function() {
    const howItWorksBtn = document.getElementById('howItWorksBtn');
    const modal = document.getElementById('videoModal');
    const closeBtn = document.getElementById('modalCloseBtn');
    const videoFrame = document.getElementById('videoFrame');

    // YouTube video URL (placeholder - replace with actual video ID)
    const videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    function openModal() {
        modal.classList.add('active');
        videoFrame.src = videoUrl;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        videoFrame.src = '';
        document.body.style.overflow = '';
    }

    if (howItWorksBtn) {
        howItWorksBtn.addEventListener('click', openModal);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
