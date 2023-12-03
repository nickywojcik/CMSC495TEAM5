let cleanupFlag = true;

function cleanup() {
    window.addEventListener('unload', function (event) {
        if (cleanupFlag) {
            navigator.sendBeacon('/cleanup');
        }
    });
}
cleanup();