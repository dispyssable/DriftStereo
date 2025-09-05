document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("galleryGrid");
    if (!grid) return;

    async function loadMessages() {
        const res = await fetch("/messages.json", { cache: "no-store" });
        const items = await res.json();

        grid.innerHTML = items.map(m => {
            const textColor = DSUtils.getContrastColor(m.color);
            const time = new Date(m.created_at).toLocaleString();
            return `
        <article class="card" style="background:${m.color}; color:${textColor};">
          <h3>To: ${m.to}</h3>
          <p>${m.body}</p>
          <time>${time}</time>
        </article>
      `;
        }).join("");
    }

    loadMessages();
    setInterval(loadMessages, 10000);
});
