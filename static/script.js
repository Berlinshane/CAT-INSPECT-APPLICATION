function startDictation(elementId) {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
            var transcript = e.results[0][0].transcript;
            document.getElementById(elementId).innerText = transcript.trim().toLowerCase();
            document.getElementById(elementId + '_textbox').value = transcript.trim().toLowerCase(); // Update text input field
            if (elementId === 'rust_dents_damage') {
                handleRustDentsDamage(transcript);
            }
            recognition.stop();
        };

        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}

function handleRustDentsDamage(transcript) {
    var notesDiv = document.getElementById('rust_dents_damage_notes');
    if (transcript === 'yes') {
        notesDiv.style.display = 'block';
    } else {
        notesDiv.style.display = 'none';
    }
}

function submitSurvey() {
    var rustDentsDamage = document.getElementById('rust_dents_damage').innerText || document.getElementById('rust_dents_damage_textbox').value;
    var engineOilCondition = document.getElementById('engine_oil_condition').innerText || document.getElementById('engine_oil_condition_textbox').value;
    var engineOilColor = document.getElementById('engine_oil_color').innerText || document.getElementById('engine_oil_color_textbox').value;
    var brakeFluidCondition = document.getElementById('brake_fluid_condition').innerText || document.getElementById('brake_fluid_condition_textbox').value;
    var brakeFluidColor = document.getElementById('brake_fluid_color').innerText || document.getElementById('brake_fluid_color_textbox').value;
    var oilLeak = document.getElementById('oil_leak').innerText || document.getElementById('oil_leak_textbox').value;

    var data = {
        rust_dents_damage: rustDentsDamage,
        engine_oil_condition: engineOilCondition,
        engine_oil_color: engineOilColor,
        brake_fluid_condition: brakeFluidCondition,
        brake_fluid_color: brakeFluidColor,
        oil_leak: oilLeak
    };

    fetch('/save_voice_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log('Success:', data);
            fetchVoiceInputs(); // Fetch updated data after successful submission
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchVoiceInputs() {
    fetch('/get_voice_inputs')
    .then(response => response.json())
    .then(data => {
        const voiceInputsDiv = document.getElementById('voice-inputs');
        voiceInputsDiv.innerHTML = '';
        
        if (data.status === "success") {
            data.data.forEach(input => {
                const p = document.createElement('p');
                p.innerText = `ID: ${input.id}, Rust/Dents/Damage: ${input.rust_dents_damage}, Engine Oil Condition: ${input.engine_oil_condition}, Engine Oil Color: ${input.engine_oil_color}, Brake Fluid Condition: ${input.brake_fluid_condition}, Brake Fluid Color: ${input.brake_fluid_color}, Oil Leak: ${input.oil_leak}`;
                voiceInputsDiv.appendChild(p);
            });
            
            data.recommendations.forEach(recommendation => {
                const p = document.createElement('p');
                p.innerText = `Recommendation for ID ${recommendation.id}: ${recommendation.recommendation}`;
                voiceInputsDiv.appendChild(p);
            });
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Fetch initial data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchVoiceInputs();
});
