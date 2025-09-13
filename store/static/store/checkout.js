
document.addEventListener("DOMContentLoaded", function() {
    // Load Django data safely
    const quantities = JSON.parse('{{ quantities_json|escapejs }}');
    const basePrices = JSON.parse('{{ products_json|escapejs }}');

    const swagCheckbox = document.getElementById("swag");
    const twoForVoucherCheckbox = document.getElementById("two_for_one_voucher");
    const bulkTshirtCheckbox = document.getElementById("bulk_tshirt");
    const totalPriceEl = document.querySelector(".display-5");

    function updateTotal() {
        let total = 0;
        let remaining = {...quantities};

        // --- SWAG Pack First ---
        if (swagCheckbox && swagCheckbox.checked) {
            let num_swag = Math.min(remaining.VOUCHER, remaining.TSHIRT, remaining.MUG);
            total += num_swag * 25;
            remaining.VOUCHER -= num_swag;
            remaining.TSHIRT -= num_swag;
            remaining.MUG -= num_swag;
        }

        // --- 2-for-1 Voucher ---
        if (twoForVoucherCheckbox && twoForVoucherCheckbox.checked) {
            let qty = remaining.VOUCHER;
            total += ((Math.floor(qty / 2) + qty % 2) * basePrices.VOUCHER.price);
            remaining.VOUCHER = 0;
        }

        // --- Bulk T-Shirt Discount ---
        if (bulkTshirtCheckbox && bulkTshirtCheckbox.checked && remaining.TSHIRT >= 3) {
            total += remaining.TSHIRT * 19;
            remaining.TSHIRT = 0;
        }

        // --- Remaining at Normal Price ---
        total += remaining.VOUCHER * basePrices.VOUCHER.price;
        total += remaining.TSHIRT * basePrices.TSHIRT.price;
        total += remaining.MUG * basePrices.MUG.price;

        if (totalPriceEl) {
            totalPriceEl.textContent = total.toFixed(2) + "€";
        }
    }

    // Event listeners
    [swagCheckbox, twoForVoucherCheckbox, bulkTshirtCheckbox].forEach(checkbox => {
        if (checkbox) checkbox.addEventListener("change", updateTotal);
    });

    // Initial calculation
    updateTotal();
});

