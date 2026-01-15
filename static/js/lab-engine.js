document.getElementById('start-btn').addEventListener('click', async () => {
    const btn = document.getElementById('start-btn');
    btn.innerText = "Launching Container...";
    
    const response = await fetch('/start-lab', { method: 'POST' });
    const data = await response.json();
    
    if (data.container_id && !data.container_id.startsWith("ERROR")) {
        document.getElementById('container-display').innerText = data.container_id.substring(0, 12);
        document.getElementById('mission-box').classList.add('hidden');
        document.getElementById('lab-interface').classList.remove('hidden');
        
        // Update OSI Visual to Network Layer (Layer 3)
        updateOSI(3);
    } else {
        alert("Docker Error: " + data.container_id);
        btn.innerText = "Retry Initialization";
    }
});

document.getElementById('submit-val').addEventListener('click', async () => {
    const subnet = document.getElementById('subnet-input').value;
    
    const response = await fetch('/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subnet: subnet })
    });
    const data = await response.json();
    
    if (data.result) {
        document.getElementById('lab-interface').classList.add('hidden');
        document.getElementById('success-box').classList.remove('hidden');
        completeOSILayer(3);
    } else {
        alert("Incorrect Subnet Mask. Try again!");
    }
});

document.getElementById('complete-btn').addEventListener('click', async () => {
    const response = await fetch('/complete-lab', { method: 'POST' });
    const data = await response.json();
    
    if (data.uploaded) {
        alert("Report successfully saved to AWS S3!");
        window.location.href = "/history";
    }
});