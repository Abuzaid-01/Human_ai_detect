// // Track text statistics
// document.addEventListener('DOMContentLoaded', function() {
//     const textArea = document.getElementById('text');
//     const charCount = document.getElementById('character-count');
//     const wordCount = document.getElementById('word-count');
//     const clearBtn = document.getElementById('clear-btn');
    
//     if (textArea && charCount && wordCount) {
//         // Update counts on input
//         textArea.addEventListener('input', updateCounts);
        
//         // Initial counts
//         updateCounts();
        
//         // Clear button functionality
//         if (clearBtn) {
//             clearBtn.addEventListener('click', function() {
//                 textArea.value = '';
//                 updateCounts();
//                 textArea.focus();
//             });
//         }
//     }
    
//     function updateCounts() {
//         const text = textArea.value;
//         const chars = text.length;
        
//         // Count words (split by whitespace and filter out empty strings)
//         const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        
//         charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
//         wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
//     }
// });

// // Add animation to the result page
// document.addEventListener('DOMContentLoaded', function() {
//     const meter = document.querySelector('.meter span');
    
//     if (meter) {
//         // Get the width from style attribute and set it to 0 initially
//         const widthValue = meter.style.width;
//         meter.style.width = '0';
        
//         // Trigger animation after a short delay
//         setTimeout(() => {
//             meter.style.width = widthValue;
//         }, 300);
//     }
// });







// Track text statistics and handle UI interactions
document.addEventListener('DOMContentLoaded', function() {
    const textArea = document.getElementById('text');
    const charCount = document.getElementById('character-count');
    const wordCount = document.getElementById('word-count');
    const clearBtn = document.getElementById('clear-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const classifyForm = document.getElementById('classify-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const exampleButtons = document.querySelectorAll('.example-button');
    
    // Text statistics tracking
    if (textArea && charCount && wordCount) {
        // Update counts on input
        textArea.addEventListener('input', updateCounts);
        
        // Initial counts
        updateCounts();
        
        // Clear button functionality
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                textArea.value = '';
                updateCounts();
                textArea.focus();
            });
        }
        
        // Show loading overlay when form is submitted
        if (classifyForm) {
            classifyForm.addEventListener('submit', function(e) {
                if (textArea.value.trim().length < 10) {
                    e.preventDefault();
                    alert('Please enter at least a few sentences for accurate classification.');
                    return;
                }
                
                if (loadingOverlay) {
                    loadingOverlay.classList.add('visible');
                }
            });
        }
        
        // Example text buttons
        if (exampleButtons.length > 0) {
            exampleButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const type = button.getAttribute('data-example');
                    
                    if (type === 'human') {
                        textArea.value = "The sunset cast a golden glow across the rippling water, creating a moment of perfect serenity. As I watched from the weathered dock, I couldn't help but reflect on how these small instances of natural beauty often go unnoticed in our busy lives. My grandfather used to say that watching the sunset was like reading a letter from the universe - a reminder that we're part of something greater, something that continues with or without our attention. Yesterday's sunset was particularly striking, with streaks of purple I hadn't seen before.";
                    } else if (type === 'ai') {
                        textArea.value = "The implementation of artificial intelligence in healthcare systems has demonstrated significant potential for improving diagnostic accuracy and treatment outcomes. Research indicates that AI algorithms can analyze medical imaging with precision comparable to expert radiologists, while simultaneously processing patient data at unprecedented speeds. Furthermore, these systems can identify patterns and correlations that may not be immediately apparent to human practitioners, thereby enhancing the overall quality of care provided to patients. The integration of such technologies represents a transformative shift in medical practice.";
                    }
                    
                    updateCounts();
                });
            });
        }
    }
    
    function updateCounts() {
        const text = textArea.value;
        const chars = text.length;
        
        // Count words (split by whitespace and filter out empty strings)
        const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        
        charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
        wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
        
        // Dynamically adjust textarea height
        textArea.style.height = 'auto';
        textArea.style.height = (textArea.scrollHeight) + 'px';
    }
});

// Result page animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate confidence meter
    const meter = document.querySelector('.meter span');
    
    if (meter) {
        // Get the width from style attribute and set it to 0 initially
        const widthValue = meter.style.width;
        meter.style.width = '0';
        
        // Trigger animation after a short delay
        setTimeout(() => {
            meter.style.width = widthValue;
        }, 300);
    }
    
    // Add scroll effect to analyzed text
    const textDisplay = document.querySelector('.text-display');
    if (textDisplay) {
        // Add a slight delay to highlight the text
        setTimeout(() => {
            textDisplay.classList.add('highlighted');
        }, 800);
    }
    
    // Disable back button resubmission
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});