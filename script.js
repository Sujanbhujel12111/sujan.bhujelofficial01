let formChanged = false;

function setFormChanged(changed) {
    formChanged = changed;
}

// Show confirmation message when trying to refresh or close the tab
window.addEventListener('beforeunload', function (e) {
    if (formChanged) {
        var confirmationMessage = "Are you sure you want to leave this page? You have unsaved changes.";
        e.returnValue = confirmationMessage; // Standard for most browsers
        return confirmationMessage; // For older browsers
    }
});

function addRow() {
    const tbody = document.querySelector('#financeTable tbody');
    const rowCount = tbody.children.length;
    const newRow = document.createElement('tr');
    
    newRow.innerHTML = `
        <td class='number'>${rowCount + 1}</td>
        <td><input type="text" class="accountHolder" onchange="setFormChanged(true)"></td>
        <td><input type="text" class="accountNumber" onchange="setFormChanged(true)"></td>
        <td><input type="number" class="previousBalance" onchange="calculateRowTotal(this); setFormChanged(true)"></td>
        <td><input type="number" class="todayDeposit" onchange="calculateRowTotal(this); setFormChanged(true)"></td>
        <td><input type="number" class="loanPayment" onchange="calculateRowTotal(this); setFormChanged(true)"></td>
        <td><input type="number" class="totalAmount" readonly></td>
    `;
    
    tbody.appendChild(newRow);
    setFormChanged(true);
    updateSummary();
}

function addWithdrawalRow() {
    const tbody = document.querySelector('#withdrawalTable');
    const newRow = document.createElement('tr');
    
    newRow.innerHTML = `
        <td><input type="text" onchange="setFormChanged(true)"></td>
        <td><input type="text" onchange="setFormChanged(true)"></td>
        <td><input type="number" onchange="setFormChanged(true); updateSummary()"></td>
        <td><input type="number" onchange="setFormChanged(true)"></td>
        <td><input type="text" onchange="setFormChanged(true)"></td>
    `;
    
    tbody.appendChild(newRow);
    setFormChanged(true);
}

function removeLastRow() {
    const tbody = document.querySelector('#financeTable tbody');
    const lastRow = tbody.lastElementChild;
    if (lastRow) {
        tbody.removeChild(lastRow);
    }
    setFormChanged(true);
    updateSummary();
}

function removeLastWithdrawalRow() {
    const tbody = document.querySelector('#withdrawalTable');
    const lastRow = tbody.lastElementChild;
    if (lastRow) {
        tbody.removeChild(lastRow);
    }
    setFormChanged(true);
}

function calculateRowTotal(input) {
    const row = input.closest('tr');
    const prev = parseFloat(row.querySelector('.previousBalance').value) || 0;
    const today = parseFloat(row.querySelector('.todayDeposit').value) || 0;
    const loan = parseFloat(row.querySelector('.loanPayment').value) || 0;
    
    row.querySelector('.totalAmount').value = (prev + today + loan).toFixed(2);
    updateSummary();
}

function calculateDenominationTotal() {
    let total = 0;
    document.querySelectorAll('.denomination').forEach(input => {
        const value = parseInt(input.dataset.value);
        const count = parseInt(input.value) || 0;
        const rowTotal = value * count;
        input.closest('tr').querySelector('.denomination-total').textContent = rowTotal;
        total += rowTotal;
    });
    document.getElementById('grandTotal').textContent = total.toFixed(2);
    updateFinalTotal();
}

function updateSummary() {
    let savingsTotal = 0;
    let loanTotal = 0;

    // Calculate savings total (today's deposits)
    document.querySelectorAll('.todayDeposit').forEach(input => {
        savingsTotal += parseFloat(input.value) || 0;
    });

    // Calculate loan total
    document.querySelectorAll('.loanPayment').forEach(input => {
        loanTotal += parseFloat(input.value) || 0;
    });

    // Subtract withdrawals from savings
    document.querySelectorAll('#withdrawalTable input[type="number"]:nth-child(1)').forEach(input => {
        savingsTotal -= parseFloat(input.value) || 0;
    });

    document.getElementById('savingsTotal').value = savingsTotal.toFixed(2);
    document.getElementById('loanTotal').value = loanTotal.toFixed(2);
    updateFinalTotal();
}

function updateFinalTotal() {
    const savings = parseFloat(document.getElementById('savingsTotal').value) || 0;
    const loan = parseFloat(document.getElementById('loanTotal').value) || 0;
    const other = parseFloat(document.getElementById('otherTotal').value) || 0;
    
    const finalTotal = savings + loan + other;
    document.getElementById('finalTotal').value = finalTotal.toFixed(2);

    // Verify against denomination total
    const denominationTotal = parseFloat(document.getElementById('grandTotal').textContent) || 0;
    if (denominationTotal !== finalTotal) {
        document.getElementById('finalTotal').style.color = 'red';
    } else {
        document.getElementById('finalTotal').style.color = 'black';
    }
}

function saveData() {
    // Here you would typically implement the actual save functionality
    const formData = {
        date: document.getElementById('date').value,
        sector: document.getElementById('sector').value,
        representative: document.getElementById('representative').value,
        totalMembers: document.getElementById('totalMembers').value,
        transactions: [],
        withdrawals: [],
        denominations: {},
        summary: {
            savings: document.getElementById('savingsTotal').value,
            loan: document.getElementById('loanTotal').value,
            other: document.getElementById('otherTotal').value,
            total: document.getElementById('finalTotal').value
        }
    };

    // Collect transaction data
    document.querySelectorAll('#financeTable tbody tr').forEach(row => {
        formData.transactions.push({
            accountHolder: row.querySelector('.accountHolder').value,
            accountNumber: row.querySelector('.accountNumber').value,
            previousBalance: row.querySelector('.previousBalance').value,
            todayDeposit: row.querySelector('.todayDeposit').value,
            loanPayment: row.querySelector('.loanPayment').value,
            totalAmount: row.querySelector('.totalAmount').value
        });
    });

    // Collect withdrawal data
    document.querySelectorAll('#withdrawalTable tr').forEach(row => {
        const inputs = row.querySelectorAll('input');
        if (inputs.length === 5) {
            formData.withdrawals.push({
                accountHolder: inputs[0].value,
                accountNumber: inputs[1].value,
                withdrawalAmount: inputs[2].value,
                remainingBalance: inputs[3].value,
                mobileNumber: inputs[4].value
            });
        }
    });

    // Collect denomination data
    document.querySelectorAll('.denomination').forEach(input => {
        formData.denominations[input.dataset.value] = input.value;
    });

    // In a real application, you would send this data to a server
    console.log('Form Data:', formData);
    setFormChanged(false);
    alert('Data saved successfully!');
}

document.addEventListener('DOMContentLoaded', function() {
    addRow();
    
    // Add event listeners for real-time updates
    document.getElementById('otherTotal').addEventListener('input', updateFinalTotal);
    document.querySelectorAll('.denomination').forEach(input => {
        input.addEventListener('input', calculateDenominationTotal);
    });
});

// Optional: validate before print to check for unsaved changes
function validateBeforePrint() {
    if (formChanged) {
        if (!confirm('You have unsaved changes. Are you sure you want to print?')) {
            return false;
        }
    }
    window.print();
}
