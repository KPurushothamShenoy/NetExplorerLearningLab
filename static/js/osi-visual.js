function updateOSI(activeLayer) {
    const layers = document.querySelectorAll('.osi-layer');
    layers.forEach(layer => {
        layer.classList.remove('active');
        if (parseInt(layer.dataset.layer) === activeLayer) {
            layer.classList.add('active');
        }
    });
}

function completeOSILayer(layerNum) {
    const layer = document.querySelector(`.osi-layer[data-layer="${layerNum}"]`);
    if (layer) {
        layer.classList.remove('active');
        layer.classList.add('completed');
    }
}