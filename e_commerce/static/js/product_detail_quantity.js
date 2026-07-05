document.addEventListener('DOMContentLoaded', function () {
    const quantityInput = document.getElementById('product-quantity');
    const buyNowQuantityInput = document.getElementById('buy-now-quantity');

    if (quantityInput && buyNowQuantityInput) {
        const syncQuantity = () => {
            buyNowQuantityInput.value = quantityInput.value;
        };

        quantityInput.addEventListener('input', syncQuantity);
        quantityInput.addEventListener('change', syncQuantity);
    }
});
