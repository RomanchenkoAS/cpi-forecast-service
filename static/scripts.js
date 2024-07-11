document.addEventListener('DOMContentLoaded', function () {
    const productSelect = document.getElementById('product-select');
    if (productSelect) {
        // Load product list only if #product-select is present
        fetch('/get_products')
            .then(response => response.json())
            .then(products => {
                products.forEach((product, index) => {
                    const option = document.createElement('option');
                    option.value = product[1]; // slugified product name
                    option.text = product[0];  // original product name
                    productSelect.appendChild(option);

                    // Set the first option as selected
                    if (index === 0) {
                        option.selected = true;
                    }
                });
            });

        // Tie getForecast function to the button
        document.getElementById('get-forecast').addEventListener('click', getForecast);
    }
});

function getForecast() {
    const productName = document.getElementById('product-select').value;
    if (productName) {
        // Get metadata
        fetch('/get_metadata/' + encodeURIComponent(productName))
            .then(response => response.json())
            .then(metadata => {
                console.log(metadata);
                document.getElementById('metadata').innerHTML = `
                    <h6>Metadata:</h6>
                    <p>Product: ${metadata.product_name}</p>
                    <p>Date Created: ${metadata.date_created}</p>
                    <p>Train MAE: ${metadata.train_mae.toFixed(2)}</p>
                    <p>Test MAE: ${metadata.test_mae.toFixed(2)}</p>
                    <hr>
                    <p>Confidence interval estimation</p>
                    <p>Avg in-sample CI: ${metadata.avg_in_sample_ci_width.toFixed(2)}</p>
                    <p>Max in-sample CI: ${metadata.max_in_sample_ci_width.toFixed(2)}</p>
                    <p>Avg forecast CI: ${metadata.avg_forecast_ci_width.toFixed(2)}</p>
                    <p>Max forecast CI: ${metadata.max_forecast_ci_width.toFixed(2)}</p>
                `;
            });

        // Load forecast image
        const forecastImage = document.getElementById('forecast-image');
        forecastImage.src = '/forecast/' + encodeURIComponent(productName);
        forecastImage.style.display = 'block';
    }
}

function fetchModels(type) {
    const loader = document.getElementById(`loader-${type}`);
    loader.style.display = 'inline-block';

    if (type === 'auto') {
        fetch('/models')
            .then(response => response.json())
            .then(handleResponse)
            .catch(handleError)
            .finally(() => loader.style.display = 'none');
    } else if (type === 'upload') {
        const form = document.getElementById('upload-form');
        const formData = new FormData(form);

        fetch('/models', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(handleResponse)
            .catch(handleError)
            .finally(() => loader.style.display = 'none');
    }
}

function handleResponse(data) {
    if (data.success === true) {
        window.location.href = '/plot';
    } else {
        handleError(data.error);
    }
}

function handleError(error) {
    const message_box = document.getElementById('message-placeholder');
    message_box.style.display = 'block';
    message_box.className = 'message error';
    message_box.textContent = 'Error: ' + error;
}

function eraseModels() {
    fetch('/erase')
        .then(response => response.json())
        .then(data => {
            if (data.success === true) {
                // alert('Models erased successfully');
                location.reload();
            } else {
                handleError(data.error);
            }
        })
        .catch(error => {
            handleError(error);
        });
}