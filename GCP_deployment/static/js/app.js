// Update threshold value display
document.addEventListener('DOMContentLoaded', function() {
    const thresholdSlider = document.getElementById('conf_threshold');
    const thresholdValue = document.getElementById('thresholdValue');
    
    if (thresholdSlider && thresholdValue) {
        thresholdSlider.addEventListener('input', function() {
            thresholdValue.textContent = this.value;
        });
    }

    // Handle form submission
    const form = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    if (form) {
        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            btnText.textContent = 'Processing...';
            btnLoader.style.display = 'inline-block';
        });
    }
});

