// main.js — students will add JS here as features are built
// Currently handles the share button as a basic demo

document.addEventListener('DOMContentLoaded', function () {

    const shareBtn = document.getElementById('share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', function () {
            if (navigator.share) {
                navigator.share({
                    title: document.title,
                    url: window.location.href
                });
            } else {
                navigator.clipboard.writeText(window.location.href);
                shareBtn.querySelector('.action-label').textContent = 'Copied!';
                setTimeout(() => {
                    shareBtn.querySelector('.action-label').textContent = 'Share';
                }, 2000);
            }
        });
    }

});
