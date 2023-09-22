window.onload = function () {
    const loadingContainer = document.querySelector('.loading-container');
    const background = document.querySelector('.background');
    const loadingText = document.getElementById('loading-text');
    const loadingProgress = document.getElementById('loading-progress');
    let startTime = performance.now(); // Input start time
  
    // Function to hide loading message after 30 seconds
    const hideLoading = function () {
      loadingContainer.style.animation = 'fadeOut 0.5s forwards'; // Animation for fade-out
    };
  
    // Hide loading message after 30 seconds
    setTimeout(hideLoading, 30000);
  
    document.addEventListener('mousemove', function (e) {
      const mouseX = e.clientX / window.innerWidth - 0.5;
      const mouseY = e.clientY / window.innerHeight - 0.5;
  
      background.style.transform = `translateZ(-1px) scale(2) translateX(${mouseX * 50}px) translateY(${mouseY * 50}px)`;
    });
  
    const updateLoadingProgress = function () {
      // Current time
      const currentTime = performance.now();
      const elapsedTime = currentTime - startTime;
      const progress = Math.min((elapsedTime / 30000) * 100, 100);
      loadingProgress.textContent = `${Math.round(progress)}%`;
      requestAnimationFrame(updateLoadingProgress);
    };
  
    updateLoadingProgress();
  
    const platformDropdown = document.getElementById('platform');
    const contentTypeDropdown = document.getElementById('content_type');
    const dynamicInput = document.getElementById('dynamic_input');
    const contentOptions = {
      instagram: ['comments', 'posts', 'overview', 'profile'],
      facebook: ['comments', 'pages'],
      twitter: ['profiles'],
    };
  
    function updateContentOptions() {
      const selectedPlatform = platformDropdown.value;
      const options = contentOptions[selectedPlatform] || [];
  
      contentTypeDropdown.innerHTML = '';
      options.forEach((option) => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        contentTypeDropdown.appendChild(optionElement);
      });
    }
    function showInputFields() {
      const selectedContent = contentTypeDropdown.value;
      dynamicInput.innerHTML = '';
  
      if (selectedContent === 'comments' || selectedContent == 'posts') {
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.name = 'post_link';
        inputField.placeholder = 'Enter Post Link';
        inputField.id = 'post_link';
        dynamicInput.appendChild(inputField);
      } else if (selectedContent === 'profile') {
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.name = 'username';
        inputField.placeholder = 'Enter Profile Username ';
        dynamicInput.appendChild(inputField);
      } else if (selectedContent === 'pages' || selectedContent === 'profiles') {
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.name = 'profile_name';
        inputField.placeholder = 'Enter Profile/Page Name';
        dynamicInput.appendChild(inputField);
      } else if (selectedContent === 'overview') {
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.name = 'overview';
        inputField.placeholder = 'Enter Profile Username';
        dynamicInput.appendChild(inputField);
      }
    }
  
    function displayScrapedData(data) {
      const table = document.getElementById('scraped_data');
      table.innerHTML = ''; // Clear previous data
  
      if (data && data.length > 0) {
        const headerRow = document.createElement('tr');
        for (const key in data[0]) {
          const th = document.createElement('th');
          th.textContent = key;
          headerRow.appendChild(th);
        }
        table.appendChild(headerRow);
  
        data.forEach((item) => {
          const row = document.createElement('tr');
          for (const key in item) {
            const cell = document.createElement('td');
            cell.textContent = item[key];
            row.appendChild(cell);
          }
          table.appendChild(row);
        });
  
        table.style.display = 'table';
      } else {
        table.style.display = 'none';
      }
    }
  
    platformDropdown.addEventListener('change', () => {
      updateContentOptions();
      showInputFields();
      document.getElementById('scraped_data').style.display = 'none';
    });
    contentTypeDropdown.addEventListener('change', showInputFields);
    updateContentOptions();
    showInputFields();
  };
  