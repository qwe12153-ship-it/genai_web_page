const sidebar = document.querySelector('.sidebar');
const resizer = document.querySelector('.resizer');
let isResizing = false;
let startX = 0;
let startWidth = 0;

resizer.addEventListener('mousedown', function(e) {
    if (window.innerWidth <= 700) return; // Disable on mobile
    isResizing = true;
    startX = e.clientX;
    startWidth = sidebar.offsetWidth;
    document.body.style.cursor = 'ew-resize';
    document.body.style.userSelect = 'none';
});

document.addEventListener('mousemove', function(e) {
    if (!isResizing) return;
    let delta = startX - e.clientX;
    let newWidth = startWidth + delta;
    newWidth = Math.max(150, Math.min(400, newWidth)); // min/max width
    sidebar.style.width = newWidth + 'px';
});

document.addEventListener('mouseup', function() {
    isResizing = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
});