$(document).ready(function() {
    // Populate the product dropdown
    $.get('/get_products', function(products) {
        products.forEach(function(product) {
            $('#product-select').append($('<option>', {
                value: product[1], // slugified product name
                text: product[0]  // original product name
            }));
        });
    });

    // Handle button click
    $('#get-forecast').click(function() {
        var selectedProduct = $('#product-select').val();
        if (selectedProduct) {
            var imageUrl = '/forecast/' + encodeURIComponent(selectedProduct) + '?t=' + new Date().getTime();
            $('#forecast-image').attr('src', imageUrl).show();
        } else {
            alert('Please select a product');
        }
    });
});