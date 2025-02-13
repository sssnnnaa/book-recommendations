document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".work-request");

    // Ajout d'un div pour les messages
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        display: none;
        z-index: 1000;
        font-family: Arial, sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        min-width: 200px;
        text-align: center;
    `;
    document.body.appendChild(messageDiv);

    // Fonction pour afficher les messages
    function showMessage(message, isError = false) {
        messageDiv.style.backgroundColor = isError ? '#ff4444' : '#0f33ff';
        messageDiv.style.color = 'white';
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        
        // Animation d'entrée
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 10);

        // Cache le message après 5 secondes
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 300);
        }, 5000);
    }

    // Ajout d'un loader
    const loader = document.createElement('div');
    loader.innerHTML = `
        <div class="loader-content">
            <div class="spinner"></div>
            <div class="loader-text">Sending your recommendations...</div>
        </div>
    `;
    loader.style.cssText = `
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 1000;
        justify-content: center;
        align-items: center;
    `;
    
    const spinnerCSS = `
        <style>
            .loader-content {
                text-align: center;
                color: white;
                font-family: Arial, sans-serif;
            }
            .spinner {
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid #0f33ff;
                border-radius: 50%;
                margin: 0 auto 20px auto;
                animation: spin 1s linear infinite;
            }
            .loader-text {
                font-size: 18px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    document.head.insertAdjacentHTML('beforeend', spinnerCSS);
    document.body.appendChild(loader);

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Get form data
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const selectedTopics = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);

        // Validation
        if (!name.trim()) {
            showMessage('Please enter your name', true);
            return;
        }

        if (!email.trim() || !email.includes('@')) {
            showMessage('Please enter a valid email address', true);
            return;
        }

        if (selectedTopics.length === 0) {
            showMessage('Please select at least one topic', true);
            return;
        }

        // Show loader
        loader.style.display = 'flex';

        // Prepare data
        const formData = {
            name: name,
            email: email,
            topics: selectedTopics
        };

        try {
            console.log("Sending request...");
            const response = await fetch("/send-email", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });
            
            console.log("Response status:", response.status);
            const data = await response.json();
            console.log("Response data:", data);

            if (response.ok) {
                showMessage("Thank you! Check your email for recommendations!");
                form.reset();
            } else {
                showMessage(data.error || "An error occurred", true);
            }
        } catch (error) {
            console.error("Detailed error:", error);
            showMessage("Network error. Please try again later.", true);
        } finally {
            loader.style.display = 'none';
        }
    });
});
