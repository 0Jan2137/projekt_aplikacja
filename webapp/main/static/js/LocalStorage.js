function saveState(key, obj) {
    localStorage.setItem(key, JSON.stringify( obj ));
}

function loadState(key) {
    const saved = localStorage.getItem(key);
    if (!saved) {
        return null;
    }
    try {
        return JSON.parse(saved);
    } catch (error) {
        return null;
    }
}