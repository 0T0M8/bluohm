// Dark mode toggle
const darkToggle = document.getElementById('dark-toggle');
if(darkToggle){
    darkToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
    });
}

// Modal
const modal = document.getElementById('modal');
const modalImages = document.getElementById('modal-images');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');
const modalPrice = document.getElementById('modal-price');

function openModal(propertyId){
    fetch(`/api/properties/${propertyId}/`)  // optionally create a simple JSON endpoint
        .then(res => res.json())
        .then(data => {
            modalImages.innerHTML = '';
            data.images.forEach(img => {
                const el = document.createElement('img');
                el.src = img.url;
                modalImages.appendChild(el);
            });
            modalTitle.innerText = data.title;
            modalDesc.innerText = data.description;
            modalPrice.innerText = `MWK ${data.price}`;
            modal.style.display = 'block';
        });
}

function closeModal(){
    modal.style.display = 'none';
}
