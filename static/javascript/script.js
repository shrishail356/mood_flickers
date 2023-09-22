window.onload = function() {
  const loadingContainer = document.querySelector('.loading-container');
  const background = document.querySelector('.background');
  const loadingText = document.getElementById('loading-text');
  const loadingProgress = document.getElementById('loading-progress');
  let startTime = performance.now(); // Input start time

  // in order to hide loading message after 30secs time interval
  setTimeout(function() {
    loadingContainer.style.animation = 'fadeOut 0.5s forwards'; // Animation for fade-out
  }, 30000);

  document.addEventListener('mousemove', function(e) {
    const mouseX = e.clientX / window.innerWidth - 0.5;
    const mouseY = e.clientY / window.innerHeight - 0.5;

    background.style.transform = `translateZ(-1px) scale(2) translateX(${mouseX * 50}px) translateY(${mouseY * 50}px)`;
  });

  const updateLoadingProgress = function() {
    // Current time
    const currentTime = performance.now(); 
    const elapsedTime = currentTime - startTime;
    const progress = Math.min((elapsedTime / 30000) * 100, 100);
    loadingProgress.textContent = `${Math.round(progress)}%`;
    requestAnimationFrame(updateLoadingProgress);
  };

  updateLoadingProgress();
};

