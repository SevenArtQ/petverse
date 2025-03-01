let tg = window.Telegram.WebApp;

// Инициализация Telegram Mini App
tg.expand();

// Замените URL на реальный URL вашего бэкенда
const API_URL = 'http://localhost:8000';

// Получение данных питомца
async function getPetData() {
    try {
        const response = await fetch(`${API_URL}/api/pet-data`, {
            headers: {
                'Authorization': `Bearer ${tg.initData}`
            }
        });
        const data = await response.json();
        updatePetUI(data);
    } catch (error) {
        console.error('Error fetching pet data:', error);
    }
}

// Обновление интерфейса
function updatePetUI(petData) {
    document.getElementById('healthBar').style.width = `${petData.health}%`;
    document.getElementById('happinessBar').style.width = `${petData.happiness}%`;
    
    // Обновление аватара питомца
    const petAvatar = document.getElementById('petAvatar');
    petAvatar.style.backgroundImage = `url(${getPetImage(petData.type, petData.level)})`;
}

// Действия с питомцем
async function feedPet() {
    try {
        const response = await fetch('/api/feed', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${tg.initData}`
            }
        });
        const data = await response.json();
        updatePetUI(data);
        tg.showPopup({
            title: 'Успех!',
            message: 'Питомец накормлен'
        });
    } catch (error) {
        console.error('Error feeding pet:', error);
    }
}

async function playWithPet() {
    // Аналогично feedPet()
}

async function trainPet() {
    // Аналогично feedPet()
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    getPetData();
}); 