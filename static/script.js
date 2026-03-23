document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const imagePreview = document.getElementById('imagePreview');
    const dropzoneContent = document.getElementById('dropzoneContent');
    const captionInput = document.getElementById('captionInput');
    const generateBtn = document.getElementById('generateBtn');
    
    const resultsSection = document.getElementById('resultsSection');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');
    const resultsContent = document.getElementById('resultsContent');
    const shortAltTextEl = document.getElementById('shortAltText');
    const longAltTextEl = document.getElementById('longAltText');
    
    let selectedFile = null;

    // Drag and Drop Flow
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
    });

    dropzone.addEventListener('drop', handleDrop, false);
    dropzone.addEventListener('click', () => fileInput.click());
    
    // Accessibility: Trigger open on enter/space
    dropzone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', handleFileSelect);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];
        
        if (!file.type.startsWith('image/')) {
            showError("Please upload an image file (PNG, JPG, WebP)");
            return;
        }

        selectedFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.hidden = false;
            dropzoneContent.hidden = true;
            generateBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Generate Action
    generateBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI updates
        resultsSection.hidden = false;
        loadingState.hidden = false;
        errorState.hidden = true;
        resultsContent.hidden = true;
        generateBtn.disabled = true;

        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('caption', captionInput.value.trim());

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate alt text. Please check server logs.');
            }

            // Populate results
            shortAltTextEl.textContent = data.short_alt_text || "No short alt text generated.";
            longAltTextEl.textContent = data.long_alt_text || "No long alt text generated.";
            
            // Show results
            loadingState.hidden = true;
            resultsContent.hidden = false;

        } catch (error) {
            showError(error.message);
        } finally {
            generateBtn.disabled = false;
        }
    });

    function showError(message) {
        resultsSection.hidden = false;
        loadingState.hidden = true;
        resultsContent.hidden = true;
        errorState.hidden = false;
        errorMessage.textContent = message;
    }

    // Copy functionality
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const textToCopy = document.getElementById(targetId).textContent;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                const icon = btn.querySelector('i');
                const originalClass = icon.className;
                
                icon.className = 'fi fi-rr-check';
                btn.classList.add('copied');
                btn.setAttribute('aria-label', 'Copied to clipboard');
                
                setTimeout(() => {
                    icon.className = originalClass;
                    btn.classList.remove('copied');
                    btn.setAttribute('aria-label', `Copy ${targetId === 'shortAltText' ? 'short' : 'long'} alt text`);
                }, 2000);
            });
        });
    });
});
