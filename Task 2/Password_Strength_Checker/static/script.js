document.getElementById('password').addEventListener('input', checkPassword);

// Store the original thead elements
const originalPropertiesHeader = document.querySelector('#properties thead');
const originalCrackingHeader = document.querySelector('#cracking-times thead');

// Remove the thead elements from the tables initially
originalPropertiesHeader.remove();
originalCrackingHeader.remove();

// Toggle password visibility
const eyeIcon = document.getElementById('eye-icon');
eyeIcon.addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        passwordInput.type = 'password';
        eyeIcon.innerHTML = '<i class="fas fa-eye"></i>';
    }
});

// Hide Password Report text and tables initially
const passwordReport = document.querySelector('.password-report');
const tablesSection = document.querySelector('.tables-section');
passwordReport.style.display = 'none';
tablesSection.style.display = 'none';

function checkPassword() {
    const password = document.getElementById('password').value;
    const container = document.querySelector('.container');
    const strongerPasswordText = document.getElementById('stronger-password-text');
    const generateButton = document.getElementById('generate-button');

    // After processing the response and updating the UI, check if the password is empty
    if (!document.getElementById('password').value) {
        // If the password field is empty, show the elements
        strongerPasswordText.style.display = 'block';
        generateButton.style.display = 'block';
    } else {
        // If the password field is not empty, hide the elements
        strongerPasswordText.style.display = 'none';
        generateButton.style.display = 'none';
    }

    if (!password) {
        container.style.backgroundColor = ''; // Reset background color
        document.getElementById('results').style.display = 'none';
        strongerPasswordText.style.display = 'block';
        generateButton.style.display = 'block';

        // Re-add the thead elements to the tables
        document.querySelector('#properties').appendChild(originalPropertiesHeader);
        document.querySelector('#cracking-times').appendChild(originalCrackingHeader);

        // Reset all fields to N/A or 0
        document.getElementById('strength-percent').textContent = '(0%)';
        document.getElementById('evaluation').textContent = 'N/A';
        document.getElementById('progress').style.width = '0%';
        document.getElementById('progress').style.backgroundColor = 'gray';

        const propertiesTable = document.getElementById('properties').getElementsByTagName('tbody')[0];
        propertiesTable.innerHTML = '';
        const properties = {
            "Password length": { "value": 0, "comment": "N/A" },
            "Numbers": { "value": 0, "comment": "N/A" },
            "Uppercase Letters": { "value": 0, "comment": "N/A" },
            "Lowercase Letters": { "value": 0, "comment": "N/A" },
            "Symbols": { "value": 0, "comment": "N/A" },
            "Letters": { "value": 0, "comment": "N/A" },
            "TOP 10000 password": { "value": "N/A", "comment": "N/A" },
            "Charset size": { "value": 0, "comment": "N/A" },
        };
        for (const prop in properties) {
            const row = propertiesTable.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);
            cell1.textContent = prop;
            cell2.textContent = properties[prop].value;
            cell3.textContent = properties[prop].comment;
            cell3.style.color = 'goldenrod'; // Default color
        }

        const crackingTable = document.getElementById('cracking-times').getElementsByTagName('tbody')[0];
        crackingTable.innerHTML = '';
        const crackingTimes = {
            "Standard Desktop PC": "N/A",
            "Fast Desktop PC": "N/A",
            "GPU": "N/A",
            "Fast GPU": "N/A",
            "Parallel GPUs": "N/A",
            "Medium size botnet": "N/A",
        };
        for (const machine in crackingTimes) {
            const row = crackingTable.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            cell1.textContent = machine;
            cell2.textContent = crackingTimes[machine];
        }

        document.getElementById('safe').textContent = 'Your password is: N/A';
        document.getElementById('safe').style.color = 'gray';
        document.getElementById('cracking-message').textContent = 'It would take a computer to crack this password.';

        return;
    }

    strongerPasswordText.style.display = 'none';
    generateButton.style.display = 'none';

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `password=${encodeURIComponent(password)}`,
    })
        .then(response => response.json())
        .then(data => {
            // Dynamic background color for container
            const strength = data.strength;
            const strengthColors = [
                { strength: 30, color: 'rgb(245 159 159)' },
                { strength: 60, color: 'rgb(255 227 176)' },
                { strength: 80, color: 'rgb(255 255 180)' },
                { strength: 100, color: 'rgb(178 253 178)' }
            ];
            let backgroundColor = 'gray';
            for (const range of strengthColors) {
                if (strength <= range.strength) {
                    backgroundColor = range.color;
                    break;
                }
            }
            container.style.backgroundColor = backgroundColor; // Change container background

            // Rest of the code remains the same
            document.getElementById('results').style.display = 'block';

            // Show table names and headers
            document.querySelectorAll('.table-name').forEach(element => {
                element.style.display = 'block';
            });

            // Re-add the thead elements to the tables
            document.querySelector('#properties').appendChild(originalPropertiesHeader);
            document.querySelector('#cracking-times').appendChild(originalCrackingHeader);

            document.getElementById('strength-percent').textContent = `(${data.strength}%)`;
            document.getElementById('evaluation').textContent = data.evaluation;

            // Change progress bar color based on strength
            const progressBar = document.getElementById('progress');
            progressBar.style.width = `${data.strength}%`;
            if (data.strength < 30) {
                progressBar.style.backgroundColor = 'red';
            } else if (data.strength < 70) {
                progressBar.style.backgroundColor = 'orange';
            } else {
                progressBar.style.backgroundColor = 'green';
            }

            const propertiesTable = document.getElementById('properties').getElementsByTagName('tbody')[0];
            propertiesTable.innerHTML = '';
            for (const prop in data.properties) {
                const row = propertiesTable.insertRow();
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                const cell3 = row.insertCell(2);
                cell1.textContent = prop;
                cell2.textContent = data.properties[prop].value;
                cell3.textContent = data.properties[prop].comment;

                // Change comment text color based on comment
                if (data.properties[prop].comment.includes("Missing") || data.properties[prop].comment.includes("Short") || data.properties[prop].comment.includes("Too") || data.properties[prop].comment.includes("Password is one of the most frequently used passwords.")) {
                    cell3.style.color = 'maroon';
                } else if (data.properties[prop].comment.includes("Medium")) {
                    cell3.style.color = 'goldenrod';
                } else if (data.properties[prop].comment.includes("OK") || data.properties[prop].comment.includes("Used") || data.properties[prop].comment.includes("High") || data.properties[prop].comment.includes("Password is NOT one of the most frequently used passwords.")) {
                    cell3.style.color = 'green';
                } else {
                    cell3.style.color = 'goldenrod';
                }
            }

            const crackingTable = document.getElementById('cracking-times').getElementsByTagName('tbody')[0];
            crackingTable.innerHTML = '';
            for (const machine in data.cracking_times) {
                const row = crackingTable.insertRow();
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                cell1.textContent = machine;
                cell2.textContent = data.cracking_times[machine];
            }

            // Update cracking message with "Fast Desktop PC" time (bold, large, and in quotes)
            const crackingMessage = document.getElementById('cracking-message');
            if (data.cracking_times && data.cracking_times['Fast Desktop PC']) {
                crackingMessage.innerHTML = `It would take a computer about <span style='font-size: larger;'>&quot;<b>${data.cracking_times['Fast Desktop PC']}</b>&quot;</span> to crack this password.`;
            } else {
                crackingMessage.textContent = 'It would take a computer to crack this password.';
            }

            // Show the password report and tables section
            passwordReport.style.display = 'block';
            tablesSection.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
