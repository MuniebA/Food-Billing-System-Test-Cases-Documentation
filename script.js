document.addEventListener('DOMContentLoaded', () => {
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    document.querySelectorAll('.quantity').forEach(input => {
        input.addEventListener('input', (e) => {
            const value = e.target.value.replace(/[^0-9]/g, '');
            e.target.value = value ? parseInt(value) : '';
        });
    });

    document.getElementById('calculate').addEventListener('click', () => {
        const items = document.querySelectorAll('.item');
        const discountCheckbox = document.getElementById('discount');
        let subtotal = 0;
        let billDetails = '';
        let hasItems = false;

        // Add debug logging
        console.log('Discount checkbox state:', discountCheckbox.checked);

        items.forEach(item => {
            const price = parseFloat(item.dataset.price);
            const quantity = parseInt(item.querySelector('.quantity').value) || 0;
            const itemName = item.querySelector('h2').innerText;

            if (quantity > 0) {
                hasItems = true;
                let itemTotal = parseFloat((price * quantity).toFixed(2));
                subtotal = parseFloat((subtotal + itemTotal).toFixed(2));
                billDetails += `
                    <div class="bill-item">
                        <span>${itemName} × ${quantity}</span>
                        <span>${formatCurrency(itemTotal)}</span>
                    </div>`;
            }
        });

        if (!hasItems) {
            document.getElementById('bill-details').innerHTML = `
                <p class="no-items">Please select at least one item to generate bill.</p>`;
            return;
        }

        console.log('Subtotal before discount:', subtotal);

        // Calculate final amounts with precise decimal handling
        let subtotalAfterDiscount = subtotal;
        let discountAmount = 0;

        if (discountCheckbox && discountCheckbox.checked) {
            discountAmount = parseFloat((subtotal * 0.5).toFixed(2));
            subtotalAfterDiscount = parseFloat((subtotal - discountAmount).toFixed(2));
        }

        console.log('Subtotal after discount:', subtotalAfterDiscount);

        const sst = parseFloat((subtotalAfterDiscount * 0.06).toFixed(2));
        const total = parseFloat((subtotalAfterDiscount + sst).toFixed(2));

        console.log('SST:', sst);
        console.log('Final total:', total);

        const detailedBill = `
            <div class="order-section">
                <h3>Order Details</h3>
                <div class="bill-items">
                    ${billDetails}
                </div>
            </div>
            
            <div class="calculations-section">
                <h3>Bill Calculations</h3>
                <div class="bill-calculations">
                    <div class="subtotal">
                        <span>Sub Total:</span>
                        <span>${formatCurrency(subtotal)}</span>
                    </div>
                    ${discountCheckbox && discountCheckbox.checked ? `
                        <div class="discount">
                            <span>Discount Amount (50%):</span>
                            <span>-${formatCurrency(discountAmount)}</span>
                        </div>
                        <div class="subtotal-after-discount">
                            <span>Total after discount:</span>
                            <span>${formatCurrency(subtotalAfterDiscount)}</span>
                        </div>
                    ` : ''}
                    <div class="sst">
                        <span>SST (6%):</span>
                        <span>${formatCurrency(sst)}</span>
                    </div>
                </div>
                
                <div class="bill-total">
                    <span>Final Total with SST:</span>
                    <span>${formatCurrency(total)}</span>
                </div>
            </div>`;

        document.getElementById('bill-details').innerHTML = detailedBill;

        if (window.innerWidth <= 992) {
            document.querySelector('.bill-summary').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});