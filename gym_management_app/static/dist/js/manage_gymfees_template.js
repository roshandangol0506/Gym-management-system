document.addEventListener("DOMContentLoaded", function() {
    const today = new Date();

    document.querySelectorAll('.due-row').forEach(function(row) {
        const endDateStr = row.getAttribute('data-end-date');
        const endDate = new Date(endDateStr);

        const daysLeftTd = row.querySelector('.days-left');
        const sendEmailBtn = row.querySelector('.btn-info');

        const diffTime = endDate - today;

        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays > 0) {
            daysLeftTd.textContent = diffDays + " days left";
            sendEmailBtn.disabled = true;
            sendEmailBtn.classList.add('disabled'); 
        } else {
            daysLeftTd.textContent = "Expired";
            sendEmailBtn.disabled = false;
            sendEmailBtn.classList.remove('disabled');
            row.classList.add('expired-row');
        }
    });

    // Listen for the success or error message to change button color
    if (document.querySelector('.messages.success')) {
        console.log("Roshan")
        const sendEmailBtn = document.querySelector('.send-email-btn');
        sendEmailBtn.classList.add('btn-black');  // Change to black on success
    } else{
        console.log("Dangol")
    }
});
