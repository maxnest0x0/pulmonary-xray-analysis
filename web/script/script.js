document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    const analyzeBtn = document.getElementById('analyze-btn');
    const errorMessage = document.getElementById('error-message');
    const fileUploadZone = document.getElementById('file-upload-zone');
    const overlay = document.getElementById('drop-overlay');
    const uploadBtn = document.getElementById('file-upload-btn');

    // Обработка выбора файла (клик или drag&drop)
    const handleFiles = (files) => {
        errorMessage.classList.remove('show');
        const preview = document.querySelector('.image-preview');

        if (!files || files.length === 0) {
            preview.style.display = 'none';
            uploadBtn.textContent = 'Выбрать файл';
            return;
        }

        const file = files[0];

        try {
            validateFile(file);
            uploadBtn.textContent = file.name;
            showPreview(file);
        } catch (err) {
            errorMessage.textContent = err.message;
            errorMessage.classList.add('show');
            fileInput.value = '';
            preview.style.display = 'none';
            uploadBtn.textContent = 'Выбрать файл';
        }
    };

    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

    // === DRAG & DROP ТОЛЬКО НА ЗОНЕ ===
    ['dragenter', 'dragover'].forEach((event) => {
        fileUploadZone.addEventListener(event, (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileUploadZone.classList.add('drag-over');
            overlay.style.display = 'flex';
        });
    });

    ['dragleave', 'dragend'].forEach((event) => {
        fileUploadZone.addEventListener(event, () => {
            fileUploadZone.classList.remove('drag-over');
            overlay.style.display = 'none';
        });
    });

    fileUploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileUploadZone.classList.remove('drag-over');
        overlay.style.display = 'none';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    // Клик по зоне = открыть выбор файла
    fileUploadZone.addEventListener('click', () => fileInput.click());

    // Кнопка анализа
    analyzeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        errorMessage.classList.remove('show');

        if (!fileInput.files || fileInput.files.length === 0) {
            errorMessage.textContent =
                'Пожалуйста, выберите файл для диагностики.';
            errorMessage.classList.add('show');
            return;
        }

        analyzeBtn.style.display = 'none';
        document.getElementById('loading').style.display = 'block';

        const data = new FormData();
        data.append('image', fileInput.files[0]);
        fetch('/api/analyze', {
            method: 'POST',
            body: data,
        })
            .then((res) => res.json())
            .then((res) => {
                document.getElementById('loading').style.display = 'none';
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = 'Начать диагностику';

                // Открываем модальное окно
                const modal = document.getElementById('result-modal');
                const modalText = document.getElementById('modal-result-text');
                const heatmapImg = document.getElementById('heatmap-image');

                switch (res.diagnosis) {
                    case 'normal':
                        modalText.innerHTML = `
                        <h3>Всё в норме!</h3>
                        <p><strong>Вердикт:</strong> Признаков пневмонии не обнаружено.</p>
                        <p><strong>Рекомендация:</strong> Лёгкие выглядят чистыми. Дополнительное обследование не требуется. 
                        Продолжайте вести здоровый образ жизни, при появлении симптомов (кашель, температура, одышка) — обращайтесь к врачу.</p>
                    `;
                        break;
                    case 'viral_pneumonia':
                        modalText.innerHTML = `
                        <h3>Вирусная пневмония</h3>
                        <p><strong>Вердикт:</strong> Обнаружена вирусная пневмония.</p>
                        <p><strong>Рекомендация:</strong> Срочно обратитесь к врачу. 
                        Вирусная пневмония часто требует противовирусной терапии, симптоматического лечения и наблюдения. 
                        Не занимайтесь самолечением — важно начать правильную терапию как можно раньше.</p>
                    `;
                        break;
                    case 'bacterial_pneumonia':
                        modalText.innerHTML = `
                        <h3>Бактериальная пневмония</h3>
                        <p><strong>Вердикт:</strong> Обнаружена бактериальная пневмония.</p>
                        <p><strong>Рекомендация:</strong> Это состояние требует немедленного обращения к врачу! 
                        Обычно назначаются антибиотики, иногда — госпитализация. 
                        Не откладывайте визит — бактериальная пневмония может быстро прогрессировать.</p>
                    `;
                        break;
                }

                if (res.heatmap_image) {
                    heatmapImg.style.display = 'flex';
                    heatmapImg.src = `data:${res.heatmap_image.mime};base64,${res.heatmap_image.base64}`;
                } else {
                    heatmapImg.style.display = 'none';
                }

                modal.style.display = 'block';
            });

        // Закрытие модалки
        document.querySelector('.close-modal').addEventListener('click', () => {
            document.getElementById('result-modal').style.display = 'none';
        });

        // Закрытие по клику вне окна
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('result-modal');
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Валидация
    function validateFile(file) {
        const allowed = ['image/jpeg', 'image/png', 'image/webp'];
        const maxSize = 5 * 1024 * 1024;

        if (!allowed.includes(file.type)) {
            throw new Error('Недопустимый формат. Только JPG, PNG, WebP.');
        }
        if (file.size > maxSize) {
            throw new Error('Файл слишком большой. Максимум 5 МБ.');
        }
    }

    // Превью
    function showPreview(file) {
        const preview = document.querySelector('.image-preview');
        const img = preview.querySelector('.preview-img');
        const reader = new FileReader();
        reader.onload = (e) => {
            img.src = e.target.result;
            preview.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }

    const defaultUploadBtnHTML = uploadBtn.innerHTML;

    document.querySelector('.remove-preview')?.addEventListener('click', () => {
        document.querySelector('.image-preview').style.display = 'none';
        fileInput.value = '';
        uploadBtn.innerHTML = defaultUploadBtnHTML;
        analyzeBtn.style.display = 'block';
    });
});
