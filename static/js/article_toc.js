(function () {
    const content = document.querySelector('.notebook-container');
    const nav     = document.querySelector('.contents-nav');
    if (!content || !nav) return;

    const heads = Array.from(content.querySelectorAll('h2, h3'));
    if (heads.length === 0) return;

    // "Contents" label
    const label = document.createElement('div');
    label.className = 'toc-label';
    label.textContent = 'Contents';
    nav.appendChild(label);

    // Flat list — h2 at top level, h3 indented
    const ul = document.createElement('ul');
    ul.className = 'toc-list';

    heads.forEach(h => {
        const li = document.createElement('li');
        li.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
        const a = document.createElement('a');
        const targetId = h.getAttribute('data-anchor-id') || h.closest('section')?.id || h.id;
        a.href = `#${targetId}`;
        a.textContent = h.textContent.replace(/¶$/, '').trim();
        a.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(`[data-anchor-id="${targetId}"]`) || document.getElementById(targetId);
            if (!target) return;
            const navHeight = document.querySelector('nav.site-nav')?.offsetHeight || 54;
            const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 8;
            window.scrollTo({ top, behavior: 'smooth' });
        });
        li.appendChild(a);
        ul.appendChild(li);
    });

    nav.appendChild(ul);

    // Smooth open/close animation for <details> elements
    content.querySelectorAll('details').forEach(details => {
        const summary = details.querySelector('summary');
        if (!summary) return;

        summary.addEventListener('click', e => {
            e.preventDefault();
            if (details.open) {
                const anim = details.animate(
                    { height: [`${details.offsetHeight}px`, `${summary.offsetHeight}px`] },
                    { duration: 300, easing: 'ease' }
                );
                anim.onfinish = () => { details.open = false; details.style.height = ''; };
            } else {
                details.open = true;
                const full = details.offsetHeight;
                details.animate(
                    { height: [`${summary.offsetHeight}px`, `${full}px`] },
                    { duration: 300, easing: 'ease' }
                );
            }
        });
    });
})();
