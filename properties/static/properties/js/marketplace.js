// 🟦 marketplace.js

// Modal Elements
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');
const modalPrice = document.getElementById('modal-price');

// Open Modal function
function openModal(propertyId) {
    // Fetch property data from a JSON endpoint or embedded data
    // For now, let's use embedded data attributes in your template
    const card = document.querySelector(`.property-card[onclick="openModal(${propertyId})"]`);

    if (!card) return;

    // Extract data attributes or inner info
    const title = card.querySelector('.property-info h4').innerText;
    const price = card.querySelector('.price').innerText;
    
    // Optional: description if you embed it in a hidden span
    const descSpan = card.querySelector('.property-info .desc');
    const desc = descSpan ? descSpan.innerText : '';

    const img = card.querySelector('img').src;

    // Fill modal content
    modalImg.src = img;
    modalTitle.innerText = title;
    modalPrice.innerText = price;
    modalDesc.innerText = desc;

    // Show modal
    modal.style.display = 'block';
}

// Close Modal function
function closeModal() {
    modal.style.display = 'none';
}

// Optional: close modal when clicking outside content
window.onclick = function(event) {
    if (event.target === modal) {
        closeModal();
    }
}
