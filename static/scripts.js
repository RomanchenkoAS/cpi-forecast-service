$(document).ready(function () {
    if ($('#product-select').length > 0) {
        // Load product list only if #product-select is present
        $.getJSON('/get_products', function (products) {
            products.forEach(function (product, index) {
                var option = $('<option>', {
                    value: product[1], // slugified product name
                    text: product[0]  // original product name
                });
                $('#product-select').append(option);

                // Set the first option as selected
                if (index === 0) {
                    option.attr('selected', 'selected');
                }
            });
        });

        // Tie getForecast function to the button
        $('#get-forecast').click(getForecast);
    }
});


function getForecast() {
    var productName = $('#product-select').val();
    if (productName) {
        // Get metadata
        $.getJSON('/get_metadata/' + encodeURIComponent(productName), function (metadata) {
            var metadataHtml = `
                <h6>Metadata:</h6>
                <p>Product: ${metadata.product_name}</p>
                <p>Train MAE: ${metadata.train_mae.toFixed(2)}</p>
                <p>Test MAE: ${metadata.test_mae.toFixed(2)}</p>
                <p>Date Created: ${new Date(metadata.date_created).toLocaleString()}</p>
            `;
            $('#metadata').html(metadataHtml);
        });

        // Load forecast image
        $('#forecast-image').attr('src', '/forecast/' + encodeURIComponent(productName)).show();
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
        handleError(data.Error)
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