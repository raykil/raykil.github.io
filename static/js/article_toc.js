(function () {
    const content = document.querySelector('.notebook-container'); // the serialized ipynb. Identical to build/articles/Brownian_motion/index.html.
    const nav     = document.querySelector('.contents-nav');
    // if (!content || !nav) return;
    // console.log(content);
    const heads = Array.from(content.querySelectorAll('h2, h3'));
    // heads.forEach(h=> {console.log("textContent is: ", h.textContent, "tagname is: ", h.tagName)});

    // Table of Contents DOM (Document Object Model)
    const fragment = document.createDocumentFragment();
    // What are these?
    let currentDetails = null;
    let currentList = null;

    heads.forEach( h => {
        currentDetails = document.createElement('details');
        currentDetails.className = 'toc-item';
        const summary = document.createElement('summary');
        const chev = document.createElement('span');
        chev.className = 'chevron';
        summary.appendChild(chev);
        summary.appendChild(document.createTextNode(h.textContent));
        currentDetails.appendChild(summary);
        currentList = document.createElement('ul');
        currentList.className = 'subsections';
        currentDetails.appendChild(currentList);
        fragment.appendChild(currentDetails);
        
        if (h.tagName === 'H3') {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${h.id}`;
            a.textContent = h.textContent;
            li.appendChild(a);
            currentList.appendChild(li);
        }
    })

    // Injecting to <nav>
    // nav.innerHTML = '';
    nav.appendChild(fragment);

})();