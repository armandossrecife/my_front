// Toggle Main Sidebar
document.getElementById('toggleSidebar').addEventListener('click', function () {
    const mainSidebar = document.getElementById('mainSidebar');
    const bsCollapse = new bootstrap.Collapse(mainSidebar, { toggle: true });
});