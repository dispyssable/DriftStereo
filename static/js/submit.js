// static/js/submit.js
document.addEventListener("DOMContentLoaded", () => {
    const select = document.querySelector('#color');
    const preview = document.getElementById('colorPreview');
    if (!select || !preview || !window.DSUtils) return;

    function apply() {
        const hex = select.value;
        preview.style.background = hex;
        preview.style.color = DSUtils.getContrastColor(hex);
        preview.textContent = `Preview (${hex})`;
    }

    select.addEventListener('change', apply);
    apply(); // inicial
});
