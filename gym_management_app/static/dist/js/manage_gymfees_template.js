document.addEventListener("DOMContentLoaded", function() {
    const today = new Date();

    // Loop through each row with the 'due-row' class
    document.querySelectorAll('.due-row').forEach(function(row) {
        // Get the session_end_date from the data attribute
        const endDateStr = row.getAttribute('data-end-date');
        const endDate = new Date(endDateStr);

        // Find the <td> with class 'days-left'
        const daysLeftTd = row.querySelector('.days-left');
        // Find the "Send Email" button within the current row
        const sendEmailBtn = row.querySelector('.btn-info');

        // Calculate the difference in milliseconds
        const diffTime = endDate - today;

        // Convert milliseconds to days
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        // Check if the session has expired
        if (diffDays > 0) {
            // Display the number of days left
            daysLeftTd.textContent = diffDays + " days left";
            // Disable the "Send Email" button since there are days left
            sendEmailBtn.disabled = true;
            sendEmailBtn.classList.add('disabled'); // Bootstrap class for disabled appearance
        } else {
            // Display "Expired"
            daysLeftTd.textContent = "Expired";
            // Enable the "Send Email" button since the session has expired
            sendEmailBtn.disabled = false;
            sendEmailBtn.classList.remove('disabled');
            // Optionally add a class to style the expired rows differently
            row.classList.add('expired-row');
        }
    });
});
