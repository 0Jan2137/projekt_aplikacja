const ACTIVE_TAB_KEY = 'active-tab';
const SORT_DIRECTION_KEY = 'sort-direction';

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