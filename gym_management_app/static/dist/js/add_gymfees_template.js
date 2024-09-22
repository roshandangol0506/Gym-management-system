document.getElementById('session_start_date').addEventListener('change', updateEndDate);
    document.getElementById('amount').addEventListener('change', updateEndDate);

    function updateEndDate() {
        const startDate = document.getElementById('session_start_date').value;
        const amount = document.getElementById('amount').value;

        if (startDate && amount) {
            const start = new Date(startDate);
            let monthsToAdd = 0;

            if (amount == "2500") {
                monthsToAdd = 1;
            } else if (amount == "6000") {
                monthsToAdd = 3;
            } else if (amount == "10000") {
                monthsToAdd = 6;
            }

            start.setMonth(start.getMonth() + monthsToAdd);

            // Set the calculated end date
            const endDate = start.toISOString().split('T')[0];  // Format date as YYYY-MM-DD
            document.getElementById('session_end_date').value = endDate;
        }
    }