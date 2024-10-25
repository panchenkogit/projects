// Функция для подсчета калорий на основе введенных данных
function calculateCalories() {
    const proteins = parseFloat(document.getElementById("proteins").value) || 0;
    const fats = parseFloat(document.getElementById("fats").value) || 0;
    const carbohydrates = parseFloat(document.getElementById("carbohydrates").value) || 0;
    
    const calories = proteins * 4 + fats * 9 + carbohydrates * 4;
    document.getElementById("calories").value = calories.toFixed(1);
}

// Функция для отправки данных продукта на сервер
async function addProduct() {
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const proteins = parseFloat(document.getElementById("proteins").value) || 0;
    const fats = parseFloat(document.getElementById("fats").value) || 0;
    const carbohydrates = parseFloat(document.getElementById("carbohydrates").value) || 0;
    const calories = parseFloat(document.getElementById("calories").value) || 0;

    const product = { name, description, proteins, fats, carbohydrates, calories };

    try {
        const response = await fetch('/product/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });

        if (response.ok) {
            const result = await response.json();
            showNotification(`Продукт "${result.name}" добавлен!`);
        } else {
            console.error('Ошибка при добавлении продукта:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
    }
}

// Функция для показа уведомления о добавлении продукта
function showNotification(message) {
    const notification = document.createElement("div");
    notification.className = "notification";
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = "0";
        setTimeout(() => document.body.removeChild(notification), 1000);
    }, 3000);
}

// Загрузка продуктов при загрузке страницы
document.addEventListener("DOMContentLoaded", loadProducts);

async function loadProducts() {
    try {
        const response = await fetch("/products");
        if (!response.ok) {
            throw new Error("Ошибка загрузки данных");
        }
        const products = await response.json();
        const tableBody = document.getElementById("productTable").getElementsByTagName("tbody")[0];
        tableBody.innerHTML = "";  // Очищаем таблицу

        products.forEach(product => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.description || ""}</td>
                <td>${product.proteins}</td>
                <td>${product.fats}</td>
                <td>${product.carbohydrates}</td>
                <td>${product.calories}</td>
            `;
        });
    } catch (error) {
        console.error("Ошибка при загрузке продуктов:", error);
    }
}


