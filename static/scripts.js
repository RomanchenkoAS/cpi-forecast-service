$(document).ready(function () {
    // Load product list
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

    $('#get-forecast').click(function () {
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
    });
});